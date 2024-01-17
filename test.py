'''
Created on Jan 28, 2012
@author: yati

Updated Jan 17, 2024
by FrederickCousins
'''
import pygame
import sys
from sevensegment import *

pygame.init()


if __name__ == '__main__':
    # ssdchars = [SevenSegmentChar(k, width=10) for k in sorted(SSD_CHAR_MAP.keys()) if SSD_CHAR_MAP[k]]
    line1 = SevenSegmentDisplay(800, 200, 'HELLO FrEd',
                                colour_on=(0xcc, 0, 0), colour_off=(40, 0, 0), char_width=20, segment_width=4)
    line2 = SevenSegmentDisplay(800, 200, 'ANd tHANk you Yati',
                                colour_on=(0xcc, 0, 0), colour_off=(40, 0, 0), char_width=20, segment_width=4)

    scr = pygame.display.set_mode((800, 200))
    scr.fill((0, 0, 0))

    scr.blit(line1.surface, (0, 0))
    scr.blit(line2.surface, (0, 100))

    pygame.display.flip()
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                sys.exit()
