# Getting Started

This is step by step installation method on how to install `microros` into `Ubuntu` and `ESP32`. Any other micrcontroller should work fine.

## Step 1: Install Arduino and Setup ESP32 package

If you're using Ubuntu, you can download `Arduino` directly from the Store.
Once done then we'll install `ESP32` package as follow

* In your Arduino IDE, go to File> Preferences
* Enter following into `Additional Board Manager URL`
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
* Open the Boards Manager. Go to Tools > Board > Boards Manager
* Search for ESP32 and press install button for the `ESP32 by Espressif Systems` and select `v2.0.2`
