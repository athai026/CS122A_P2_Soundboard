# tutorial used: https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython 
import time
import board
import busio
import lcd

import adafruit_mpr121

import pygame

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

def sense():
    for i in range(12):
        if mpr121[i].value:
            print("Input {} touched!".format(i))
            lcd.lcd_string("Input {} touched".format(i), lcd.LCD_LINE_1)
            lcd.lcd_string('', lcd.LCD_LINE_2)
    time.sleep(0.1)  

pressed = [False, False, False, False, False, False, False, False, False, False, False, False]
def gui_sense(soundboard, soundsList, sounds):
    global pressed
    for i in range(12):
        if mpr121[i].value:
            print("Input {} touched!".format(i+1))
            lcd.lcd_string("Sound {} touched".format(i+1), lcd.LCD_LINE_1)
            lcd.lcd_string('', lcd.LCD_LINE_2)
            if sounds[i]:
                if not pressed[i]:
                    pygame.mixer.Channel(i).play(sounds[i])
                    pressed[i] = True
        else:
            pressed[i] = False
