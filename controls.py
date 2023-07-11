import pygame as pg


# use dictionaries instead of if statements, put keyboard inputs as values etc, should be easy to do.

from entity import entity
from bullet import bullet
from screen import screen
from scene2 import mask

def show(obj:entity):
    obj.flip()

def menu_click(pos, button_rect):
    if button_rect.collidepoint(pos):
        print("Button Pressed")

def move_left(obj:entity):
    """left movement for object

    Args:
        obj (entity): the object to apply the movement
    """
    obj.dx = -obj.speed
    obj.charaFlip = True
    obj.isMoving = True
    obj.hasVelocity = True

def move_right(obj:entity):
    """right movement for object

    Args:
        obj (entity): the object to apply the movement
    """
    obj.dx = obj.speed
    obj.charaFlip = False
    obj.isMoving = True
    obj.hasVelocity = True
 
def move_jump(obj:entity): 
    """jump movement for object

    Args:
        obj (entity): the object to apply the movement
    """
    if obj.jump == False:
        obj.jump = True
        obj.vel_y = -obj.jumpVal

def attk_light(obj:entity):
    """Light attack action for object

    Args:
        obj (entity): the object to apply the action
    """
    obj.isAttacking = True
    obj.attacking = pg.time.get_ticks()

def attk_medium(obj:entity):
    """medium attack action for object

    Args:
        obj (entity): the object to apply the action
    """
    obj.isAttacking = True
    obj.attacking = pg.time.get_ticks()

def attk_heavy(obj:entity):
    """heaavy attack action for object

    Args:
        obj (entity): the object to apply the action
    """
    obj.isAttacking = True
    obj.attacking = pg.time.get_ticks()

def shoot(obj:entity):
    """shootattack action for object

    Args:
        obj (entity): the object to apply the action

    """ 
    if  pg.time.get_ticks() - obj.shootTime  > obj.shotCooldown:
        obj.isShooting = True

def stop(obj:entity):
    """stops all character movement and action dynamics

    Args:
        obj (entity): _description_
    """
    obj.stopEx()
    
class control_dsg:

    def __init__(self) -> None:
        """The control_dsg object deals with filtering and processing keyboard inputs using pygame
        """
        self.key = pg.key.get_pressed()
        
        # The input dictionary sets the inputs for what each movement to be processed. 
        # The default is the AD Control scheme below 
        self.inputs = {
            pg.K_a: move_left, 
            pg.K_d: move_right,
            pg.K_w: move_jump
        } 

    def borderAll(self, screen:screen, *obj:entity, coords=(-1, -1, -1)) -> None:
        """Sets the exception preventing objects going past the game screen.

        Args:
            screen (screen): The screen object for the game
            obj (entity): the objects to obey the exception
            coords : xl, xr and y coordinates for object(s) border
        """
        

        def borderXl(o:entity, coords) -> None:
            if coords == None:
                pass # Character does not have a border
            else:
                if o.rect.left + o.dx < coords:
                    o.dx = -o.rect.left

                    o.hasVelocity = False
                    o.jump = False
        
        def borderXr(o:entity, coords) -> None:
            if coords == None:
                pass # Character does not have a border
            else:
                if o.rect.right + o.dx > coords - 100:
                    o.past_border = True
                    o.hasVelocity = False 
                    o.dx = (screen.WIDTH/2) - o.rect.right

        # this needs to be modified to a mask system, not useful enough once we add elevation to the level..
        # def borderY(o:entity, col) -> None:
        
        #     if col == None:
        #         pass # Character does not have a border
        #     else:

        #         # coordsAdj = col
        #         # if o.rect.bottom + o.dy > coordsAdj:
        #         #     o.vel_y = 0
        #         #     o.dy = screen.HEIGHT - 200 - o.rect.bottom 
        #         #     o.jump = False

        if coords[0] == -1 : xl = screen.borderXl 
        else: xl = coords[0]
        if coords[1] == -1 : xr = screen.borderXr
        else: xr = coords[1]

        # if coords[2] == -1 : y = screen.borderY
        # else:  y = coords[2]

        for o in obj:
            borderXl(o, xl)
            borderXr(o, xr)
            # borderY(o, y)

    def borderCol(self, obj:entity) -> None:
        for maskobj in mask.getMaskDict().keys():
            mask_img = maskobj.mask_img
            mask_rect = maskobj.get_mask_rect()

            offset_x = obj.rect.x - mask_rect.x

            offset_y = obj.y - mask_rect.y
            current_y = obj.y

            # overlap = mask_img.overlap(mask_img, (offset_x, offset_y))

            #current problem with mask - jumping odesn't work so great..

            if offset_y > 600:
                # print(obj.rect.y)
                # obj.vel_y = 0
                if obj.y != current_y:
                    obj.dy = -1
                
                obj.jump = False
                # if pg.time.get_ticks() - obj.jump_time > 100:
                #     obj.jump = False

            else:
                obj.dy = 0

    def jumpEx(self, *obj:entity) -> None:
        """Sets the exception making objects obey their gravity variable and jump.

        Args:
            obj (entity): the objects to obey the exception
        """
        for o in obj:
            if o.jump:
                o.vel_y += o.gravity                
                o.dy += o.vel_y

    def set_move_AD(self):
        inputs = {
            pg.K_a:     move_left,
            pg.K_d:     move_right,
            pg.K_w:     move_jump,
            pg.K_SPACE: show,
            pg.K_r:     attk_light,
            pg.K_t:     shoot
        }

        return inputs

    def set_move_AK(self):
        inputs = {
            pg.K_LEFT: move_left,
            pg.K_RIGHT: move_right,
            pg.K_UP: move_jump,
            pg.K_SPACE: show,
            pg.K_k: attk_light,
            pg.K_l: attk_light
        }

        return inputs

    def menu(self, event, button_rect):
        """Set object inputs to the control scheme found in the inputs directory for the game menu

        Args:
            event (_type_): pygame event object
            obj (entity): object to use control scheme
        """
        if event.type == pg.KEYDOWN:
            try:
                self.menuClick[event.key](event.pos, button_rect)

            except KeyError:
                pass    

    def move(self, event, obj:entity, inputs:dict,  gamestate):
        """Set object inputs to the control scheme found in the inputs directory for moving characters

        Args:
            event (_type_): pygame event object
            obj (entity): object to use control scheme
        """

        if event.type == pg.KEYDOWN:

            if not (obj.isAttacking) and not (obj.isShooting):
                try:

                    inputs[event.key](obj)
                    obj.Kinput = True

                except KeyError:
                    pass

        if event.type == pg.KEYUP:
            #controls shooting variables
            if obj.isShooting:
                obj.release = True
                obj.shootTime  = pg.time.get_ticks()

            stop(obj)  
