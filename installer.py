from sys import platform
import subprocess

if platform == "win32" or platform == "win64":
    subprocess.run(["../arduino-cli.exe", "core", "install", "arduino:mbed_rp2040"])
    subprocess.run(["../arduino-cli.exe", "config", "set", "library.enable_unsafe_install", "true"])
    subprocess.run(["../arduino-cli.exe", "lib", "install", "--zip-path", "../files/Adafruit_NeoPixel-1.12.3.zip"])
else: 
    print("System not supported")
