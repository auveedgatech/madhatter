import pygame

#Sends audio to headphone jack
pygame.mixer.init()
pygame.mixer.music.load("name.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue