import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader= SimpleMFRC522()

try:
    text = input('New data: ')
    print('now place your tag to write')
    reader.write(text)
    print('written')
    print('\n')

    print('place tag to read')
    id, text = reader.read()
    print('read')
    print(id)
    print(text)
finally: 
    GPIO.cleanup()