import pygame as pg
import itertools
import math, numpy

from pathlib import Path

from object import object
from entity import entity, player
from screen import screen

class PGimage():
        def __init__(self, img = "", alpha:bool= False, show:bool = True, coord=(0,0), imgsize= ( 1280 * 3, 720) ) -> None:
            self.img = []
            self.full_img = []
            self.show = show
            self.WIDTH  = imgsize[0]
            self.HEIGHT = imgsize[1]
            self.x  = coord[0]
            self.y  = coord[1]

            if img != "":
                for images in img:
                    if alpha:
                        self.img.append(pg.image.load(images).convert_alpha())
                    else:
                        self.img.append(pg.image.load(images).convert())

            for img in self.img:
                self.full_img.append(pg.transform.scale(img, imgsize).copy())

        def draw(self, screen:screen, scale:tuple = None, coord=(0,0)):
            """Draw the object on screen

            Args:
                screen (screen): The pygame screen to draw on
                scale (bool, optional): Whether to scale the object or not. Defaults to True.
                coord (tuple, optional): The initial coordinates of the object to draw. Defaults to (0,0).
            """
            for img in self.img:
                if scale:
                    img = pg.transform.scale(img, scale)

                if self.show:
                    screen.SCREEN.blit(img, coord)

class layer():
    def __init__(self, img=""):
        self.img = img

    def draw(self, screen:screen, coord = (0,0)):
        screen.SCREEN.blit(self.img, coord)


class mask(layer):
    _maskDict = dict()

    def __init__(self, img=""):
        super().__init__(img)

        self.mask_img = pg.mask.from_surface(self.img)

        
        self.mask_coord = (0,0)
        self.mask_rect = self.mask_img.get_rect(center=self.mask_coord)


        mask._maskDict[self] = False

    def update_mask_position(self, coord= (0,0)):
        """update the center coordinate of the mask so that it can be used for collisions accurately. (candidate for optimisation, set position once maybe..)

        Args:
            coord (tuple, optional): _description_. Defaults to (0,0).
        """
        for mask_obj, is_active in mask._maskDict.items():
            if mask_obj == self:
                is_active = True
            else:
                is_active = False 

        self.mask_rect.center = coord

    def draw(self, screen:screen, coord = (0,0)):
        screen.SCREEN.blit(self.mask_img.to_surface(unsetcolor=(0,0,0,0)), coord)

        for mask_obj, is_active in mask._maskDict.items():
            if mask_obj == self:
                is_active = True
            else:
                is_active = False 


        self.mask_rect.center = coord

    def get_mask_rect(self):
        return self.mask_rect

    def getMaskDict(): 
        """Returns a python list of all entity objects

        Returns:
            _type_: returns the entitylist, containing all entity objects
        """
        return mask._maskDict

    @property 
    def mask_img(self): return self._mask_img

    @mask_img.setter
    def mask_img(self, m:pg.mask.Mask): self._mask_img = m

class scene(PGimage):

    def __init__(self, screen:screen, img="", alpha: bool = True, show: bool = True, imgsize=( 1280 * 3, 720)) -> None:
        super().__init__(img, alpha, show, screen.SIZE, imgsize)



        self.imgsize     = imgsize
        self.screen      = screen
        self.imgtiles    = []
        self.masktiles   = []
        self.frame_index = 1
        self.x1  = 0
        self.steps = 0

    def genTiles(self, screen:screen, stepvalue:int, imgnum):
        self.steps += stepvalue
        slice = self.imgsize[0] / stepvalue
        for steps in range(stepvalue):

            temp_img = layer(pg.transform.scale(self.full_img[imgnum].subsurface(
                steps * slice,
                0,
                slice, self.imgsize[1]
            ), screen.SIZE))

            self.imgtiles.append(temp_img)

    def addMaskTiles(self, screen:screen,  masks:list, stepvalue, masksize):
        slice =  masksize[0] / stepvalue
        mask_img = []

        for imgnum in range(len(masks)):
            img = pg.image.load(masks[imgnum]).convert()
            mask_img.append( pg.transform.scale(img, masksize))

        for images in mask_img:
            for steps in range(stepvalue):
                temp_mask = images

                temp_mask.set_colorkey((0,0,0))

                temp_mask = mask(pg.transform.scale(images.subsurface(
                steps * slice,
                0,
                slice, masksize[1]
                 ), screen.SIZE))
            

                self.masktiles.append(temp_mask)

    def drawbg(self, screen:screen, p:player, *ents:entity):
        p.update_borders()

        p.borderMoveLayerindx(p.speed, self)

        self.imgtiles[self.frame_index].draw(screen, coord=(self.x1, 0))
        self.masktiles[self.frame_index].update_mask_position(coord=(self.x1, -20))

        if  self.frame_index + 1 > len(self.imgtiles) - 1:
            self.frame_index = 1
            
        elif self.frame_index - 1 < 0:
            self.frame_index = self.steps - 2


        self.imgtiles[self.frame_index + 1].draw(screen, coord=(self.x1 + screen.WIDTH, 0))
        self.masktiles[self.frame_index + 1].update_mask_position(coord=(self.x1, -20))

        self.imgtiles[self.frame_index - 1].draw(screen, coord=(self.x1 - screen.WIDTH, 0))
        self.masktiles[self.frame_index - 1].update_mask_position(coord=(self.x1, -20))


        if p.rx > 1280:
            p.rx -= 1280
            self.x1 += screen.WIDTH
            self.frame_index += 1

        elif p.lx > 1280:
            p.lx -= 1280
            self.x1 -= screen.WIDTH
            self.frame_index -= 1

        if ents:
            p.borderMoveEnt(p.speed, *ents)

            for e in ents:
                e.draw(screen, coord=(e.rect.x, e.rect.y))


        p.draw(screen, coord=(p.rect.x, p.rect.y))

