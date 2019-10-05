import sys, logging, os, random, math, arcade, color

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN=30
SCREEN_TITLE = "Space Shooter"
NUM_METEORS=5
NUM_ENEMIES= 5 
STRATING_LOCATION=(400,100)
BULLET_DEMAGE = 10
ENEMY_HP=100
HIT_SCORE = 10
KILL_SCORE=100
GAME_INTRO_0=0
GAME_INTRO=1
GAME_RUNNING=2
GAME_END=3
GRAVITY=-3


class Bullet(arcade.Sprite):
    def __init__(self,position,velocity,damage):

        super().__init__("PNG/Sprites/Missiles/spaceMissiles_003.png",0.5)
        (self.center_x,self.center_y)=position
        (self.dx,self.dy)=velocity
        self.damage=damage
    def update(self):
        self.center_x+=self.dx
        self.center_y+=self.dy
        
class Missiles(arcade.Sprite):
    def __init__(self,position,velocity,damage):

        super().__init__("PNG/Sprites/Missiles/spaceMissiles_006.png",0.5)
        (self.center_x,self.center_y)=position
        (self.dx,self.dy)=velocity
        self.damage=damage
    def update(self):
        self.center_x+=self.dx
        self.center_y+=self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("PNG/Sprites/Rockets/spaceRockets_003.png",0.5)
        (self.center_x, self.center_y)=STRATING_LOCATION


class Enemy(arcade.Sprite):
    def __init__(self,position):
        super().__init__("PNG/Sprites/Ships/spaceShips_004.png", 0.5)
        self.hp=ENEMY_HP
        (self.center_x, self.center_y)=position
        self.dx=0
        self.dy=0
    def accelerate(self,dx,dy):
        self.dx+=dx
        self.dy+=dy

class Meteor(arcade.Sprite):
    def __init__(self, x,y, position):
        super().__init__("PNG/Sprites/Meteors/spaceMeteors_001.png", 0.5)
        self.x=x
        self.y=y
        self.hp=ENEMY_HP
        (self.center_x, self.center_y)=position
        self.dx=0
        self.dy=0

    def accelerate(self,dx,dy):
        self.dx+=dx
        self.dy+=dy

class Window(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)
        self.bullet_list=arcade.SpriteList()
        self.enemy_list=arcade.SpriteList()
        self.meteor_list=arcade.SpriteList()
        self.player=Player()
        self.score=0
        self.status=GAME_INTRO_0
        arcade.set_background_color(arcade.color.BLUE)




    def setup(self):
        
        #set up enemies
        for i in range(NUM_ENEMIES):
            x=random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y=random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            self.enemy=Enemy((x,y))
            self.enemy_list.append(self.enemy)

        #set up Meteors
        for a in range(NUM_METEORS):
            x=random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y=random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            self.meteor=Meteor(x,y,(x,y))
            self.meteor_list.append(self.meteor)



    def update(self, delta_time):
        #make the enemies and meteors moving
        for b in self.enemy_list:
            b.accelerate(0,GRAVITY)
            b.update()
        
        for c in self.meteor_list:
            c.accelerate(0,GRAVITY)
            c.update()


    def draw_game_intro(self):
        '''
            draw welcome interface
        '''
        output="Space Shooter"
        arcade.draw_text(output,200,500,arcade.color.WHITE,54)

        output2="Click right mouse to start"
        arcade.draw_text(output2,200,400,arcade.color.WHITE,45)
    def draw_game_over(self):

        output3="GAME OVER"
        arcade.draw_text(output3,200,500,arcade.color.WHITE,54)
        output4="Score: "+str(self.score)
        arcade.draw_text(output4,200,400,arcade.color.WHITE,35)
    
    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()

        if self.status==GAME_INTRO:
            self.draw_game_intro()
        if self.status==GAME_RUNNING:
            arcade.draw_text(str(self.score),20, SCREEN_HEIGHT-40, arcade.color.WHITE, 16)
            self.player.draw()
            self.bullet_list.draw()
            self.enemy_list.draw()
            self.meteor_list.draw()
        if self.status==GAME_END:
            self.draw_game_over()




    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button== arcade.MOUSE_BUTTON_RIGHT:
            if self.status==GAME_INTRO_0:
                self.status=GAME_INTRO
            elif self.status==GAME_INTRO:
                self.setup()
                self.status=GAME_RUNNING
            elif self.status==GAME_RUNNING:
                self.setup()
                self.status=GAME_END

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()