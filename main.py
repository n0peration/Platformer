import pyglet
from pyglet.window import key, mouse
import config
import util
import sprites
from collide import *

class PygletGame(object):
    """A layer between pyglet and the game itself. Discard if inconvenient"""

    def start(self):
        # pyglet window
        self.window = pyglet.window.Window(config.RESOLUTION[0], config.RESOLUTION[1], caption=config.TITLE)
        self.window.set_handlers(self)
        # logging every key and mouse event
        self.window.push_handlers(pyglet.window.event.WindowEventLogger())

        # instantiate game
        self.game = Game()
        self.game.load()

        # key handling
        self.game.keys = key.KeyStateHandler()
        self.window.push_handlers(self.game.keys)
        
        # set update interval
        pyglet.clock.schedule_interval(self.game.update, 1.0 / config.FPS)

        # start
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.game.draw()

class Game(object):

    def __init__(self):
        self.keys = None
        self.platforms = set()

    def load(self):
        """Initialize the game"""

        # sprites
        background_image = util.load_image(config.IMG_BACKGROUND)
        ground_image = util.load_image(config.IMG_GROUND)
            
        self.background = sprites.GameSprite(background_image, 0, 0)
        self.ground = sprites.GameSprite(ground_image, 0, 0 )
        self.player = sprites.Player(x=100, y=100)
        self.platform = sprites.Platform(x=250, y=260)

        self.sprites_background = set()
        self.sprites_foreground = set()

        # forces
        self.passive_forces = []
        self.active_forces = []

    def draw(self):
        self.background.draw()
        self.ground.draw()
        self.player.draw()
        self.platform.draw()

    def update(self, dt):
        self.handle_input(dt)
        
        if self.player.y < 0:
            self.player.y = 0
        
        if self.platform.y < 0:
            self.platform.y = 0
            
        #gravity 
        self.player.y -= 9
        
        #ground collision
        while collide(self.player.collision, self.ground.collision):
            self.player.y += 1 # stay above ground
        
        #platform collision
        while collide(self.player.collision, self.platform.collision):
            self.platform.apply_force(self.platform.force_up, dt)
            self.player.apply_force(self.player.force_down, dt)
    

    def handle_input(self, dt):
        if self.keys[key.LEFT]:
            self.player.go_left(dt)
        if self.keys[key.RIGHT]:
            self.player.go_right(dt)
        if self.keys[key.UP]:
        	self.player.go_up(dt)
        if self.keys[key.DOWN]:
        	self.player.go_down(dt)
            
def main():
    game = PygletGame()
    game.start()

if __name__ == "__main__":
    main()


