#!/usr/bin/env python3

import time
import datetime
from gpiozero import Button
from unicornhatmini import UnicornHATMini
from random import randrange
from signal import pause

# Settings
# Flash the colon between hour and minutes?
blinkDots = True

# Change brightness for day and night?
brightnessDaytime = 0.1
brightnessNightTime = 0.02
dayTimeStartHour = 8
dayTimeEndHour = 23
enableNightMode = True

# Change colour every hour or minute?
changeColourEveryMinute = False
changeColourEveryHour = True

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(brightnessDaytime)

red = 0
green = 0
blue = 0
dotson = True
previousMinute = -1
previousHour = -1
mode = 'time'

numbers = {
    "0": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [2, 1]],
    "1": [[0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [0, 6], [2, 6]],
    "2": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6]],
    "3": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [1, 3], [0, 3], [2, 4], [2, 5], [2, 6], [1, 6], [0, 6]],
    "4": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]],
    "5": [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 4], [2, 5], [2, 6], [1, 6], [0, 6]],
    "6": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3]],
    "7": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [1, 4], [1, 5], [1, 6]],
    "8": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3], [2, 2], [2, 1]],
    "9": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3], [2, 2], [2, 1]],
    ":": [[1, 2], [1, 4]],
    ".": [[1, 6]]
}

button_a = Button(5)
button_b = Button(6)
#button_x = Button(16)
#button_y = Button(24)


def enable_show_time():
    global mode
    mode = 'time'


def enable_show_date():
    global mode
    mode = 'date'
    time.sleep(5)
    enable_show_time()


def change_color():
    global red
    global green
    global blue
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)


button_a.when_pressed = enable_show_date
# button_a.when_released = enable_show_time
button_b.when_pressed = change_color


def letter(char, offset):
    for pixel in numbers[char]:
        x = pixel[0] + offset
        y = pixel[1]
        unicornhatmini.set_pixel(x, y, red, green, blue)


def show_time(now):
    global dotson
    unicornhatmini.clear()
    timestring = now.strftime("%H%M")
    letter(timestring[0], 0)
    letter(timestring[1], 4)
    if not blinkDots or dotson:
        letter(":", 7)
    letter(timestring[2], 10)
    letter(timestring[3], 14)
    unicornhatmini.show()


def show_date(now):
    unicornhatmini.clear()
    timestring = now.strftime("%d%m")
    letter(timestring[0], 0)
    letter(timestring[1], 4)
    letter(".", 7)
    letter(timestring[2], 10)
    letter(timestring[3], 14)
    unicornhatmini.show()


if not changeColourEveryMinute and not changeColourEveryHour:
    # Colour must be set at least once, else no lights
    change_color()


while True:
    now = datetime.datetime.now()

    # Time based brightness
    if enableNightMode and (now.hour < dayTimeStartHour or now.hour >= dayTimeEndHour):
        unicornhatmini.set_brightness(brightnessNightTime)
    else:
        unicornhatmini.set_brightness(brightnessDaytime)

    # Time based colour change
    if changeColourEveryMinute and (now.minute != previousMinute):
        change_color()
    if not changeColourEveryMinute and (changeColourEveryHour and (now.hour != previousHour)):
        change_color()

    if mode == 'time':
        show_time(now)

    if mode == 'date':
        show_date(now)

    dotson = not dotson
    previousMinute = now.minute
    previousHour = now.hour
    time.sleep(0.5)
