import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import shutil
import subprocess
from subprocess import PIPE
import tkinter
import tkinter.ttk
from tkinter import messagebox
import asyncio
import sys

async def read_stream(stream, callback):
    """Reads lines from a stream and forwards them to a callback function."""
    while True:
        line = await stream.readline()
        if line:
            callback(line.decode('utf-8'))
        else:
            break

async def run_command(cmd):
    # Start the process asynchronously
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Define how to handle the live text
    def handle_stdout(text):
        print(f"{text}", end="")

    def handle_stderr(text):
        print(f"{text}", end="", file=sys.stderr)

    # Run stream readers concurrently
    await asyncio.gather(
        read_stream(process.stdout, handle_stdout),
        read_stream(process.stderr, handle_stderr)
    )

    # Wait for the process to exit completely
    return_code = await process.wait()
    return return_code

parser = argparse.ArgumentParser()
parser.add_argument(
    "--arduino-cli",
    required=True,
    type=str,
    metavar="/path/to/arduino-cli.exe",
    help="Path to arduino-cli.exe",
)
parser.add_argument(
    "--avrdude",
    required=True,
    type=str,
    metavar="/path/to/avrdude",
    help="Path to avrdude",
)
parser.add_argument(
    "--serial-port",
    required=True,
    type=str,
    metavar="/path/to/serial-port",
    help="Serial port path or name",
)
parser.add_argument(
    "--file-server",
    required=True,
    type=str,
    metavar="https://file-server.com",
    help="File server URL",
)

parser.add_argument(
    "--basic-auth-username",
    type=str,
    metavar="username",
    help="Username for basic auth (if needed)",
)

parser.add_argument(
    "--basic-auth-password",
    type=str,
    metavar="password",
    help="Password for basic auth (if needed)",
)

args = parser.parse_args()

if not os.path.exists(args.arduino_cli):
    raise FileNotFoundError(f"{args.arduino_cli} not found")

if not os.path.exists(args.avrdude):
    raise FileNotFoundError(f"{args.avrdude} not found")

if args.basic_auth_username and args.basic_auth_password:
    auth = HTTPBasicAuth(args.basic_auth_username, args.basic_auth_password)
else:
    auth = None

root = None
combobox = None
button = None

users = {}


def compile_and_flush_code():
    global combobox
    global button

    button.config(state="disabled")
    button.update()

    user = combobox.get()
    print(user, users[user])

    if os.path.exists("build"):
        shutil.rmtree("build")

    # download
    button.config(text="ダウンロード中...")
    button.update()
    print("ダウンロード中...")
    # download_file(users[user], './onshake_handler.ino')
    url = args.file_server if args.file_server[-1] != "/" else args.file_server[:-1]
    url = f"{url}/download/{users[user]}"
    print(url)
    r = requests.get(url, allow_redirects=True, auth=auth)
    open("./onshake_handler.ino", "wb").write(r.content)

    # compile
    command = [args.arduino_cli, "compile", "--fqbn", "megaTinyCore:megaavr:atxy4:chip=1604", "--build-path", "./build", "-v"]
    button.config(text="コンパイル中...")
    button.update()
    print("コンパイル中...")
    print(" ".join(command))
    return_code = asyncio.run(run_command(command))
    if return_code != 0:
        messagebox.showerror(title="エラー", message="コンパイルに失敗しました")
        button.config(text="コンパイル & 書き込み", state="normal")
        button.update()
        return

    # flush
    command = [os.path.join(args.avrdude, "bin", "avrdude.exe"), "-C", os.path.join(args.avrdude, "etc", "avrdude.conf"),  "-v", "-p", "attiny1604", "-c", "serialupdi", "-P", args.serial_port, "-U", "flash:w:build/attiny1604-led-ornament.ino.hex:i"]
    button.config(text="書き込み中...")
    button.update()
    print("書き込み中...")
    print(" ".join(command))
    return_code = asyncio.run(run_command(command))
    if return_code != 0:
        messagebox.showerror(title="エラー", message="書き込みに失敗しました")
    else:
        messagebox.showinfo(title="完了", message="コンパイルと書き込みが完了しました")
        
    button.config(text="コンパイル & 書き込み", state="normal")
    button.update()


url = args.file_server if args.file_server[-1] != "/" else args.file_server[:-1]
url = f"{url}/download/users"
r = requests.get(url, allow_redirects=True, auth=auth)
if r.status_code != 200:
    messagebox.showerror(title="エラー", message="サーバーにアクセスできません")
    exit(-1)
users = {user["display_name"]: user["username"] for user in r.json()["users"]}

root = tkinter.Tk()
root.title("LEDオーナメント | 書き込みツール")
root.geometry("320x160")
root.configure(background="#EEEEEE")

combobox = tkinter.ttk.Combobox(
    root, state="readonly", values=[key for key in users.keys()]
)
combobox.current(0)
combobox.pack(pady=24)

button = tkinter.Button(
    text="コンパイル & 書き込み", padx=24, pady=16, command=compile_and_flush_code
)
button.pack(pady=16)

root.mainloop()
