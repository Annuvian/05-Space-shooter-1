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
# NUM_METEORS=10
NUM_ENEMIES= 6 
STRATING_LOCATION=(400,100)
BULLET_DAMAGE = 10
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
    def __init__(self,locate,speed,damage):

        super().__init__("PNG/Sprites/Missiles/spaceMissiles_004.png",0.5)
        (self.center_x,self.center_y)=locate
        (self.dx,self.dy)=speed
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


# class Meteor(arcade.Sprite):
#     def __init__(self, position):
#         super().__init__("PNG/Sprites/Meteors/spaceMeteors_001.png", 0.2)
#         (self.center_x, self.center_y)=position
#         self.hp=20
#         self.dx=0
#         self.dy=0

#     def update(self):
#         self.center_x += self.dx
#         self.center_y += self.dy
        

#     def accelerate(self,dx,dy):
#         self.dx+=dx
#         self.dy+=dy

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
        # self.meteor_list=arcade.SpriteList()
        self.missiles_list=arcade.SpriteList()
        self.player=Player()
        self.score=0
        self.life=100
        self.level=1
        self.status=GAME_INTRO_0
        self.enemy_list_hp={}
        arcade.set_background_color(arcade.color.BLUE)




    def setup(self):
        
        #set up enemies
        for i in range(NUM_ENEMIES):
            x=120*(i+1)+40
            y=500
            self.enemy = Enemy((x,y))
            self.enemy_hp=self.enemy.hp           
            self.enemy_list_hp[self.enemy]=self.enemy_hp
            self.enemy_list.append(self.enemy) 
                        
        

      



    def update(self, delta_time):
        #make the enemies and meteors moving
        self.bullet_list.update()
        self.missiles_list.update()
        for d in self.enemy_list: 
            if random.randrange(200) == 0:
                a= d.center_x
                b= d.center_y
                if self.level==1:
                    missiles=Missiles((a,b),(0,-1),BULLET_DAMAGE)
                    self.missiles_list.append(missiles)
                elif self.level==2:
                    missiles=Missiles((a,b),(0,-3),BULLET_DAMAGE)
                    self.missiles_list.append(missiles)
                elif self.level==3:
                    missiles=Missiles((a,b),(0,-5),BULLET_DAMAGE)
                    self.missiles_list.append(missiles)
        
        for j in self.missiles_list:
                attack=arcade.check_for_collision(j,self.player)
                if bool(attack) is True:
                    j.kill()
                    self.life-=HIT_SCORE
                    if int(self.life)==0:
                        self.player.kill()
                        self.status=GAME_END
        
        for e in self.enemy_list: 
            for i in self.bullet_list:
                hit=arcade.check_for_collision_with_list(i,self.enemy_list)
                if len(hit)>0:
                    i.kill()
                    self.score+=HIT_SCORE
                    for b in hit:
                        self.enemy_list_hp[b]-=HIT_SCORE
                        if int(self.enemy_list_hp[b])==0:
                            b.kill() 
                            del self.enemy_list_hp[b]
                            #if there is no enemy in the list, the game will end 
                            if bool(self.enemy_list_hp) is False:
                                self.status=GAME_END

    def draw_game_intro(self):
        '''
            draw welcome interface
        '''
        output="Space Shooter"
        arcade.draw_text(output,200,500,arcade.color.WHITE,54)

        output2="Click [enter] to start"
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
            arcade.draw_text("Score: "+str(self.score),40, SCREEN_HEIGHT-40, arcade.color.WHITE, 16)
            arcade.draw_text("Life: "+str(self.life),40, SCREEN_HEIGHT-60, arcade.color.WHITE, 16)
            self.player.draw()
            self.missiles_list.draw()
            self.bullet_list.draw()
            self.enemy_list.draw()
            # self.meteor_list.draw()
            if self.score>0 and self.score<100:
                arcade.draw_text("level:"+str(self.level),40, SCREEN_HEIGHT-80, arcade.color.WHITE, 16)
            if self.score>100 and self.score<300:
                arcade.draw_text("level:"+str(self.level),40, SCREEN_HEIGHT-80, arcade.color.WHITE, 16)
            if self.score>300 and self.score<6:
                arcade.draw_text("level:"+str(self.level),40, SCREEN_HEIGHT-80, arcade.color.WHITE, 16)
        if self.status==GAME_END:
            self.draw_game_over()




    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.score<100:
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,5),BULLET_DAMAGE)
                self.bullet_list.append(bullet)
            elif self.score<300:
                self.level=2
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet1 = Bullet((x-20,y),(0,8),BULLET_DAMAGE)
                bullet2 = Bullet((x+20,y),(0,8),BULLET_DAMAGE)
                self.bullet_list.append(bullet1)
                self.bullet_list.append(bullet2)
            elif self.score<=600:
                self.level=3
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
                bullet1 = Bullet((x-20,y),(0,10),BULLET_DAMAGE)
                bullet2 = Bullet((x+20,y),(0,10),BULLET_DAMAGE)
                self.bullet_list.append(bullet)
                self.bullet_list.append(bullet1)
                self.bullet_list.append(bullet2)
            
        

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        
        if key== arcade.key.ENTER:
            if self.status==GAME_INTRO_0:
                self.status=GAME_INTRO
            elif self.status==GAME_INTRO:
                self.setup()
                self.status=GAME_RUNNING
            elif self.status==GAME_RUNNING:
                self.setup()
                self.status=GAME_END

        if key == arcade.key.LEFT:
            print("Left")
            self.player.center_x-=20

        elif key == arcade.key.RIGHT:
            print("Right")
            self.player.center_x+=20

        elif key == arcade.key.UP:
            print("Up")
            self.player.center_y+=20

        elif key == arcade.key.DOWN:
            print("Down")
            self.player.center_y-=20

        elif key == arcade.key.SPACE:
            if self.score<100:
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,5),BULLET_DAMAGE)
                self.bullet_list.append(bullet)
            elif self.score<300:
                self.level=2
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet1 = Bullet((x-20,y),(0,8),BULLET_DAMAGE)
                bullet2 = Bullet((x+20,y),(0,8),BULLET_DAMAGE)
                self.bullet_list.append(bullet1)
                self.bullet_list.append(bullet2)
            elif self.score<=600:
                self.level=3
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
                bullet1 = Bullet((x-20,y),(0,10),BULLET_DAMAGE)
                bullet2 = Bullet((x+20,y),(0,10),BULLET_DAMAGE)
                self.bullet_list.append(bullet)
                self.bullet_list.append(bullet1)
                self.bullet_list.append(bullet2)
            
    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT:
            print("Left")
            self.player.center_x-=10

        elif key == arcade.key.RIGHT:
            print("Right")
            self.player.center_x+=10

        elif key == arcade.key.UP:
            print("Up")
            self.player.center_y+=10

        elif key == arcade.key.DOWN:
            print("Down")
            self.player.center_y-=10

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()