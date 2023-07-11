import pygame as pg

from screen     import screen
from object     import object
from gameState  import gameState


def main():
    #initialize pygame
    pg.init()

    #setup game screen
    fscreen = screen( (1280,720), color=(205,200,0), caption="Funny Alibaba", fps=60)

    #game loop
    gs = gameState(fscreen)
    
    gs.state_manager(*object.getObjList())     # loop wrapper
    pg.quit()                      # kill pygame after exit

    # run_game(fscreen)

if __name__ == "__main__":
    main()
