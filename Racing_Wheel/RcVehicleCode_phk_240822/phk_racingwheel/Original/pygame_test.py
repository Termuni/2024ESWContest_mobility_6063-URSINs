import pygame
import sys
import pygame.joystick
from gpiozero import Button

pygame.init()

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)

joystick.init()

i = 0

while i<500000000000:
    print("wheel : {}".format(joystick.get_axis(0)))    

