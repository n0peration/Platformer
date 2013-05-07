import pyglet
import config
from util import *
from gamemath import vector_add
from collide import *

class GameSprite(pyglet.sprite.Sprite):
    """A sprite on which physical forces can apply"""

    def __init__(self, image, x, y ):
        pyglet.sprite.Sprite.__init__(self, image, x=x, y=y)
        self.collision = SpriteCollision(self)
        self.forces = set()

    def apply_force(self, force, dt):
        """force is a function
        dt is the elapsed time since the last frame

        returns the movement vector of the force

        """
        dv = force(self, dt)
        if dv != None:
            pos_new = vector_add(self.position, dv)
            self.set_position(pos_new[0], pos_new[1])
        return dv

    def update(self, dt):
        # apply forces
        for force in self.forces:
            dv = self.apply_force(force, dt)
            if not dv:
                self.forces.remove(force)

class Player(GameSprite):

    def __init__(self, x=0, y=0 ):
        player_image = load_image(config.IMG_PLAYER)
        GameSprite.__init__(self, player_image, x=x, y=y)
        self.speed = 450
        self.force_left = lambda p, dt: (-p.speed * dt, 0)
        self.force_right = lambda p, dt: (p.speed * dt, 0)
        self.force_up = lambda p, dt: (0, p.speed * dt)
        self.force_down = lambda p, dt: (0, -p.speed * dt)

    def go_left(self, dt):
        self.apply_force(self.force_left, dt)

    def go_right(self, dt):
        self.apply_force(self.force_right, dt)
    
    def go_up(self, dt):
    	self.apply_force(self.force_up, dt)
    	
    def go_down(self, dt):
    	self.apply_force(self.force_down, dt)

class Platform(GameSprite):

    def __init__(self, x=0, y=0 ):
        platform_image = load_image(config.IMG_PLATFROM)
        GameSprite.__init__(self, platform_image, x=x, y=y )
        self.power = 5
        self.force_up = lambda p, dt: (0, p.power * dt)
        