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
    line1 = SevenSegmentDisplay(1600, 150, "HELLO FrEd",
                                colour_on=(0xcc, 0, 0), colour_off=(20, 0, 0), char_width=80, segment_width=15, segment_padding=8, frame_width=4, right_justify=False)
    line2 = SevenSegmentDisplay(1600, 150, "ANd tHANk you Yati",
                                colour_on=(0xcc, 0, 0), colour_off=(20, 0, 0), char_width=80, segment_width=15, segment_padding=8, frame_width=4, right_justify=False)
    line3 = SevenSegmentDisplay(1600, 150, "0123456789 abcdef",
                                colour_on=(0xcc, 0, 0), colour_off=(20, 0, 0), char_width=40, segment_width=8, segment_padding=4, frame_width=2, right_justify=False)

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
