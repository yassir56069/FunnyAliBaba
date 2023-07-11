import pygame as pg
import orjson


from object import object
from screen import screen
from bullet import bullet

class entity(object):

    _entityList = []
    _npc        = []

    def __init__(self, config="", img="", show:bool = True, coord:tuple = (0,0), size= (80,180) ) -> None:
        """the entity class represents the playable entity character pygame objects

        Args:
            img (str, optional): The image of the entity. Defaults to "".
            show (bool, optional): Whether to show the object or not. Defaults to "" (True).
            coord (tuple, optional): The coordinates of the object's initial position. Defaults to (0,0).
            size (tuple, optional): The size of the object in question. Defaults to (80,180).
        """

        super().__init__(img, show, coord, size)

        # character
        if config: 
           self.speed, self.jumpVal, self.gravity, self.health, self.scale, self.imgSize, self.imgoffset = readConfigJSON(config)
        else:
            self.speed        = 3
            self.jumpVal      = 6
            self.gravity      = 1
            self.health       = 100
            self.imgSize      = 162 
            self.scale        = 3
            self.imgoffset    = (50,50)
        
        # movement
        self.dx = self.dy = self.vel_y = 0
        self.gx = self.gy = 0
        self.Kinput = False


        self.charaFlip      = False
        self.jump           = True
        self.jump_time      = pg.time.get_ticks()
        self.isMoving       = False
        self.lastPress      = 0
        self.shootTime      = 0
        self.isAttacking    = False

        self.shotPower      = 4       
        self.shotCooldown   = 2000     # cooldown for shots in ms (default 5000) 
        self.isShooting     = False
        self.release        = False

        # sprite
        self.bulletImg   = pg.image.load('assets//images//icons//bullet.png').convert_alpha()
        self.update_time = pg.time.get_ticks()
        self.anim_list   = []
        self.action      = 0     # 0:idle | 1:run | 2:jump | 3:attack1 | 4:attack2 | 5:hit | 6:death 
        self.frame_index = 0
        self.attacking   = 0
        self.steps       = []
        if img:
            self.sprite_img = self.img.copy()

        entity._entityList.append(self)
        if type(self) != player:
            entity._npc.append(self)

    def draw(self, screen: screen, scale=False, coord=(0,0)):
        """Draw the entity to the game screen [Overwirtes the object function]

        Args:
            screen (screen): Game screen object
            scale (bool, optional): Whether to scale the object or not. Defaults to True.
            coord (tuple, optional): The coordinates of the of the object to . Defaults to (0,0).
        """

        self.rect.x += self.dx
        self.rect.y += self.dy

        self.gx += self.dx
        self.gy += self.dy

        self.x = coord[0] + self.rect.x - (self.imgoffset[0] * self.scale) 
        self.y  = coord[1] + self.rect.y - (self.imgoffset[1] * self.scale)

       

        if self.img == "": pg.draw.rect(screen.SCREEN, (255,0,0), self.rect)
        else: 
            # pg.draw.rect(screen.SCREEN, (255,0,0), self.rect)
            self.img = pg.transform.flip(self.anim_list[self.action][self.frame_index], self.charaFlip, False)

            super().draw(screen, scale, (self.x , self.y))

    def animChara(self):
        """Call in game loop to animate the object
        """

        anim_cooldown = 50  # cooldown for animation in ms
        attk_cooldown = 350 # cooldown for attack action to last
        self.action   = 0   # character is idle

        action = {
            self.isMoving    : 1,
            self.jump        : 2,
            self.isAttacking : 3,   
        }

        for action, value in action.items():
            if action == True:
                self.action = value

        if pg.time.get_ticks() - self.attacking > attk_cooldown:
            self.isAttacking = False

        # check if time elapsed is enough for the last update
        if pg.time.get_ticks() - self.update_time > anim_cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        
        if self.frame_index >= len(self.anim_list[self.action]):
            self.frame_index = 0

    def GenImages(self, *step_values) -> None:
        """Generate sprite images for the object, for the steps values given
        """

        if len(step_values) < 8:
            steps = []
            for v in step_values:
                steps.append(v)
        else:
            print('too many step notations or invalid step notation, clearing image to avoid crash')
            print('maybe you forgot to give step values..?')
            self.img = ''


        # check if images have already been generated
        if not self.anim_list:                                # IMPORTANT : look at full sprite image to understand
            for y, animation in enumerate(steps):             # for each action in step - (y : row -> action being done) (animation : sprite)
                _img_list = []                                # <-- individual sprite images are stored here (temp)
                for x in range(animation):                    # for each sprite: 
                    temp_img = self.sprite_img.subsurface(    # <-- stores one sprite image (temp)
                        x * self.imgSize,                       # x: column from full sprite image
                        y * self.imgSize,                       # y: row from full sprite image 
                        self.imgSize, self.imgSize              
                        )

                    # append collection of images for action to image list in one element
                    _img_list.append(
                        pg.transform.scale(temp_img, (self.imgSize * self.scale, self.imgSize * self.scale))
                        )

                # store full list
                self.anim_list.append(_img_list)

    def delayEx(self, timeout = 50) -> None:
        """Sets the exception adding delay to object input

        Args:
            timeout (int, optional):  amount of delay in ms. Defaults to 50ms.
        """
        if self.Kinput == False:
            if pg.time.get_ticks() - self.lastPress > timeout:
                self.dx = 0

    def stopEx(self):
        """Sets the exception to stop the object appropriately, setting all conditions 
        """
        self.Kinput = False
        self.isMoving = False
        self.isShooting = False
        self.lastPress = pg.time.get_ticks()
        
    def BulletEx(self, shoot_decay = 500) -> None:
        """Sets the exception to manage throwables ruling

        Args:
            shoot_decay (int, optional):  amount time before bullets are cleared. Defaults to 500ms.
        """

        # power of shot increases as player triggers the shoot function
        if self.isShooting:
            self.shotPower += 0.1

        # shots eventually decay after the shootTime has elapsed
        if pg.time.get_ticks() - self.shootTime > shoot_decay:
            bullet._group.empty()

        # release the shot
        if self.release:
            bullets = bullet(self.bulletImg,(self.rect.centerx + 60 * ((not self.charaFlip) * 2 - 1), self.rect.centery - 90), self.shotPower, self.charaFlip)
            bullet._group.add(bullets)
            self.release   = False
            self.shotPower = 4

    def drawAtk(self, screen:screen, target):
        """Draw the sprite's attacks

        Args:
            screen (screen): Screen to draw the attack to
            target (_type_): The target of the attack
        """

        self.atkRect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.charaFlip), self.rect.y, 2 * self.rect.width, self.rect.height)

        if self.atkRect.colliderect(target.rect):
            color = (255,0,0)
            target.health -= 10
        else:
            color = (0,255,0)

        pg.draw.rect(screen.SCREEN, color, self.atkRect)

    def place(self, pos:tuple):
        """"place object at designated coordinates"""       
        
        self.x = pos[0]
        self.y = pos[1]

#region Getters and Setters

        @property 
        def dx(self): return self._dx
            
        @dx.setter
        def dx(self, c:float): self._dx = c
        
        @dx.deleter 
        def dx(self): del self._dx
                        
        @property 
        def dy(self): return self._dy
            
        @dy.setter
        def dy(self, c:float): self._dy = c
        
        @dy.deleter 
        def dy(self): del self._dy

        @property 
        def attacking(self): return self._attacking
            
        @attacking.setter
        def attacking(self, c): self._attaking = c
        
        @attacking.deleter 
        def attacking(self): del self._attacking

        @property 
        def vel_y(self): return self._vel_y
            
        @vel_y.setter
        def vel_y(self, c:float): self._vel_y = c
        
        @vel_y.deleter 
        def vel_y(self): del self._vel_y

        @property 
        def shotPower(self): return self._shotPower
            
        @shotPower.setter
        def shotPower(self, c:float): self._shotPower = c
        
        @shotPower.deleter 
        def shotPower(self): del self._shotPower

        
        @property 
        def Kinput(self): return self._Kinput
            
        @Kinput.setter
        def Kinput(self, b:bool): self._Kinput = b
        
        @Kinput.deleter 
        def Kinput(self): del self._Kinput

        @property 
        def isAttacking(self): return self._isAttacking
            
        @isAttacking.setter
        def isAttacking(self, b:bool): self._isAttacking = b
        
        @isAttacking.deleter 
        def isAttacking(self): del self._isAttacking

        @property 
        def isMoving(self): return self._isMoving
            
        @isMoving.setter
        def isMoving(self, b:bool): self._isMoving = b
        
        @isMoving.deleter 
        def isMoving(self): del self._isMoving

        @property 
        def isShooting(self): return self._isShooting
            
        @isShooting.setter
        def isShooting(self, b:bool): self._isShooting = b
        
        @isShooting.deleter 
        def isShooting(self): del self._isShooting

        @property 
        def charaFlip(self): return self._charaFlip
            
        @charaFlip.setter
        def charaFlip(self, b:bool): self._charaFlip = b
        
        @charaFlip.deleter 
        def charaFlip(self): del self._charaFlip


#endregion

    def getentityList(): 
        """Returns a python list of all entity objects

        Returns:
            _type_: returns the entitylist, containing all entity objects
        """
        return entity._entityList
    
    def getNpcs(): 
        """Returns a python list of all npcs

        Returns:
            _type_: returns the entitylist, containing all entity objects
        """
        return entity._npc

class player(entity):
    def __init__(self, config="", img="", show: bool = True, coord: tuple = (0, 0), size=(80, 180)) -> None:
        
        self.rx = self.lx = 0
        self.border = 500
        self.past_border = self.befr_border = False

        super().__init__(config, img, show, coord, size)

    def update_borders(self) -> None:

        self.past_border = self.rect.x > self.border and self.action == 1 
        self.befr_border = self.rect.x < self.border and (self.action == 1 and self.charaFlip == 1) 

    def is_past_border(self) -> bool:
        """Check if entity object is current located past the border

        Returns:
            bool: of condition
        """

        return self.past_border

    def is_before_border(self) -> bool:
        """Check if entity object is currently located before the border

        Returns:
            bool: of condition
        """
        
        player.update_borders(self)


        return self.befr_border

    def borderMoveEnt(self, speed:float, *ent:entity) -> None:

        for e in ent:
            if self.past_border:
                e.rect.x -= speed
            
            if self.befr_border:
                e.rect.x += speed

    def borderMoveLayerindx(self, speed:float, bg) -> None:
        # for layer in layers:
        if self.past_border:
            self.rx  += speed
            self.gx += speed
            bg.x1 -= speed
        
        if self.befr_border:
            self.lx  += speed
            self.gx -= speed
            bg.x1 += speed

    def setScreenborder(self, screen:screen, ratio = 0) -> None:
        """Set the screen border for the entitywithin a ratio

        Args:
            screen (screen): the screen to set the ratio from
            ratio (_type_): the ratio to set the screen border to
        """
        if ratio == 0:
            self.border = 0
        else:
            self.border = screen.WIDTH / ratio

def readConfigJSON(config):
    """Read a config JSON file : in this case used for character value configs

    Args:
        config (_type_): the relative path to the config file to read

    Returns:
        integer values for the parameters that were given (speed, jump height and gravity strength)
    """
    with open(config, "r") as f:
        data = orjson.loads(f.read())

        speed   = int(data["speed"])
        jump    = int(data["jump"])
        gravity = int(data["gravity"])
        health  = int(data["health"])
        scale   = int(data["scale"])
        size    = int(data["size"])
        offset  = tuple(data["offset"])

    return speed, jump, gravity, health, scale, size, offset

# player: moving, attacking


# def GenSteps(self, *values:int) -> None:
#     """Generate sprite steps for the object (steps for each action)
#     """
#     if len(values) < 8:
#         self.steps = []
#         for v in values:
#             self.steps.append(v)
#     else:
#         print('too many step notations or invalid step notation, clearing image to avoid crash')
#         self.img = ''+


# def borderMoveLayer(self, speed:float, is_dynamic:bool, layer) -> None:
#     # for layer in layers:
#     if self.past_border:
#         layer.x1 -= speed
    
#     if self.befr_border:
#         layer.x1 += speed

#     if is_dynamic and (abs(layer.x1) >= layer.WIDTH):
#         layer.x1 += layer.WIDTH
