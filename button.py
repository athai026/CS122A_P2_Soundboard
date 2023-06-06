import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # GUI stop soundboard
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button to write RFID (save)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button to read RFID (load)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # remake soundboard
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # load local soundboard
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # save soundboard locally
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pause/resume spotify
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # play/restart spotify
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # search spotify
