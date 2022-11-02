from gpiozero import Servo
from time import sleep

#You will get a warning about servo jitter. Ignore it.
servo = Servo(25)

#Here are some of the basic commands you can run.
# try:
#     while True:
#         servo.min()
#         sleep(0.5)
#         servo.mid()
#         sleep(0.5)
#         servo.max()
#         sleep(0.5)
# except KeyboardInterrupt:
#     print('')

#You can use decimals to control the servos
val = -1
try:
    while True:
        servo.value = val
        sleep(0.1)
        val = val + 0.1
        if val > 1:
            val = -1
except KeyboardInterrupt:
    print("Stop")