# tutorial use: https://pimylifeup.com/raspberry-pi-rfid-rc522/ 
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import speaker
import lcd
import time

reader = SimpleMFRC522()

def write():
    lcd.lcd_string('Writing...', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)
    text = input('New data: ')
    print('now place your tag to write')
    reader.write(text)
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    print('written')
    lcd.lcd_string('Written:', lcd.LCD_LINE_1)
    lcd.lcd_string(text, lcd.LCD_LINE_2)

def read():
    lcd.lcd_string('Reading...', lcd.LCD_LINE_1)
    lcd.lcd_string('', lcd.LCD_LINE_2)
    print('place tag to read')
    id, text = reader.read()
    speaker.p.start(70)
    time.sleep(0.2)
    speaker.p.stop()
    print('read')
    print(id)
    print(text)
    lcd.lcd_string('Read:', lcd.LCD_LINE_1)
    lcd.lcd_string(text, lcd.LCD_LINE_2)
