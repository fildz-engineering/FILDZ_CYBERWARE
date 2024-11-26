# FILDZ CYBERWARE API

This compact computer, known as [CYBERWARE](https://www.indiegogo.com/projects/cyberware-next-gen-wireless-prototyping-platform/coming_soon), is powered by the remarkable Wi-Fi microcontroller, [CYBERCORE X1](https://www.indiegogo.com/projects/cybercore-x1-a-tiny-wi-fi-module#/) that is based on ESP8285.

Moreover, CYBERCORE X1 runs CYBEROS - a custom build of MicroPython with its libraries and APIs that seamlessly handles wireless connections on the go!

We already have a few prototypes built:
* LED RGB (NeoPixel) module
* Button module
* Buzzer module
* OLED display module
* Stepper motor module

## Features

* Single PCB integrates MCU and sensor.
* All communications are wireless and done via ESP-NOW.
* Only two wires required - power and ground.
* On-board OS takes care of libraries and APIs.
* It's a modular, wireless solution that works straight out of the box.

## Setup

1. Download and extract .zip file contents to fildz_cyberware folder.
2. Upload fildz_cyberware folder to your MicroPython powered device.

## Requirements

1. FILDZ custom build of [MicroPython](https://github.com/fildz-engineering/FILDZ_CYBEROS_FIRMWARE).
2. Libraries [fildz_cyberos](https://github.com/fildz-engineering/FILDZ_CYBEROS), [fildz_button](https://github.com/fildz-engineering/FILDZ_CYBEROS_Button), [fildz_buzzer](https://github.com/fildz-engineering/FILDZ_CYBEROS_Buzzer) and [fildz_neopixel](https://github.com/fildz-engineering/FILDZ_CYBEROS_NeoPixel).
3. (Optional) APIs [fildz_button_api](https://github.com/fildz-engineering/FILDZ_CYBEROS_Button_API).

## Documentation

[CYBERWARE API Wiki](https://github.com/fildz-engineering/FILDZ_CYBERWARE/wiki)

## Contributing

FILDZ CYBEROS is an open-source project that thrives on community contributions. We welcome developers to contribute to the project by following the MIT license guidelines. Feel free to submit pull requests, report issues, or suggest enhancements to help us improve the project further.

## Acknowledgment 

We are immensely thankful to the [MicroPython](https://github.com/micropython/micropython) community for developing and maintaining this incredible open-source project. Their dedication and hard work have provided us with a powerful and versatile platform to build upon.
