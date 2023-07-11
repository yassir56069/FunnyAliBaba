import pygame as pg
import itertools
import math

from pathlib import Path

from object import object
from entity import entity, player
from screen import screen

def lazy_adder(**layers):
    p_layers = []

    for index, (image, (alpha, is_dynamic, scale)) in enumerate(layers.items()):
        p_layers.append(layer(image, True, 1 * index + 1, index, alpha=alpha, is_dynamic=is_dynamic, scale=scale))

    return p_layers

def usemode_FMBE(s:screen, *layers):
    layers_list = list(*layers)
    FMB = list(itertools.islice(layers_list, 3))
    eff = [i for i in layers_list if i not in FMB]
    p_layers = []

    for index, image in enumerate(FMB):
        p_layers.append(layer(image, True, 1 * index + 1, s, (index * 2)+ 1))

    for index, image in enumerate(eff):
        p_layers.append(layer(image, True, 1 * index + 1, s))
    
    return p_layers

def usemode_FMB(s:screen, *layers):
    """Mode of layer stacking that involves the layers being 

    Returns:
        _type_: _description_
    """
    layers_list = list(*layers)

    p_layers = []

    for index, image in enumerate(layers_list):
        p_layers.append(layer(image, True, 1 * index + 1, s, (index) + 1))

    return p_layers

def usemode_FMEBE(s:screen, *layers):
    layers_list = list(*layers)

    p_layers = []


    for index, image in enumerate(itertools.islice(layers_list, 3)):
        p_layers.append(layer(image, True, 1 * index + 1, s, index + 1))
        layers_list.pop()

    for index, image in enumerate(layers_list):
        p_layers.append(layer(image, True, 1 * index + 1))
    
    return p_layers

class layer(object):
    """The layer object attaches various properties to an image that will be used for it's arrangement into a scene.
        Images are not transformed into pygame objects on init by this class.
    
        Args:
            img (str): The image to convert [Path]
            drawspeed (int): the drawspeed of the image is how fast the image should glide when the target is moving
            imgsize(tuple): the size of the image
            title_index (int, optional): The arrangement for the imge of the layer, which can be-
                        0 : effect (Default value, this will be an effect layer)
                        1 : front  (this will be a front layer)
                        2 : middle (this will be a middle layer)
                        3 : back   (this will be a back layer)
    """

    def __init__(self, img:str, show:bool,  drawspeed:int, title_index:int = 0,  alpha:bool= True, is_dynamic=False, scale:tuple=None, imgsize:tuple = (1280, 720)) -> None:
        """The layer object attaches various properties to an image that will be used for it's arrangement into a scene.
        Images are not transformed into pygame objects on init by this class.
    
        Args:
            img (str): The image to convert [Path]
            drawspeed (int): the drawspeed of the image is how fast the image should glide when the target is moving
            show (int): whether to show the image or not
            title_index (int, optional): The arrangement for the imge of the layer, which can be-
                        0 : effect (Default value, this will be an effect layer)
                        1 : front  (this will be a front layer)
                        2 : effect 
                        3 : middle (this will be a middle layer)
                        4 : effect 
                        5 : back   (this will be a back layer)
            imgsize (tuple, optional): the size of the image being passed
        """

        super().__init__(img, alpha, show, size=imgsize)

        self.titles     = {
            0:'effect',
            1:'front',
            2:'effect',
            3:'middle',
            4:'effect',
            5:'back'
        }
        self.scale       = scale
        self.is_dynamic  = is_dynamic
        self.drawspeed   = drawspeed
        self.title_index = title_index
        self.x1          = self.rect.x
        self.full_img    = self.img


    def draw(self, screen:screen, coord=(0,0)):

        super().draw(screen, self.scale, coord=coord)


class scene():
    """The scene object acts as a compilation of pygame image objects layered together to create
        a full fledged and comprehensive background for the game screen. it features multiple modes
        of layering so that it can support different looks for the background, by default the mode 
        is set to 0, which is the FMBE mode (stands for front, middle, back, effect) of layering.

        Args:
            s (screen): The pygame screen object to display the scene.
            mode (int, optional): The mode of arrangement for the layers of the scene, which can be-
                        0 : FMBE (Default value, stands for front, middle, back, effect)
                        1 : FMB  (stands for front, middle, back, display discards effects)
    """
    def __init__(self, s:screen, mode, **layers) -> None:
        """The scene object acts as a compilation of pygame image objects layered together to create
        a full fledged and comprehensive background for the game screen. it features multiple modes
        of layering so that it can support different looks for the background, by default the mode 
        is set to 0, which is the FMBE mode (stands for front, middle, back, effect) of layering.

        Args:
            s (screen): The pygame screen object to display the scene.
            mode (int, optional): The mode of arrangement for the layers of the scene, which can be-
                        0 : FMBE (Default value, stands for front, middle, back, effect)
                        1 : FMB  (stands for front, middle, back, display discards effects)
        """
        func_path = {
            0 : usemode_FMBE,
            1 : usemode_FMB,
            2 : lazy_adder
        }

        self.mode     = mode
        self.p_layers = func_path[self.mode](**layers)

        self.screen_size = (s.HEIGHT, s.WIDTH)
        self.border      = s.WIDTH/2

        #assigns the individual images to class objects, pls clean
        for image in self.p_layers:

            print(f'image: {image.img}\ndrawspeed: {image.drawspeed}\ntitle_index: {image.title_index}')


            if image.title_index == 0:
                self.back = image

            elif image.title_index == 1:
                self.back = image

            elif image.title_index == 3:
                self.middle = image

            elif image.title_index == 5:
                self.front = image

    def dynamic_scene(self, screen, to_draw:layer):

        to_draw.draw(screen, coord=(to_draw.x1, to_draw.rect.y))
        to_draw.draw(screen, coord=(to_draw.x1 + screen.WIDTH, to_draw.rect.y))

    def static_scene(self, screen, to_draw:layer):

        to_draw.draw(screen, coord=(to_draw.x1, to_draw.rect.y))

    def draw_scene(self, screen:screen, p:player, *ents:entity) ->None:
        """Draws a scene to the specified screen,

        Args:
            screen (screen): the screen to draw to
            p (player): player object
            dynamic (bool, optional): whether to draw dynamically looped or static screen (dynamic is costly). Defaults to 0.
        """
        p.update_borders()

        self.back.draw(screen, coord=(self.back.x1, self.back.rect.y))

        if self.back.is_dynamic:
            self.back.draw(screen, coord=(self.back.x1 + screen.WIDTH, self.back.rect.y))

        p.borderMoveLayer(self.back.drawspeed, self.back.is_dynamic, self.back)

        if ents:
            p.borderMoveEnt(self.back.drawspeed, *ents)

            for e in ents:
                e.draw(screen, coord=(e.rect.x, e.rect.y))

        p.draw(screen, coord=(p.rect.x, p.rect.y))
