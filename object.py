import pygame as pg
from screen import screen

class object:

    # Python List keeping track of all objects for execution and processing purposes
    _objList = []

    def __init__(self, img="", alpha:bool= True, show:bool = True, coord=(0,0), size= (80,180) ) -> None:
        """Subclass for pygame Objects. used for the game screen 

        Args:
            img (str, optional): The image of the pygame object. Defaults to "".
            show (bool, optional): Whether to show the pygame object or not. Defaults to True.
        """


        # Pos and display
        self.show = show
        self.x  = coord[0]
        self.y  = coord[1]
        self.ini_x = self.x 
        self.ini_y = self.y 
        self.WIDTH  = size[0]
        self.HEIGHT = size[1]


        self.rect = pg.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

        if img != "":
            if alpha:
                self.img = pg.image.load(img).convert_alpha()
            else:
                self.img = pg.image.load(img).convert()
        
        object._objList.append(self)

    def draw(self, screen:screen, scale:tuple = None, coord=(0,0)):
        """Draw the object on screen

        Args:
            screen (screen): The pygame screen to draw on
            scale (bool, optional): Whether to scale the object or not. Defaults to True.
            coord (tuple, optional): The initial coordinates of the object to draw. Defaults to (0,0).
        """
        if scale:
            self.img = pg.transform.scale(self.img, scale)

        if self.show:
            screen.SCREEN.blit(self.img, coord)

    def flip(self):
        """FLip the show value of the object
        """
        self.show = not self.show

    def hide(self):
        """Hide the object
        """
        self.show = False
    
    def show(self):
        """Show the object
        """
        self.show = True

    def getObjList(): 
        """Get the lit of all pygame objects

        Returns:
            _type_: list of objects
        """
        return object._objList

