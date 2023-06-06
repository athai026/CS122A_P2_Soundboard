# tutorial used: https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython 
import time
import board
import busio
import lcd
import button
from enum import Enum
import RPi.GPIO as GPIO

import adafruit_mpr121

import pygame

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# check-in
def sense():
    for i in range(12):
        if mpr121[i].value:
            print("Input {} touched!".format(i))
            lcd.lcd_string("Input {} touched".format(i), lcd.LCD_LINE_1)
            lcd.lcd_string('', lcd.LCD_LINE_2)
    time.sleep(0.1)  

# function called from gui
def gui_sense(sounds):
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

# turned into state machine
############################## TASK SCHEDULER CLASS ##############################
class task:
    def __init__(self, state, period, elapsedTime, func):
        self.state = state
        self.period = period
        self.elapsedTime = elapsedTime
        self.func = func
############################## TASK SCHEDULER CLASS ##############################

############################## GLOBAL VARIABLES ##############################
numTasks = 1
period_gcd = 0.01
############################## GLOBAL VARIABLES ##############################

############################# TOUCH TASK ##############################
class touchStates(Enum):
    startTouch = 1
    senseTouch = 2
    stopTouch = 3

touchState = Enum('touchStates', ['startTouch', 'senseTouch', 'stopTouch'])

pressed = [False, False, False, False, False, False, False, False, False, False, False, False]
sounds = []

def Touch(state):
    global pressed
    global sounds

    # transitions
    if state == touchState.startTouch:
        state = touchState.senseTouch
    elif state == touchState.senseTouch:
        if not GPIO.input(19):
            state = touchState.senseTouch
        elif GPIO.input(19):
            state = touchState.stopTouch
    elif state == touchState.stopTouch:
        state = touchState.stopTouch

    # state actions
    if state == touchState.senseTouch:
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

    
    return state

def main(incoming_sound):
    global numTasks
    global period_gcd
    global sounds

    sounds = incoming_sound

    # initializing task
    task1 = task(touchState.startTouch, period_gcd, 0, Touch)

    tasks = [task1]

    while True:
        for i in range(numTasks):
            if tasks[i].elapsedTime >= tasks[i].period:
                tasks[i].state = tasks[i].func(tasks[i].state)
            tasks[i].elapsedTime += period_gcd
        
        if task1.state == touchState.stopTouch: # if in stop state, stop running scheduler and return
            break
############################# TOUCH TASK ##############################