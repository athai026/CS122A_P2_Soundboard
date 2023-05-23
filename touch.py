# tutorial used: https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython 
import time
import board
import busio
import lcd

import adafruit_mpr121

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
    time.sleep(0.25)  
