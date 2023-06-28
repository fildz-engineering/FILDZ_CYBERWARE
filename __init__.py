# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)

################################################################################
# FILDZ CYBEROS CYBERWARE API
#
# All the hardware-related setup for the cyberware such as its name, id, mac, etc. Every cyberware has an integrated
# power button that is used for pairing. Additionally, every cyberware can come with one (or more) device such as a
# sensor, button, display, accelerometer, etc.

# TODO:
#  1. Cyberware status monitor e.g. "OK", "CONNECTING TO AP", "WRONG PASSWORD", etc.
#  2. As "ap_name" used to config the AP, make sure user chosen name is valid to use (length, special characters, etc).

import network
import ubinascii
from machine import unique_id, Pin, PWM
import fildz_cyberos as cyberos


class CYBERWARE:
    def __init__(self):
        self._fullname = 'OLED DISPLAY 0.96" 128x64 REV 1.0'
        self._type = 'DISPLAY'
        # self._fullname = 'GENERIC BUTTON REV 1.0'
        # self._type = 'BUTTON'
        self._id = ubinascii.hexlify(unique_id()[:3]).upper()  # ESP8266/ESP8285 returns e.g. b'\x0f\x88\x9a\x00'
        self._version = 'CYBERWARE_VERSION'
        self._status = 'CYBERWARE_STATUS'
        self._name = '%s-%s' % (self._type, self._id.decode())
        self._ap_name = None if cyberos.preferences['ap_name'] is None else cyberos.preferences['ap_name']
        self._ap_color = None if cyberos.preferences['ap_color'] is None else cyberos.preferences['ap_color']
        self._ap_color_code = None if cyberos.preferences['ap_color_code'] is None else cyberos.preferences['ap_color_code']
        self._mac_private = network.WLAN(network.STA_IF).config('mac')
        self._mac_private_str = ubinascii.hexlify(self._mac_private, ':').decode().upper()
        # We must use bytearray here instead of bytes.
        # See: https://github.com/micropython/micropython/issues/11357
        # self._mac_public = b'\x9e\x9c\x1f\x00\x00\x00'
        self._mac_public = bytearray(b'\x9e\x9c\x1f\x00\x00\x00')
        self._mac_public_str = '9E:9C:1F:00:00:00'

        # Cyberware devices and sensors go here.
        #
        # Integrated power button on pin 13.
        try:
            from fildz_button import Button
            self._power_button = Button(Pin(13, Pin.OUT))
        except ImportError:
            pass
            # print('\n"fildz_button" library is not installed.')

        # Integrated buzzer on pin 12.
        try:
            from fildz_buzzer import Buzzer
            self._buzzer = Buzzer(PWM(Pin(12), freq=100, duty=0))
        except ImportError:
            pass
            # print('\n"fildz_buzzer" library is not installed.')

        # Integrated WS2812 (NeoPixel) on pin 14.
        try:
            from fildz_neopixel import NeoPixel
            self._pixel = NeoPixel(Pin(14, Pin.OUT), 1)
            # Generate AP name and color code on fresh start.
            if self._ap_name is None:
                import random
                color = (
                    ('R', self._pixel.C_RED),
                    ('O', self._pixel.C_ORANGE),
                    ('Y', self._pixel.C_YELLOW),
                    ('G', self._pixel.C_GREEN),
                    ('A', self._pixel.C_AQUA),
                    ('B', self._pixel.C_BLUE),
                    ('P', self._pixel.C_PURPLE),
                    ('W', self._pixel.C_WHITE))
                c1 = color[random.getrandbits(3)]
                c2 = color[random.getrandbits(3)]
                c3 = color[random.getrandbits(3)]
                self._ap_color = (c1[1], c2[1], c3[1])
                cyberos.preferences['ap_color'] = self._ap_color
                self._ap_color_code = '%s%s%s' % (c1[0], c2[0], c3[0])
                cyberos.preferences['ap_color_code'] = self._ap_color_code
                self._ap_name = '%s-%s' % (self._name, self._ap_color_code)
                cyberos.preferences['ap_name'] = self._ap_name
                cyberos.settings.on_save_settings.set()
        except ImportError:
            pass
            # print('\n"fildz_neopixel" library is not installed.')

        cyberos.cyberwares[self._ap_name] = {'events': {}}

    ################################################################################
    # Properties
    #
    # Name e.g., "BUTTON-02AD9A".
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # AP name e.g., "BUTTON-02AD9A-YYG".
    @property
    def ap_name(self):
        return self._ap_name

    @ap_name.setter
    def ap_name(self, value):
        self._ap_name = value

    # AP color e.g., ((255, 255, 0), (255, 255, 0), (0, 255, 0))
    @property
    def ap_color(self):
        return self._ap_color

    # AP color code e.g., "YYG".
    @property
    def ap_color_code(self):
        return self._ap_color_code

    # Fullname displays the entire name of the cyberware e.g., "OLED DISPLAY 0.96” 128x64 REV 1.0".
    @property
    def fullname(self):
        return self._fullname

    # Defines the cyberware type e.g., "DISPLAY".
    @property
    def type(self):
        return self._type

    # Unique ID of the cyberware e.g., "OF889A".
    @property
    def id(self):
        return self._id

    # Version of the cyberware e.g., "2022.05.03".
    @property
    def version(self):
        return self._version

    # Display real-time status of the cyberware e.g., "OK", "PAIRING".
    # Status is displayed when the user is connected to cyberware via the web interface.
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    # Private MAC address e.g., "b'\x9c\x9c\x1f\xXX\xXX\xXX'".
    # This MAC address is set on the STA interface and is used for communication between paired cyberwares.
    @property
    def mac_private(self):
        return self._mac_private

    # Private MAC address as string e.g., "9C:9C:1F:XX:XX:XX".
    @property
    def mac_private_str(self):
        return self._mac_private_str

    # Public MAC address b'\x9e\x9c\x1f\x00\x00\x00'.
    # This MAC address is hardcoded to every cyberware and set on the AP interface.
    # It is used for just one thing - pairing.
    # When cyberware starts to send pairing requests, it is sending them to a public MAC address.
    @property
    def mac_public(self):
        return self._mac_public

    # Public MAC address as string "9E:9C:1F:00:00:00".
    @property
    def mac_public_str(self):
        return self._mac_public_str

    # Single power button that is integrated into every cyberware.
    # Primarily used for pairing and to enable/disable AP.
    @property
    def power_button(self):
        return self._power_button

    # Single buzzer that is integrated into every cyberware.
    # Primarily used to notify user when cyberware is powered on, on successful pairing etc.
    @property
    def buzzer(self):
        return self._buzzer

    # Single WS2812 that is integrated into every cyberware.
    # Primarily used to identify the module AP via blinking colors (ap_color_code).
    @property
    def pixel(self):
        return self._pixel
