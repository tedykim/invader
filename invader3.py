''' invader.py game 구현 '''
# 각종 lib import
import sys
import pygame
from random import randint
from pygame.locals import Rect, QUIT, KEYDOWN, \
    K_LEFT, K_RIGHT, K_SPACE

pygame.init()
SURFACE = pygame.display.set_mode((600,600))
FPSCLOCK = pygame.time.Clock()

pygame.key.set_repeat(5,5) # pygame.key.set_repeat(delay, interval) mil sec


