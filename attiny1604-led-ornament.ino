/*
 * Chip: ATtiny1604
 * Clock: 20MHz internal
 * Startup time: 8ms
 */
#include <avr/sleep.h>
#include <avr/interrupt.h>
#include <tinyNeoPixel.h>

#define PIN_INTERRUPT PIN_PA2
#define WS2812_DATA PIN_PA1 // Neopixel data line
#define WS2812_VCC PIN_PA6 // Neopixel power line

#define PORTA_INT_BM PORT_INT2_bm

#define NUMPIXELS 1
tinyNeoPixel pixels(NUMPIXELS, WS2812_DATA, NEO_GRB + NEO_KHZ800);

typedef struct rgb {
    int r;
    int g;
    int b;
} Rgb;

typedef struct hsv {
  uint16_t h;
  uint8_t s;
  uint8_t v;
} Hsv;

typedef struct ledColor {
  Rgb rgb;
  Hsv hsv;
} LedColor;

ISR(PORTA_PORT_vect) {
  PORTA.INTFLAGS = PORTA_INT_BM;
}

void setup() {
  pinMode(PIN_INTERRUPT, INPUT_PULLUP);
  pinMode(WS2812_VCC, OUTPUT);

  // pull up unused pins
  pinMode(PIN_PA0, INPUT_PULLUP);
  pinMode(PIN_PA3, INPUT_PULLUP);
  pinMode(PIN_PA4, INPUT_PULLUP);
  pinMode(PIN_PA5, INPUT_PULLUP);
  pinMode(PIN_PA7, INPUT_PULLUP);
  pinMode(PIN_PB0, INPUT_PULLUP);
  pinMode(PIN_PB1, INPUT_PULLUP);
  pinMode(PIN_PB2, INPUT_PULLUP);
  pinMode(PIN_PB3, INPUT_PULLUP);

  PORTA.PIN2CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;

  pixels.begin();
}

int counter = 0;
int wakeupInterval = 10;

void loop() {
  if (counter == 0 || counter >= wakeupInterval) {
    digitalWrite(WS2812_VCC, HIGH);
    handleOnShake();
    counter = 0;  
  }
  counter++;

  goToSleep();
}

void goToSleep() {
  digitalWrite(WS2812_VCC, LOW);

  cli();

  // Disable the ADC
  ADC0.CTRLA &= ~ADC_ENABLE_bm;
   
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();

  sei();
  sleep_cpu();

  sleep_disable();
}

