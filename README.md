## PCB components
### U1: ATTiny1604
https://akizukidenshi.com/catalog/g/g131108/

### C1: 0.1uF
https://akizukidenshi.com/catalog/g/g113374/

### C2: 10uF
https://akizukidenshi.com/catalog/g/g113161/

### LED1: WS2812C-2020
https://akizukidenshi.com/catalog/g/g115068/

### PW1
Original CR1220 battery case

### SW1: SW-18030

## Flask server
### GET parameter
#### `user`
User name: `user1`|`user2`|`user3`|`user4`|`user5`|`user6`|`user7`|`user8`

example: http://192.168.1.1:8000?user=user1

### References
#### Editor
- Makecode micro:bit
https://makecode.microbit.org/#editor

#### Fonts
- MADE Tommy Soft
https://www.dafont.com/made-tommy-soft.font
- Font Awesome
https://fontawesome.com

#### JS library
- highlight.js
https://github.com/highlightjs/highlight.js
- jscolor
https://jscolor.com

## `compile_and_flush_code.py`
A Tkinter app for compiling and writing an Arduino led ornament project.

### paremeters
#### `--arduino-cli`
Path to the command `arduino-cli`
#### `--avrdude`
Path to the command `--avrdude`
#### `--file-server`
The URL of the Flask file server
#### `--basic-auth-username`
The username of the basic authentication
#### `--basic-auth-password`
The password of the basic authentication

#### Example
```
python compile_and_flush_code.py --arduino-cli=/path/to/arduino-cli --avrdude=/path/to/avrdude --file-server=https://app-creator.tech/ --basic-auth-username <username> --basic-auth-password <password>
```
