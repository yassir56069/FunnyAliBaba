import pygame as pg

from object import object
from entity import entity
from screen import screen


class layer():
    def __init__(self, img, drawspeed) -> None:
        self.img = img
        self.drawspeed = drawspeed

    def get_img(self):
        return self.img

    def get_speed(self):
        return self.drawspeed

class scene():

    def __init__(self, s:screen, *layers) -> None:
        
        if len(layers) < 3:
            raise UnboundLocalError("Not enough layers given.. object ommited")          
    
        self.layers = []

        for index, image in enumerate(layers):
            self.layers.append(layer(image, 1 * index + 1))

        # self.layers.append(layer(layers[0], 1))

        # self.layers.append(layer(layers[1], 1))
    
        # self.layers.append(layer(layers[0], 1))

        screen_size = (s.HEIGHT, s.WIDTH)

        self.border = s.WIDTH/2

        self.back   = object(self.layers[0].get_img(), size=screen_size)
        self.middle = object(self.layers[1].get_img(), size=screen_size)
        self.front  = object(self.layers[2].get_img(), size=screen_size)


    def draw_moving_scene(self, target:entity, screen:screen):
        if target.rect.x > self.border and target.action == 1:
            self.back.rect.x -= self.layers[0].get_speed()
            self.middle.rect.x -= self.layers[1].get_speed()
            self.front.rect.x -= self.layers[2].get_speed()

        if target.rect.x < self.border and (target.action ==  1 and target.charaFlip == 1):
            self.back.rect.x += self.layers[0].get_speed()
            self.middle.rect.x += self.layers[1].get_speed()
            self.front.rect.x += self.layers[2].get_speed()

        self.back.draw(screen, coord= (self.back.rect.x, self.back.rect.y))
        self.middle.draw(screen, coord= (self.middle.rect.x, self.middle.rect.y))
        target.draw(screen, coord= (target.rect.x, target.rect.y))
        self.front.draw(screen, coord= (self.front.rect.x, self.front.rect.y))

 

    def draw_scene(self, player:entity, screen:screen):

        self.back.draw(screen)
        self.middle.draw(screen)
        player.draw(screen)
        self.front.draw(screen)

        # for layer in self.layers:            
        #     layer.rect.x += self.dx
        #     layer.rect.y += self.dy