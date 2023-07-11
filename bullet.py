import pygame as pg

from object import object

class bullet(pg.sprite.Sprite):

    # create bullet group
    _group = pg.sprite.Group()

    def __init__(self, img, coords:tuple, vel:float, direction:bool, show: bool = True, ) -> None:
        """The Bullet class deals with setting and working with bullet objects

        Args:
            coords (tuple): _description_
            vel (float): _description_
            direction (_type_): _description_
            show (bool, optional): _description_. Defaults to True.
        """ 
        pg.sprite.Sprite.__init__(self)
        self.show = show
        self.image = img
        
        self.velocity    = vel
        self.x           = coords[0]
        self.y           = coords[1]
        
        self.rect        = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction   = direction

    def update(self):
        """Overwrite pygame sprite object function to update bullet (move bullet to the correct direction)
        """

        # if   not  self.direction is 1 [True]  -> 0 * 2 - 1 = -1 
        # elif not  self.direction is 0 [False] -> 1 * 2 - 1 =  1
        self.rect.x += (((not self.direction) * 2) - 1) * self.velocity

    def draw(self, screen, scale=False):
        super().draw(screen, scale, (self.rect.x - (self.imgoffset[0] * self.scale) , self.rect.y - (self.imgoffset[1] * self.scale)))