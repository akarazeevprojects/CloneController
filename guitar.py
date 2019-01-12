import RPi.GPIO as GPIO
import copy
import time

GPIO.setmode(GPIO.BCM)
NULL_CHAR = chr(0)


def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


def press_key(usage_id):
    report = NULL_CHAR * 2 + chr(usage_id) + NULL_CHAR * 5

    write_report(report)


def press_keys(usage_ids):
    report = NULL_CHAR * 2
    for usage_id in usage_ids:
        report += chr(usage_id)
    report += NULL_CHAR * (6 - len(usage_ids))

    write_report(report)


def release_keys():
    write_report(NULL_CHAR * 8)


buttons = {
    'button1': 14,
    'button2': 15,
    'button3': 18,
    'button4': 23,
    'button5': 24,
    'buttonup': 25,
    'buttondown': 8,
    'buttonp': 7
}

usage_id_mapping = {
    'button1': 30,
    'button2': 31,
    'button3': 32,
    'button4': 33,
    'button5': 34,
    'buttonup': 82,
    'buttondown': 81,
    'buttonp': 19
}

for pin in buttons.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    states = dict()

    for button in buttons:
        states[button] = True

    states_prev = copy.deepcopy(states)
    while True:
        for button, pin in buttons.items():
            states[button] = GPIO.input(pin)

        to_press = list()

        for button, state in states.items():
            if state == False:
                to_press.append(usage_id_mapping[button])

        if len(to_press) > 0:
            print(to_press)
            press_keys(to_press)
        else:
            release_keys()

        time.sleep(0.01)
        states_prev = copy.deepcopy(states)
except:
    GPIO.cleanup()
    release_keys()
    print('Exit')
