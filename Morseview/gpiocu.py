import RPi.GPIO as GPIO

ALL_BOARD_PINS = [
                3, 5, 7, 11, 13, 15, 19, 21, 23, 29, 31, 33, 35,
                8, 10, 12, 16, 18, 22, 24, 26, 32, 36, 38, 40
        ]

GPIO.setmode(GPIO.BOARD)

for pin in ALL_BOARD_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

GPIO.cleanup()
quit()
