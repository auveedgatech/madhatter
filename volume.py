import os, sys
import serial
import time
import string
import pygame


ser = serial.Serial('/dev/ttyACM1', 9600)

def parse_int(str):
    return int(str.strip(string.ascii_letters))


#Sends audio to headphone jack
# python -m serial.tools.miniterm
pygame.mixer.init()
pygame.mixer.music.load("name.wav")
pygame.mixer.music.play()

while True:
    line = ser.readline()
    if len(line) == 0:
        print("out")
    volume = parse_int(line.decode("utf-8"))
    print(volume)
    pygame.mixer.music.set_volume(volume/100)
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.load("name.wav")
        pygame.mixer.music.play()
        

