#reference: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
p = GPIO.PWM(26, 700) # piano and playback speaker
# p.start(70)
# time.sleep(0.2)
# p.stop()