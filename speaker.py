import pygame

#Sends audio to headphone jack
pygame.mixer.init()
pygame.mixer.music.load("name.wav")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(1.0)

while pygame.mixer.music.get_busy() == True:
    continue