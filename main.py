import touch
import rfid
import lcd
import speaker
import button
import RPi.GPIO as GPIO

def main():
    lcd.lcd_start()
    lcd.lcd_string('touch ready', lcd.LCD_LINE_1)

    while True:
        touch.sense()
        if GPIO.input(19):
            rfid.read()
        if GPIO.input(13):
            rfid.write()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_byte(0x01, lcd.LCD_CMD)
        lcd.lcd_string("Goodbye!", lcd.LCD_LINE_1)
        speaker.p.stop()