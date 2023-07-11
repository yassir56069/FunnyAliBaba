import pygame as pg

RED    = (255,  0,   0)
YELLOW = (255,  255, 0)
WHITE  = (255,  255, 255)


class screen:
    def __init__(self, size = (0,0), caption = "entity", color=(0,0,0), fps=60) -> None:
        """Initialize screen object to create a pygame screen object

        Args:
            width (int, optional): Set screen width. Defaults to 1000.
            height (int, optional): Set screen height. Defaults to 600.
            caption (str, optional): Set window caption. Defaults to "entity".
        """
        self.SIZE = self.WIDTH, self.HEIGHT = size
        self.CAPTION = caption
        self.COLOR = color
        self.fps = fps

        self.borderXl = 0
        self.borderXr = self.WIDTH / 2 + 100
        self.borderY  = self.HEIGHT - 140

        self.SCREEN = pg.display.set_mode(self.SIZE)
        pg.display.set_caption(self.CAPTION)
        self.clock = pg.time.Clock()
      
    def blit_Screen(self, log= False):
        """Blits the screen.

        Args:
            log (bool, optional): if true, the properties of the screen will be printed to console. Defaults to False.
        """
        if log:
            print(f"Screen Width: {self.WIDTH}\nScreen Height: {self.HEIGHT}\nScreen Caption: {self.CAPTION}\nScreen Color: {self.COLOR}\n")

        pg.display.flip()

    def half_Screen_coord(self) -> tuple:
        return (self.WIDTH / 2, self.HEIGHT/2)

    def draw_healthBar(self, health, x ,y):
        ratio = health / 100
        pg.draw.rect(self.SCREEN, WHITE, (x - 2,y - 3, 404, 36))
        pg.draw.rect(self.SCREEN, RED, (x,y, 400, 30))
        pg.draw.rect(self.SCREEN, YELLOW, (x,y, 400 * ratio, 30))

    def tick(self):
        self.clock.tick(self.fps)