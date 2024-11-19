# mouse-diy

!!!! ----- DO NOT CHANGE THE STRUCTURE OF THE FILES AND DIRECTORIES IN 'mouse-diy' ---- !!!!

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