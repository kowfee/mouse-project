# mouse-diy

!!!! ----- DO NOT CHANGE THE STRUCTURE OF THE FILES AND DIRECTORIES IN 'mouse-diy' ---- !!!!

[Installation]:

- Windows: 
    - run "installer.exe"

- Linux: 
    - run the following commands from the 'mouse-diy' directory in the terminal:
        - bin/arduino-cli core install arduino:mbed_rp2040
        - sudo $HOME/.arduino15/packages/arduino/hardware/mbed_rp2040/4.1.5/- post_install.sh
        - bin/arduino-cli config set library.enable_unsafe_install true
        - bin/arduino-cli lib install --zip-path files/Adafruit_NeoPixel-1.12.3.zip

