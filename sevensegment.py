'''
Created on Jan 28, 2012
@author: yati

Forked Jan 17, 2024
by FrederickCousins
'''
import pygame
import pygame.gfxdraw
from functools import reduce
pygame.init()

          #  _____________
A = 0x01  # |  |___A___|  |
B = 0x02  # | F|       |B |
C = 0x04  # |__|_______|__|
D = 0x08  # |__|___G___|__|
E = 0x10  # |  |       |  |
F = 0x20  # | E|_______|C |
G = 0x40  # |__|___D___|__|


def on_segments(*args):
    '''
    takes the segment codes of segments that must be ON, and returns an
    appropriate int by logically ORing all the supplied codes
    '''
    return reduce(lambda x, y: (x | y), args, 0)


ALL = on_segments(A, B, C, D, E, F, G)

# Sometimes, it is nicer to specify which segments should be off.
def off_segments(*args):
    '''
    takes the segments that are to remain off, and returns an appropriate value
    '''
    return (ALL & (~ on_segments(*args)))


# This map could as well have used sets, but I decided to stick to bit twiddling.
SSD_CHAR_MAP = {
    '0': on_segments(A, B, C, D, E, F),
    '1': on_segments(B, C),
    '2': on_segments(A, B, D, E, G),
    '3': on_segments(A, B, C, D, G),
    '4': on_segments(B, C, G, F),
    '5': on_segments(A, C, D, F, G),
    '6': on_segments(A, C, D, E, F, G),
    '7': on_segments(A, B, C),
    '8': on_segments(A, B, C, D, E, F, G),
    '9': on_segments(A, B, C, D, F, G),

    # SPACE
    ' ': off_segments(A, B, C, D, E, F, G),

    'A': off_segments(D),
    'B': off_segments(A, B),
    'C': on_segments(A, D, E, F),
    'D': off_segments(A, F),
    'E': off_segments(B, C),
    'F': off_segments(B, C, D),
    'G': off_segments(B, G),
    'H': off_segments(A, B, D),
    'I': on_segments(B, C),
    'J': off_segments(A, F, G),
    # K looks like a capital H, but that's the best we can do with
    # an SSD.
    'K': off_segments(A, D),
    'L': on_segments(D, E, F),
    # write two Ns if you need an M.
    'N': off_segments(D, G),
    'O': off_segments(A, B, F),
    'P': off_segments(C, D),
    'Q': off_segments(D, E),
    'R': on_segments(E, G),
    'S': off_segments(B, E),
    'T': off_segments(A, B, C),
    'U': off_segments(A, G),
    'V': on_segments(C, D, E),  # Actually looks like a u.
    # W: use two Vs
    # No X
    'Y': off_segments(A, E),
    'Z': off_segments(C, F),
}

# Add the keys for lowercase characters
for key in list(SSD_CHAR_MAP.keys()):
    if key.lower() != key:
        SSD_CHAR_MAP[key.lower()] = SSD_CHAR_MAP[key]


class SevenSegmentChar(object):

    def __init__(self,
                 char,
                 colour_on=(255, 0, 0),
                 colour_off=(10, 0, 0),
                 bgcolour=(0, 0, 0),
                 width=20,
                 height=80,
                 segment_width=6,
                 segment_padding=2,
                 frame_width=2):
        '''
        ctor;
        takes the following args:
        char: The char to represent. This value must be a key in SSD_CHAR_MAP.
        colour_on: (R,G,B) colour tuple - default red.
        colour_off: (R,G,B) colour tuple - default dark red.
        bgcolour: (R,G,B) triple for the background of this char - default black.
        width: width of this character in pixels - default is 20px.
        height: height of this character in pixels - default is 80px.
        segment_width: the width of each segement in the char - default is 6px.
        segment_padding: the space between each segment - default is 2px.
        frame_width: the width of the space between the character and the edge of the surface - default is 2px
        '''
        assert char in SSD_CHAR_MAP
        self._char = char
        self._width = width
        self._colour_on = colour_on
        self._colour_off = colour_off
        self._bgcolour = bgcolour
        self._segment_width = segment_width
        self._frame_width = frame_width
        self._segment_length = self._width - self._segment_width - 2 * self._frame_width
        self._segment_padding = segment_padding
        self._height = 2 * self._segment_length + \
            self._segment_width + 2 * self._frame_width
        self._surface = pygame.Surface((self._width, self._height))
        self._surface.fill(bgcolour)
        self.draw_ssd_segments()

    def _get_segment_points(self):
        '''
        returns an iterable of (on/off, point pair)s which denote the start and end points
        of each segment, in order from A to G.
        '''
        s_len = self._segment_length
        s_wid = self._segment_width
        s_pad = self._segment_padding / 2
        f_pad = self._frame_width

        x0 = f_pad
        x1 = x0 + 0.5 * s_wid
        x2 = x0 + s_wid

        x3 = x0 + s_len
        x4 = x1 + s_len
        x5 = x2 + s_len
        assert x5 + f_pad == self._width

        y0 = f_pad
        y1 = y0 + 0.5 * s_wid
        y2 = y0 + s_wid

        y3 = y0 + s_len
        y4 = y1 + s_len
        y5 = y2 + s_len

        y6 = y3 + s_len
        y7 = y4 + s_len
        y8 = y5 + s_len
        assert y8 + f_pad == self._height

        positions = {
            A: ((x1 + s_pad, y1),
                (x2 + s_pad, y0),
                (x3 - s_pad, y0),
                (x4 - s_pad, y1),
                (x3 - s_pad, y2),
                (x2 + s_pad, y2)),

            B: ((x4, y1 + s_pad),
                (x5, y2 + s_pad),
                (x5, y3 - s_pad),
                (x4, y4 - s_pad),
                (x3, y3 - s_pad),
                (x3, y2 + s_pad)),

            C: ((x4, y4 + s_pad),
                (x5, y5 + s_pad),
                (x5, y6 - s_pad),
                (x4, y7 - s_pad),
                (x3, y6 - s_pad),
                (x3, y5 + s_pad)),

            D: ((x1 + s_pad, y7),
                (x2 + s_pad, y6),
                (x3 - s_pad, y6),
                (x4 - s_pad, y7),
                (x3 - s_pad, y8),
                (x2 + s_pad, y8)),

            E: ((x1, y4 + s_pad),
                (x2, y5 + s_pad),
                (x2, y6 - s_pad),
                (x1, y7 - s_pad),
                (x0, y6 - s_pad),
                (x0, y5 + s_pad)),

            F: ((x1, y1 + s_pad),
                (x2, y2 + s_pad),
                (x2, y3 - s_pad),
                (x1, y4 - s_pad),
                (x0, y3 - s_pad),
                (x0, y2 + s_pad)),

            G: ((x1 + s_pad, y4),
                (x2 + s_pad, y3),
                (x3 - s_pad, y3),
                (x4 - s_pad, y4),
                (x3 - s_pad, y5),
                (x2 + s_pad, y5)), }

        ssd = SSD_CHAR_MAP[self._char]
        ret = []

        for segment in (A, B, C, D, E, F, G):
            if segment & ssd:
                ret.append((1, positions[segment]))
            else:
                ret.append((0, positions[segment]))

        return ret

    def update(self):
        self._segment_length = self._width - 2 * self._segment_width
        self._surface.fill(self._bgcolour)
        self.draw_ssd_segments()

    def draw_ssd_segments(self):
        segment_polygon_points = self._get_segment_points()
        for segment_points in segment_polygon_points:
            if segment_points[0]:
                pygame.draw.polygon(surface=self._surface,
                                    color=self._colour_on,
                                    points=segment_points[1])
                pygame.draw.aalines(surface=self._surface,
                                    color=self._colour_on,
                                    closed=True,
                                    points=segment_points[1])
            else:
                pygame.draw.polygon(surface=self._surface,
                                    color=self._colour_off,
                                    points=segment_points[1])
                pygame.draw.aalines(surface=self._surface,
                                    color=self._colour_off,
                                    closed=True,
                                    points=segment_points[1])

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, new):
        self._surface = new
        self.update()

    @property
    def bgcolour(self):
        return self._bgcolour

    @bgcolour.setter
    def bgcolour(self, new):
        self._bgcolour = new
        self.update()

    @property
    def colour_on(self):
        return self._colour_on

    @colour_on.setter
    def colour_on(self, new):
        self._colour_on = new
        self.update()

    @property
    def colour_off(self):
        return self._colour_off

    @colour_off.setter
    def colour_off(self, new):
        self._colour_off = new
        self.update()

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, new):
        assert new in SSD_CHAR_MAP
        self._char = new
        self.update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new):
        self._width = new
        self.update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new):
        self._height = new
        self.update()

    @property
    def segment_width(self):
        return self._segment_width

    @segment_width.setter
    def segment_width(self, new):
        self._segment_width = new
        self.update()

    @property
    def segment_padding(self):
        return self._segment_padding

    @segment_padding.setter
    def segment_padding(self, new):
        self._segment_padding = new
        self.update()

    @property
    def frame_width(self):
        return self._frame_width

    @frame_width.setter
    def frame_width(self, new):
        self._frame_width = new
        self.update()


class SevenSegmentDisplay(list):
    '''
    The main display class - acts a a container for SevenSegmentChar objects.
    '''

    def __init__(self,
                 width,
                 height,
                 content='',
                 colour_on=(255, 0, 0),  # red
                 colour_off=(40, 0, 0),  # dark red
                 bgcolour=(0, 0, 0),  # black
                 segment_width=2,
                 segment_padding=6,
                 frame_width=2,
                 char_width=None,
                 right_justify=True):
        '''
        ctor for SevenSegmentDisplay. 
        Args:
            width: width of this panel.
            height: height of this panel.
            content: a string representing the content of the panel.
            colour_on: colour of the lit up segments. default red.
            colour_off: colour of the off segments. default dark red.
            bgcolour: background of the display. default black.
            segment_width: width of a segment in pixels. default 2px.
            char_width: width of each character - If not given, this value is
                calculated from `width` and len(content). If given, this width is
                used even if space in the panel is unused.

            right_justify: If this is True(default), the content is displayed right
                justified, as in traditional SSD displays. Otherwise, content is
                displayed left justified(surprise!!)
        '''
        self._width = width
        self._height = height
        self._content = content
        self._colour_on = colour_on
        self._colour_off = colour_off
        self._bgcolour = bgcolour
        self._segment_width = segment_width
        self._segment_padding = segment_padding
        self._frame_width = frame_width
        self._right_justified = right_justify

        if char_width:
            self._char_width = char_width
        else:
            if not content:
                raise ValueError('Empty content and no char_width')

            self._char_width = int(self._width / len(self._content))

        self._surface = pygame.Surface((self._width, self._height))
        self._numchars = int(self._width / self._char_width)
        self.update()

    def update(self):
        self[:] = []
        self._numchars = int(self._width / self._char_width)
        for c in self._content:
            self.append(SevenSegmentChar(c,
                                         self._colour_on,
                                         self._colour_off,
                                         self._bgcolour,
                                         self._char_width,
                                         self._height,
                                         self._segment_width,
                                         self._segment_padding,
                                         self._frame_width))
        self.update_surface()

    def update_surface(self):
        rect = pygame.Rect(0, 0, self._char_width, self._height)
        if self._right_justified:
            deficit = self._numchars - len(self._content)
            rect.move(deficit * self._char_width, 0)

        for ssdchar in self[-self._numchars:]:
            self._surface.blit(ssdchar.surface, rect)
            rect = rect.move(self._char_width, 0)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new):
        self._width = new
        self._surface = pygame.Surface(self._width, self._height)
        self.update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new):
        self._height = new
        self._surface = pygame.Surface(self._width, self._height)
        self.update()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new):
        self._content = new[-self._numchars:]
        self.update()

    @property
    def colour_on(self):
        return self._colour_on

    @colour_on.setter
    def colour_on(self, new):
        self._colour_on = new
        for ssdchar in self:
            ssdchar.colour_on = new
        self.update_surface()

    @property
    def colour_off(self):
        return self._colour_off

    @colour_off.setter
    def colour_off(self, new):
        self._colour_off = new
        for ssdchar in self:
            ssdchar.colour_off = new
        self.update_surface()

    @property
    def bgcolour(self):
        return self._bgcolour

    @bgcolour.setter
    def bgcolour(self, new):
        self._bgcolour = new
        for ssdchar in self:
            ssdchar.bgcolour = new
        self.update_surface()

    @property
    def segment_width(self):
        return self._segment_width

    @segment_width.setter
    def segment_width(self, new):
        self._segment_width = new
        for ssdchar in self:
            ssdchar.segment_width = new
        self.update_surface()

    @property
    def segment_padding(self):
        return self._segment_padding

    @segment_padding.setter
    def segment_padding(self, new):
        self._segment_padding = new
        for ssdchar in self:
            ssdchar.segment_padding = new
        self.update_surface()

    @property
    def frame_width(self):
        return self._frame_width

    @frame_width.setter
    def frame_width(self, new):
        self._frame_width = new
        for ssdchar in self:
            ssdchar.frame_width = new
        self.update_surface()

    @property
    def char_width(self):
        return self._char_width

    @char_width.setter
    def char_width(self, new):
        self._char_width = new
        self.update()

    @property
    def right_justified(self):
        return self._right_justified

    @right_justified.setter
    def right_justified(self, new):
        self._right_justified = new
        self.update()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, new):
        self._surface = new
        self._width = new.get_width()
        self._height = new.get_height()
        self.update()
