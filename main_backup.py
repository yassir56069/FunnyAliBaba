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


from gameState import gameState



def run_game(screen:screen, running = True):

    class gameState():
        def __init__(self) -> None:
            self.states = {
                0: "gameLoop",
                1: "paused",
                2: "exiting",
                3: "menu"
            }

            self.state = self.states[0]

        def intro(self, *obj:object):
            while running:
                screen.tick()

                # create keyboard instance and catch key presses
                kb = control_dsg() 

                for event in pg.event.get():
                    if event.type == pg.QUIT: sys.exit()

                    kb.move(event, p1, kb.set_move_AD())
                    # kb.move(event, p2, kb.set_move_AK())

                sb.draw(screen)
    
                pg.display.update()


        def gameLoop(self, *obj:object):
            while running:
                screen.tick()

                # create keyboard instance and catch key presses
                kb = control_dsg() 

                for event in pg.event.get():
                    if event.type == pg.QUIT: sys.exit()

                    kb.move(event, p1, kb.set_move_AD())
                    # kb.move(event, p2, kb.set_move_AK())


                sb.draw(screen)
                #player handlingd
                bucket.spawnPC(p1, kb)
                # kb.borderCol(p1, )

                # npc handling
                bucket.spawnNPC(kb)

                bg2.drawbg(screen, p1, *entity.getNpcs())

                # bg.draw_scene(screen,  p1, *entity.getNpcs())
                kb.borderCol(p1)

                # debug
                u1.showFps(clock, screen.SCREEN) 
                # u1.showTextOnScreen((20, 30), screen.SCREEN, f'is past border: {str(p1.past_border)}')
                # u1.showTextOnScreen((20, 60), screen.SCREEN, f'is before border: {str(p1.befr_border)}')
                # u1.showTextOnScreen((20, 120), screen.SCREEN, f'o.rect.right + o.dx  {str(p1.rect.right + p1.dx) }| lx: {str(p1.x) }')
                u1.showTextOnScreen((20, 30), screen.SCREEN, f'Mask Coordinates: {str(p1.dx) }| y: {str(p1.y) }')
                # u1.showTextOnScreen((20, 110), screen.SCREEN, f'bg x1: {str(bg2.frame_index)}')


                # bullet handling
                bullet._group.update()
                bullet._group.draw(screen.SCREEN)
    
                pg.display.update()

    # objects
    p1    = player(config='assets//chara//fighter1.json',img='assets//images//warrior//Sprites//warrior.png', coord=(0,400)) 
    # p2    = entity(config='assets//chara//fighter2.json',img='assets//images//wizard//Sprites//wizard.png', coord=(100,400)) 
    # bg    = scene(screen, 2, **{'assets//images//background//dunelong.png': (True, False, (screen.WIDTH, screen.HEIGHT))}) #currently not working!
    sb    = object(img='assets//images//background//sky.png', alpha=False)
    bg2   = scene(screen, ['assets//images//background//dunelong.png', 'assets//images//background//dunelong2.png'],True, True, imgsize=(1280 * 2, 720))
    gs =    gameState()


    bg2.genTiles(screen, 8, 0)
    bg2.genTiles(screen, 8, 1)
    bg2.addMaskTiles(screen, ['assets//images//background//masks//dunemask.png'], 8, (1280, 720))

    # dev
    u1     = util()
    bucket = bucketSets(screen) 

    # init
    p1.GenImages(10,8,1,7,7,3,7)    
    # p2.GenImages(8,8,1,8,8,3,7)


    # p1.setScreenborder(screen, 2)


    clock = pg.time.Clock()
    npcs  = entity.getNpcs()

    gs.intro(*object.getObjList())     # loop wrapper
    pg.quit()                      # kill pygame after exit


def main():
    #initialize pygame
    pg.init()

    #setup game screen
    fscreen = screen( (1280,720), color=(205,200,0), caption="Funny Alibaba", fps=500)

    #game loop
    run_game(fscreen)

if __name__ == "__main__":
    main()
