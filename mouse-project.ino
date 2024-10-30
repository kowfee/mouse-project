/*
 * Copyright (c) 2024, wareya
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <SPI.h>
#include <mbed.h>


#include <Adafruit_NeoPixel.h>

// constants won't change. They're used here to 
// set pin numbers:
const int ledPin = 26;     // the number of the neopixel strip
const int numLeds = 2;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(numLeds, ledPin, NEO_GRB + NEO_KHZ800);




REDIRECT_STDOUT_TO(Serial);

#include <PluggableUSBHID.h>

#include "src/srom_3360_0x04.h"
#include "src/relmouse_16.h"
USBMouse16 mouse(false);

#define REG_PRODUCT_ID (0x00)
#define REG_REVISION_ID (0x01)
#define REG_MOTION (0x02)
#define REG_DELTA_X_L (0x03)
#define REG_DELTA_X_H (0x04)
#define REG_DELTA_Y_L (0x05)
#define REG_DELTA_Y_H (0x06)
#define REG_SQUAL (0x07)
#define REG_RAW_DATA_SUM (0x08)
#define REG_MAX_RAW_DATA (0x09)
#define REG_MIN_RAW_DATA (0x0A)
#define REG_SHUTTER_LOWER (0x0B)
#define REG_SHUTTER_UPPER (0x0C)
#define REG_CONTROL (0x0D)

#define REG_CONFIG1 (0x0F)
#define REG_CONFIG2 (0x10)
#define REG_ANGLE_TUNE (0x11)
#define REG_FRAME_CAPTURE (0x12)
#define REG_SROM_ENABLE (0x13)
#define REG_RUN_DOWNSHIFT (0x14)
#define REG_REST1_RATE_LOWER (0x15)
#define REG_REST1_RATE_UPPER (0x16)
#define REG_REST1_DOWNSHIFT (0x17)
#define REG_REST2_RATE_LOWER (0x18)
#define REG_REST2_RATE_UPPER (0x19)
#define REG_REST2_DOWNSHIFT (0x1A)
#define REG_REST3_RATE_LOWER (0x1B)
#define REG_REST3_RATE_UPPER (0x1C)

#define REG_OBSERVATION (0x24)
#define REG_DATA_OUT_LOWER (0x25)
#define REG_DATA_OUT_UPPER (0x26)

#define REG_RAW_DATA_DUMP (0x29)
#define REG_SROM_ID (0x2A)
#define REG_MIN_SQ_RUN (0x2B)
#define REG_RAW_DATA_THRESHOLD (0x2C)

#define REG_CONFIG5 (0x2F)

#define REG_POWER_UP_RESET (0x3A)
#define REG_SHUTDOWN (0x3B)

#define REG_INVERSE_PRODUCT_ID (0x3F)

#define REG_LIFTCUTOFF_TUNE3 (0x41)
#define REG_ANGLE_SNAP (0x42)

#define REG_LIFTCUTOFF_TUNE1 (0x4A)

#define REG_MOTION_BURST (0x50)

#define REG_LIFTCUTOFF_TUNE_TIMEOUT (0x58)

#define REG_LIFTCUTOFF_TUNE_MIN_LENGTH (0x5A)

#define REG_SROM_LOAD_BURST (0x62)
#define REG_LIFT_CONFIG (0x63)
#define REG_RAW_DATA_BURST (0x64)
#define REG_LIFTOFF_TUNE2 (0x65)

#define CONFIG2_REST_ENABLED (0x30)
#define CONFIG2_REPORT_MODE (0x04)


#define BUTTONS_ON 0
#define BUTTONS_OFF 1

#define BUTTON_M1 2
#define BUTTON_M2 3
#define BUTTON_M3 4
#define BUTTON_M4 6
#define BUTTON_M5 7
#define BUTTON_DPI 5

#define ENCODER_A 8
#define ENCODER_B 10
#define ENCODER_COM 9

#define PIN_NCS 17
#define PIN_MOSI 19
#define PIN_MISO 16

SPISettings spisettings(2000000, MSBFIRST, SPI_MODE3);
MbedSPI spi(PIN_MISO, PIN_MOSI, 18);

void setup_buttons()
{
    pinMode(BUTTONS_OFF, INPUT);
    pinMode(BUTTONS_ON, INPUT);
    pinMode(BUTTON_M1, INPUT_PULLUP);
    pinMode(BUTTON_M2, INPUT_PULLUP);
    pinMode(BUTTON_M3, INPUT_PULLUP);
    pinMode(BUTTON_M4, INPUT_PULLUP);
    pinMode(BUTTON_M5, INPUT_PULLUP);
    pinMode(BUTTON_DPI, INPUT_PULLUP);
    
    pinMode(ENCODER_A, INPUT_PULLUP);
    pinMode(ENCODER_B, INPUT_PULLUP);
    pinMode(ENCODER_COM, OUTPUT);
    
    digitalWrite(ENCODER_COM, LOW);
}

void setup()
{
    Serial1.begin(1000000);
    
    delay(3000);
    
    // SCK, MISO, MOSI, SS
    SPI.begin();
    pinMode(PIN_NCS, OUTPUT);
    
    digitalWrite(PIN_NCS, HIGH);
    delayMicroseconds(1);
    digitalWrite(PIN_NCS, LOW);
    delayMicroseconds(1);
    digitalWrite(PIN_NCS, HIGH);
    delayMicroseconds(1);
    
    pmw3360_boot();
    
    delay(10);
    
    pmw3360_config(15);
    
    setup_buttons();
    strip.begin();
    strip.setBrightness(80); // 1/3 brightness
}

uint32_t pins_state = 0;
uint8_t buttons = 0;
// 8ms latch time
uint8_t buttons_latch_max = 8;
uint8_t buttons_latch[5] = {0, 0, 0, 0, 0};

int dpi_values[] = {34};
int NUM_DPI_VALUES = sizeof(dpi_values) / sizeof(dpi_values[0]);
int current_dpi_index = 0;

#define GLOBAL_BRIGHTNESS 10
int rgb_modes[] = {0, 1, 2, 3, 4};
// 0 - off; 1 - static color; 2 - rainbow; 3 - police; 4 - breathing
int NUM_RGB_MODES = sizeof(rgb_modes) / sizeof(rgb_modes[0]);
int rgb_selector = 3;


volatile uint32_t * pad_control = (uint32_t *)0x4001c000;
volatile uint32_t * gpio_oe_set = (uint32_t *)0xd0000024;
volatile uint32_t * gpio_oe_clr = (uint32_t *)0xd0000028;
volatile uint32_t * gpio_in = (uint32_t *)0xd0000004;

void test() {
    // Your test function implementation here
}

void update_buttons() {
    /*
    // disable pullup/pulldown
    pad_control[BUTTONS_OFF + 1] &= 0xFFFFFFF2;
    pad_control[BUTTONS_ON + 1] &= 0xFFFFFFF2;
    */
    
    // change BUTTONS_OFF to high impedance and BUTTONS_ON to output
    // using pinMode for this is way, WAY too slow, like 50us per call (?!?!?!)
    *gpio_oe_clr = 1 << BUTTONS_OFF;
    *gpio_oe_set = 1 << BUTTONS_ON;
    
    // read ON pins
    digitalWrite(BUTTONS_ON, LOW);
    delayMicroseconds(1);
    uint32_t pins_on = ~*gpio_in;
    
    // change BUTTONS_OFF to high impedance and BUTTONS_ON to output
    *gpio_oe_set = 1 << BUTTONS_OFF;
    *gpio_oe_clr = 1 << BUTTONS_ON;
    
    // read OFF pins
    digitalWrite(BUTTONS_OFF, LOW);
    delayMicroseconds(1);
    uint32_t pins_off = ~*gpio_in;
    
    // update pin state
    // treat middle state (on-off matching) as no-update (use previous state)
    uint32_t pins_update = pins_on ^ pins_off;
    pins_state = (pins_state & (~pins_update)) | (pins_on & pins_update);
    
    // update button state
    uint8_t next_buttons =
          ((!!(pins_state & (1 << BUTTON_M1))))
        | ((!!(pins_state & (1 << BUTTON_M2))) << 1)
        | ((!!(pins_state & (1 << BUTTON_M3))) << 2)
        | ((!!(pins_state & (1 << BUTTON_M4))) << 3)
        | ((!!(pins_state & (1 << BUTTON_M5))) << 4);
    
    // handle latch
    uint8_t ok_mask = 
          ((buttons_latch[0] == 0))
        | ((buttons_latch[1] == 0) << 1)
        | ((buttons_latch[2] == 0) << 2)
        | ((buttons_latch[3] == 0) << 3)
        | ((buttons_latch[4] == 0) << 4);
    
    next_buttons = (next_buttons & ok_mask) | (buttons & ~ok_mask);
    
    // update latch timings
    for (int i = 0; i < 5; i++) {
        if (((next_buttons ^ buttons) >> i) & 1)
            buttons_latch[i] = buttons_latch_max;
        else if (buttons_latch[i])
            buttons_latch[i] -= 1;
    }
    
    static bool dpi_button_pressed = false;
    static uint32_t dpi_button_press_time = 0;
    static const uint32_t HOLD_THRESHOLD = 2000; // 2 seconds

    // Detect BUTTON_DPI press and release (state change)
    bool current_dpi_state = pins_state & (1 << BUTTON_DPI);


    if ((!dpi_button_pressed) && (current_dpi_state))
    {
        // Button was just pressed
        dpi_button_pressed = true;
        dpi_button_press_time = millis(); // Track time of button press
    }
    else if ((dpi_button_pressed) && (millis() - dpi_button_press_time >= HOLD_THRESHOLD) && (!current_dpi_state))
    {
        rgb_selector = (rgb_selector + 1) % NUM_RGB_MODES;
        dpi_button_press_time = millis(); // Reset the press time to avoid multiple calls
        dpi_button_pressed = false;
    }
    else if ((dpi_button_pressed) && (!current_dpi_state))
    {
        // Button was just released
        dpi_button_pressed = false;

        // Cycle through dpi values
        current_dpi_index = (current_dpi_index + 1) % NUM_DPI_VALUES;
        int new_dpi_value = dpi_values[current_dpi_index];

        // Call the configuration function with the new DPI value
        pmw3360_config(new_dpi_value);
    }

    buttons = next_buttons;
}


uint8_t wheel_state_a = 0;
uint8_t wheel_state_b = 0;
uint8_t wheel_state_output = 0;
int8_t wheel_progress = 0;

void update_wheel()
{
    uint8_t wheel_new_a = digitalRead(ENCODER_A);
    uint8_t wheel_new_b = digitalRead(ENCODER_B);
    
    if (wheel_new_a != wheel_state_a || wheel_new_b != wheel_state_b)
    {
        if (wheel_new_a == wheel_new_b && wheel_state_output != wheel_new_a)
        {
            // when scrolling up, B changes first. when scrolling down, A changes first
            if (wheel_new_b == wheel_state_b)
                wheel_progress += 1;
            // the wheel can glitch and jump straight from 00 to 11 (or vice versa)
            // so we need to check that only one state has changed since the last test
            else if(wheel_new_a == wheel_state_a)
                wheel_progress -= 1;
            
            wheel_state_output = wheel_new_a;
        }
        
        wheel_state_a = wheel_new_a;
        wheel_state_b = wheel_new_b;
    }
}


unsigned long previousMillis = 0; // stores the last time LEDs were updated
const long interval = 30;         // interval at which to update LEDs (milliseconds)

uint16_t j = 0;


void rgb_select(int rgb_selector) {
  switch (rgb_modes[rgb_selector])
  {
  case 0:
    rgb_off();
    break;        
  case 1:
    strip.setBrightness(GLOBAL_BRIGHTNESS);
    static_color();
    break;
  case 2:
    strip.setBrightness(GLOBAL_BRIGHTNESS);
    rainbow();
    break;
  case 3:
    strip.setBrightness(GLOBAL_BRIGHTNESS);
    police();
    break;
  case 4:
    breathing();
    break;
  }
}

void rgb_off() {
  for (int i = 0; i < strip.numPixels(); i++) {
	  strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();
}

void static_color() {
  for (int i = 0; i < strip.numPixels(); i++) {
	strip.setPixelColor(i, 217, 217, 0);
  }
  strip.show();
}

void rainbow() {
  uint16_t i;

  for(i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, RainbowWheel((i * 1 + j) & 255));
  }
  strip.show();

  j++;
  if (j >= 256) {
    j = 0;
  }
}

uint32_t RainbowWheel(byte WheelPos) {
  if(WheelPos < 85) {
    return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } 
  else if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } 
  else {
    WheelPos -= 170;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

uint16_t police_flag = 0;
static uint32_t blink_time = 0;
static const uint32_t BLINK_THRESHOLD = 500;

void police() {
  if((millis() - blink_time >= BLINK_THRESHOLD) && (police_flag == 0)) {
    blink_time = millis();
    strip.setPixelColor(0, 255, 0, 0);
    strip.setPixelColor(1, 0, 0, 255);
    police_flag=(police_flag + 1) % 2;
  }
  else if((millis() - blink_time >= BLINK_THRESHOLD) && (police_flag == 1)) {
    blink_time = millis();
    strip.setPixelColor(0, 0, 0, 255);
    strip.setPixelColor(1, 255, 0, 0);
    police_flag= (police_flag + 1) % 2;
  }
  strip.show();
}

uint32_t colors[] = {
  strip.Color(255, 0, 0),
  strip.Color(0, 255, 0),
  strip.Color(0, 0, 255),
  strip.Color(255, 255, 0),
  strip.Color(0, 255, 255),
  strip.Color(255, 0, 255)
};

int num_colors = sizeof(colors) / sizeof(colors[0]);
int currentColorIndex = 0;
int fade_brightness = 0;
int fadeAmount = 5;

void breathing() {
  strip.setPixelColor(0, colors[currentColorIndex]);
  strip.setPixelColor(1, colors[currentColorIndex]);
  strip.setBrightness(fade_brightness);
  strip.show();
  fade_brightness += fadeAmount;
  if (fade_brightness <= 0 || fade_brightness >= 255) {
    fadeAmount = -fadeAmount;
    if (fade_brightness <= 0) {
      currentColorIndex = (currentColorIndex + 1) % num_colors;
    }
  }
}

int n = 0;
int usb_hid_poll_interval = 1; 

struct MotionBurstData {
    uint8_t motion;
    uint8_t observation;
    int16_t x;
    int16_t y;
    uint8_t squal;
    uint8_t raw_sum;
    uint8_t raw_max;
    uint8_t raw_min;
    uint16_t shutter;
};

MotionBurstData spi_read_motion_burst(bool do_update_wheel);

void loop()
{
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      rgb_select(rgb_modes[rgb_selector]);
    }

    // these execute nearly instantly
    // we want to call update_wheel roughly every 250ms to avoid skipping
    update_wheel();
    delayMicroseconds(250);
    update_wheel();
    
    int16_t x = 0;
    int16_t y = 0;
    
    // takes ~400us to execute; wheel is updated again around 250ms into the call
    MotionBurstData data = spi_read_motion_burst(true);
    if (data.motion)
    {
        x = data.x;
        y = data.y;
    }
    
    update_wheel();
    update_buttons();
    
    int8_t wheel = wheel_progress;
    wheel_progress = 0;
    
    //uint32_t a = micros();
    // this will return around 1ms after the last time it returned
    // which should be around 250us from now
    mouse.update(x, y, buttons, wheel);
    //uint32_t b = micros();
    //Serial.println(b - a);
}

void pmw3360_boot()
{
    spi_write(REG_POWER_UP_RESET, 0x5A);
    delay(50);
    
    spi_read(0x02);
    spi_read(0x03);
    spi_read(0x04);
    spi_read(0x05);
    spi_read(0x06);
    
    srom_upload();
}

void pmw3360_config(int dpi_value)
{
    spi_write(REG_CONFIG1, dpi_value); // 1200 dpi
    
    // 3mm liftoff (2mm is bad for 3d printed case tolerances)
    // FIXME: make configurable
    //spi_write(REG_LIFT_CONFIG, 3);
}

void spi_begin()
{
    SPI.beginTransaction(spisettings);
}
void spi_end()
{
    SPI.endTransaction();
}

void spi_write(byte addr, byte data)
{
    spi_begin();
    
    digitalWrite(PIN_NCS, LOW);
    delayMicroseconds(1); // 120 nanoseconds; t_NCS-SCLK
    
    SPI.transfer(addr | 0x80);
    SPI.transfer(data);
    
    delayMicroseconds(35); // t_SCLK-NCS(write)
    digitalWrite(PIN_NCS, HIGH);
    
    spi_end();
    
    delayMicroseconds(180); // max(t_SWW, t_SWR)
}

byte spi_read(byte addr)
{
    spi_begin();
    
    digitalWrite(PIN_NCS, LOW);
    delayMicroseconds(1); // 120 nanoseconds; t_NCS-SCLK
    
    SPI.transfer(addr & 0x7F);
    
    delayMicroseconds(160); // t_SRAD
    
    byte ret = SPI.transfer(0);
    
    delayMicroseconds(1); // 120 nanoseconds; t_SCLK-NCS(read)
    digitalWrite(PIN_NCS, HIGH);
    
    spi_end();
    
    delayMicroseconds(20); // max(t_SRW, t_SRR)
    
    return ret;
}

MotionBurstData spi_read_motion_burst(bool do_update_wheel)
{
    MotionBurstData ret = {0};
    
    // this takes around 260ms to execute; update scroll wheel again after calling it
    spi_write(REG_MOTION_BURST, 0x00);
    if (do_update_wheel)
        update_wheel();
    
    spi_begin();
    
    digitalWrite(PIN_NCS, LOW);
    delayMicroseconds(1); // 120 nanoseconds; t_NCS-SCLK
    
    SPI.transfer(REG_MOTION_BURST);
    
    delayMicroseconds(35); // t_SRAD_MOTBR
    
    ret.motion = SPI.transfer(0);
    ret.observation = SPI.transfer(0);
    ret.x = SPI.transfer(0);
    ret.x |= ((uint16_t)SPI.transfer(0)) << 8;
    ret.y = SPI.transfer(0);
    ret.y |= ((uint16_t)SPI.transfer(0)) << 8;
    ret.squal = SPI.transfer(0);
    // don't care about the rest; terminate
    digitalWrite(PIN_NCS, HIGH);
    delayMicroseconds(1); // t_BEXIT = 500ns; wait 1000ns (1us)
    
    /*
    ret.raw_sum = SPI.transfer(0);
    ret.raw_max = SPI.transfer(0);
    ret.raw_min = SPI.transfer(0);
    ret.shutter = SPI.transfer(0);
    ret.shutter |= ((uint16_t)SPI.transfer(0)) << 8;
    */
    
    spi_end();
    
    return ret;
}

void srom_upload()
{
    spi_write(REG_CONFIG2, 0x00);
    spi_write(REG_SROM_ENABLE, 0x1D);
    delay(10);
    
    spi_write(REG_SROM_ENABLE, 0x18);
    
    spi_begin();
    
    digitalWrite(PIN_NCS, LOW);
    delayMicroseconds(1);
    
    SPI.transfer(REG_SROM_LOAD_BURST | 0x80);
    delayMicroseconds(15);
    
    for(size_t i = 0; i < SROM_LENGTH; i += 1)
    {
        SPI.transfer(srom[i]);
        delayMicroseconds(15);
    }
    
    digitalWrite(PIN_NCS, HIGH);
    delayMicroseconds(1);
    
    spi_end();
    
    delayMicroseconds(200);
    
    byte id = spi_read(REG_SROM_ID);
    printf("\n");
    printf("srom id: ");
    printf("%d", id);
    printf("\n");
    
    spi_write(REG_CONFIG2, 0x00);
}
