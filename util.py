import pygame as pg
import sys

from screen     import screen
from controls   import control_dsg
from object     import object
from entity    import entity
from bullet     import bullet
from scene      import scene

# This script is used as a utility module for the game, to add debugging features and dev tools
# please read up on each feature before using them

class util:
    """Utility class containing all utility functions for debugging and dev features.
    """
 
    def __init__(self, typeface='Arial', fontsize=18) -> None:
        """Initiliaze utility class to construct font variable and perform blits on dev screen

        Args:
            typface (str, optional): typeface to use for display. Defaults to 'Arial'.
            fontsize (int, optional): size of font to use for display. Defaults to 18.
        """
        self.font = pg.font.SysFont(typeface, fontsize)

    def showFps(self, clock:pg.time.Clock, screen) -> None:
        """Draws an fps counter to the top right of the screen

        Args:
            clock (clock): pygame.time.Clock object
            screen (pygame screen): game screen to blit the counter to, if not given will print to console
        """

        def update_fps():
            fps = str(int(clock.get_fps()))
            fps_text = self.font.render(fps, 1, pg.Color("coral"))
            return fps_text

        clock.tick()

        if screen:
            screen.blit(update_fps(), (10,0))
        else:
            print(clock.get_fps())

    def showTextOnScreen(self, coord:tuple, screen, content:str) -> None:
        """Generic function to put text on screen

        Args:
            coord (tuple): coordinates for where to display the contents
            screen (pygame screen): _description_
            content (str): string to display
        """
        to_blit = self.font.render(content, 1, pg.Color('yellow'))
        screen.blit(to_blit, coord)