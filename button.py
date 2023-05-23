import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button to read RFID
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button to write RFID