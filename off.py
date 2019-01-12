import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

gpio_pin_number = 7
#Replace YOUR_CHOSEN_GPIO_NUMBER_HERE with the GPIO pin number you wish to use
#Make sure you know which rapsberry pi revision you are using first
#The line should look something like this e.g. "gpio_pin_number=7"

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#It's very important the pin is an input to avoid short-circuits
#The pull-up resistor means the pin is high by default

while True:
    GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
    # Use falling edge detection to see if pin is pulled
    # low to avoid repeated polling

    # Wait for 2 seconds. If the button is still being pressed (still low)
    # then shutdown.
    time.sleep(2)

    # Send command to system to shutdown
    if GPIO.input(gpio_pin_number) == 0:
        os.system("sudo shutdown -h now")
        GPIO.cleanup()
    # # If the button is high after the 1.5 second delay (not being held down),
    # # reboot instead
    # else:
    #     os.system("sudo reboot -h now")

