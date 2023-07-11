import pygame as pg
import sys

from entity     import entity, player
from screen     import screen
from controls   import control_dsg
from object     import object
from bullet     import bullet

# from scene      import scene
from scene2     import scene, mask


from util       import util
from bucket     import bucketSets
# 



class gameState():
    def __init__(self, fscreen) -> None:
            
            self.states = {
                0: self.intro,
                1: self.gameLoop
            }

            self.state = 0 #start on intro


            # objects
            self.p1    = player(config='assets//chara//fighter1.json',img='assets//images//warrior//Sprites//warrior.png', coord=(0,400)) 
            # p2    = entity(config='assets//chara//fighter2.json',img='assets//images//wizard//Sprites//wizard.png', coord=(100,400)) 
            # bg    = scene(screen, 2, **{'assets//images//background//dunelong.png': (True, False, (screen.WIDTH, screen.HEIGHT))}) #currently not working!
            self.sb    = object(img='assets//images//background//sky.png', alpha=False)
            self.bg2   = scene(fscreen, ['assets//images//background//dunelong.png', 'assets//images//background//dunelong2.png'],True, True, imgsize=(1280 * 2, 720))


            self.bg2.genTiles(fscreen, 8, 0)
            self.bg2.genTiles(fscreen, 8, 1)
            self.bg2.addMaskTiles(fscreen, ['assets//images//background//masks//dunemask.png'], 8, (1280, 720))

            # dev
            self.u1     = util()
            self.bucket = bucketSets(fscreen) 

            # init
            self.p1.GenImages(10,8,1,7,7,3,7)    
            # p2.GenImages(8,8,1,8,8,3,7)

            # p1.setScreenborder(screen, 2)

            #text
            self.font = pg.font.SysFont("Arial", 40)

            self.disp      = fscreen
            self.clock     = pg.time.Clock()
            self.npcs      = entity.getNpcs()



    def state_manager(self, *obj:object):
        self.states[self.state](obj)
        
    def intro(self, running=True, *obj:object):
        """The Intro menu for the game. This is all coded in one function for clarity and simplicity in functionality.

        Args:
            running (bool, optional): _description_. Defaults to True.
        """
        while running:
            self.disp.tick()

            # create keyboard instance and catch key presses
            kb = control_dsg() 

            self.sb.draw(self.disp)
            textSurface = self.font.render("Start Game", 1, pg.Color('White'))
            button_rect = textSurface.get_rect(topleft=(100,100))

            for event in pg.event.get():
                if event.type == pg.QUIT: sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_rect.collidepoint(event.pos):
                            running = False
                            self.state = 1
                            self.state_manager(obj)


                # kb.move(event, self.p1, kb.set_move_AD())
                # kb.move(event, p2, kb.set_move_AK())


            self.disp.SCREEN.blit(textSurface, button_rect)

            pg.display.update()

    def reDraw(self):
        
            self.sb.draw(self.disp)
            #player handlingd
            self.bucket.spawnPC(self.p1, self.kb)
            # kb.borderCol(p1, )

            # npc handling
            self.bucket.spawnNPC(self.kb)

            self.bg2.drawbg(self.disp, self.p1, *entity.getNpcs())

            # bg.draw_scene(screen,  p1, *entity.getNpcs())

            # debug
            self.u1.showFps(self.clock, self.disp.SCREEN) 
            # u1.showTextOnScreen((20, 30), screen.SCREEN, f'is past border: {str(p1.past_border)}')
            # u1.showTextOnScreen((20, 60), screen.SCREEN, f'is before border: {str(p1.befr_border)}')
            # u1.showTextOnScreen((20, 120), screen.SCREEN, f'o.rect.right + o.dx  {str(p1.rect.right + p1.dx) }| lx: {str(p1.x) }')
            self.u1.showTextOnScreen((20, 30), self.disp.SCREEN, f'Mask Coordinates: {str(self.p1.dx) }| y: {str(self.p1.y) }')
            # u1.showTextOnScreen((20, 110), screen.SCREEN, f'bg x1: {str(bg2.frame_index)}')


            # bullet handling
            bullet._group.update()
            bullet._group.draw(self.disp.SCREEN)


    def gameLoop(self, running=True, *obj:object):
        while running:
            self.disp.tick()

            # create keyboard instance and catch key presses
            self.kb = control_dsg() 

            for event in pg.event.get():
                if event.type == pg.QUIT: sys.exit()

                self.kb.move(event, self.p1, self.kb.set_move_AD(), self)
                # kb.move(event, p2, kb.set_move_AK())

            self.sb.draw(self.disp)
            #player handlingd
            self.bucket.spawnPC(self.p1, self.kb)
            # kb.borderCol(p1, )

            # npc handling
            self.bucket.spawnNPC(self.kb)

            self.bg2.drawbg(self.disp, self.p1, *entity.getNpcs())

            # bg.draw_scene(screen,  p1, *entity.getNpcs())
            self.kb.borderCol(self.p1)

            # debug
            self.u1.showFps(self.clock, self.disp.SCREEN) 
            # u1.showTextOnScreen((20, 30), screen.SCREEN, f'is past border: {str(p1.past_border)}')
            # u1.showTextOnScreen((20, 60), screen.SCREEN, f'is before border: {str(p1.befr_border)}')
            # u1.showTextOnScreen((20, 120), screen.SCREEN, f'o.rect.right + o.dx  {str(p1.rect.right + p1.dx) }| lx: {str(p1.x) }')
            self.u1.showTextOnScreen((20, 30), self.disp.SCREEN, f'Mask Coordinates: {str(self.p1.dx) }| y: {str(self.p1.y) }')
            # u1.showTextOnScreen((20, 110), screen.SCREEN, f'bg x1: {str(bg2.frame_index)}')


            # bullet handling
            bullet._group.update()
            bullet._group.draw(self.disp.SCREEN)

            pg.display.update()
