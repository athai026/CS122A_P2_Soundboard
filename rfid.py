# tutorial use: https://pimylifeup.com/raspberry-pi-rfid-rc522/ 
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import speaker
import lcd
import time

reader = SimpleMFRC522()

def write(text):
    lcd.lcd_string('Place tag to', lcd.LCD_LINE_1)
    lcd.lcd_string('write', lcd.LCD_LINE_2)
    print('now place your tag to write')
    reader.write(text)
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    print('written')
    lcd.lcd_string('Tag Written', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)

def read():
    lcd.lcd_string('Place tag to', lcd.LCD_LINE_1)
    lcd.lcd_string('read', lcd.LCD_LINE_2)
    print('place tag to read')
    id, text = reader.read()
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    print('read')
    print(id)
    print(text)
    lcd.lcd_string('Tag Read', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)
    return text

def gui_write(soundboard):
    lcd.lcd_string('Place tag to', lcd.LCD_LINE_1)
    lcd.lcd_string('write', lcd.LCD_LINE_2)

    text = ''
    for i in range(12):
        if i < 11:
            text += soundboard[i] + ','
        else:
            text += soundboard[i]
    print(text)

    reader.write(text)
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    lcd.lcd_string('Tag Written', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)

def gui_read():
    lcd.lcd_string('Place tag to', lcd.LCD_LINE_1)
    lcd.lcd_string('read', lcd.LCD_LINE_2)
    print('place tag to read')
    id, text = reader.read()
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    print('read')
    print(id)
    print(text)
    lcd.lcd_string('Tag Read', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)

    soundboard = text.split(',')
    soundboard[11] = soundboard[11].strip()
    print(soundboard)
    return soundboard