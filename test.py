#! .venv/bin/python

"""
Created on Jan 28, 2012
@author: yati

Forked Jan 17, 2024
by FrederickCousins
"""
import pygame
import sys
from sevensegment import *

pygame.init()


if __name__ == "__main__":
    line1 = SevenSegmentDisplay("HELLO FRED", 80, 1600, right_justify=False)
    line2 = SevenSegmentDisplay("ANd tHANk YOU Yati", 80, 1600, right_justify=False)
    line3 = SevenSegmentDisplay("0123456789 abcdef", 40, 1600, right_justify=False)

    scr = pygame.display.set_mode((1600, 400))
    scr.fill((0, 0, 0))

    scr.blit(line1.surface, (0, 0))
    scr.blit(line2.surface, (0, 150))
    scr.blit(line3.surface, (0, 300))
    print("Allowed characters:", ''.join(SSD_CHAR_MAP.keys()))

    pygame.display.flip()
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                sys.exit()
