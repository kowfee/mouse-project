# mouse-diy
this project was inspired by https://github.com/wareya/DIY-Gaming-Mouse

!!!! ----- DO NOT CHANGE THE STRUCTURE OF THE FILES AND DIRECTORIES IN 'mouse-diy' ---- !!!!

!!!! ----- src/srom_3360_0x04.h should contain copyrighted material, so it is not included in this repository. 0x00 should be replaced with a correct sequence, available on the internet ---- !!!!
!!!! ----- it is firmware for the pmw3360 sensor. it will function without the firmware, however loses some of the functionality and precision ---- !!!!

[INSTALLATION]

- Windows: 
    - within the 'dist' folder run the "installer.exe"

- Linux: 
    - run the following commands from the 'mouse-diy' directory in the terminal:
        - chmod 744 bin/arduino-cli
        - chmod 744 dist/interface
        - bin/arduino-cli core install arduino:mbed_rp2040@4.1.5
        - sudo $HOME/.arduino15/packages/arduino/hardware/mbed_rp2040/4.1.5/post_install.sh
        - bin/arduino-cli config set library.enable_unsafe_install true
        - bin/arduino-cli lib install --zip-path files/Adafruit_NeoPixel-1.12.3.zip


[HOW TO USE]

- Windows:
    - run the 'interface.exe' within the 'dist' folder

- Linux:
    - from the 'mouse-diy' directory run the following command:
        - dist/interface

The user interface lets you choose how many DPI settings you want to save and the DPI for each setting. You can also adjust the RGB color for the static setting.


[UNINSTALL]

- Windows: 
    - run the following commands in CMD:
        - rmdir /s /q %USERPROFILE%\AppData\Local\Arduino15\packages\arduino\hardware\mbed_rp2040\
        - rmdir /s /q %USERPROFILE%\Documents\Arduino\libraries\Adafruit_NeoPixel\

- Linux:
    - run the following commands in the terminal:
        - rm -rf $HOME/.arduino15/packages/arduino/hardware/mbed_rp2040/
        - rm -rf $HOME/Arduino/libraries/Adafruit_Neopixel/


[LICENSE]
Adafruit NeoPixel is licensed under GNU Lesser General Public License https://github.com/adafruit/Adafruit_NeoPixel

Arduino CLI is licensed under GNU General Public License https://github.com/arduino/arduino-cli

relmouse_16.h is based on files from mbed OS, also licensed under the Apache License, version 2.0. https://github.com/arduino/ArduinoCore-mbed

The hardware design files ("PCB mit LED", "PCB_Fabrication_Files" "Fusion360-Base.f3z" and "Fusion360-Body.f3z") are licensed under the SolderpadLicense, version 2.1, as follows:
```
Copyright 2024 Pasty6969, klibandm, kowfee
SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

Licensed under the Solderpad Hardware License v 2.1 (the “License”); you may not use this file except in compliance with the License, or, at your option, the Apache License version 2.0. You may obtain a copy of the License at

https://solderpad.org/licenses/SHL-2.1/

Unless required by applicable law or agreed to in writing, any work distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
```

mouse-diy.ino as well as other file contents are licensed under MIT License
