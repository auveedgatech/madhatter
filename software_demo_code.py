import RPi.GPIO as GPIO
from time import sleep
from enum import Enum
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup States
class State(Enum):
    IDLE = 0
    
    #TESTS
    LED_TEST = 1
    AUDIO_TEST = 2
    MOTION_HAT_TEST = 3
    MOTION_TEACUPS_TEST = 4
    
    #DIRECTOR STATES
    CONNECT_TO_DIRECTOR = 5
    WAIT_FOR_INTRUCTION = 6
    DECODE_FILE = 7
    
# Setup Current State
current_state = State.IDLE

# Setup Interrupts
def reset_callback(channel):
    print("Resetting to Idle")
    current_state = State.IDLE
    
def led_test_callback(channel):
    print("Starting LED Test")
    current_state = State.LED_TEST


# Setup Pushbuttons

#Reset Button
pin_reset = 10
GPIO.setup(pin_reset, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_reset, GPIO.RISING, callback=reset_callback)

#LED Test Button
pin_led_test = 12
GPIO.setup(pin_led_test, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_led_test, GPIO.RISING, callback=led_test_callback)

# Setup External Components:
led_out = GPIO.LOW
led_output_port = 18
GPIO.setup(led_output_port, GPIO.OUT)
while True:
    print("PING", current_state)

    if current_state == State.IDLE:
        led_out = GPIO.LOW
        GPIO.output(led_output_port, led_out);

        sleep(0.1)
    elif current_state == State.LED_TEST:
        # Set LED High:
        print("LED INIT")
        led_out = GPIO.HIGH;
        GPIO.output(led_output_port, led_out);
        sleep(10)
        led_out = GPIO.LOW;
        GPIO.output(led_output_port, led_out);
        print("LED END")

        
        
    sleep(5)