import pygame, sys
import random
import os
import time
from pygame import mixer
from os import path

HS_FILE = "highscore.txt"                                   
WIDTH = 1950
HEIGHT = 1000
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8
score = 0
highscore = -99
rounds = 0

# load high score
try:
    file = open(HS_FILE, encoding="utf-8")
    contents = file.readlines()
finally:
    file.close()
highscore = int(contents[0])
print(highscore)



#CONSTANTS - PHYSICS
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.095   #.12
PLAYER_GRAV = 1.1
vec = pygame.math.Vector2

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (48, 227, 255)

#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


        
#DRAW TEXT
font_name = pygame.font.match_font("georgia")
def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


#SHOW START SCREEN FUNCTION
def show_start_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ROBOTS VS ALIENS", 64, WIDTH / 2 - 300, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, space to shoot", 22, WIDTH / 2 - 200, HEIGHT / 2)
    draw_text(screen, "press 'q' to quit", 22, WIDTH / 2 - 100, HEIGHT / 1.6)
    draw_text(screen, "change music by pressing 1, 2, or 3,", 18, WIDTH / 2 - 165, 700)
    draw_text(screen, "Taunt by pressing 't'. Enter infinite mode by pressing '8'", 18, WIDTH / 2 - 225, 800)
    draw_text(screen, "Press a key to begin...", 18, WIDTH / 2 - 100, HEIGHT * 3 / 4)
    draw_text(screen, "High Score: ", 22, WIDTH / 2 - 200, 15)
    draw_text(screen, str(highscore), 22, WIDTH / 2 + 100, 15)
    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_end_screen():
    if score > highscore:
        try:
            file = open(HS_FILE, "w", encoding="utf-8")
            file.write(str(score))
        finally:
            file.close()

        

    else:
        draw_text(screen, "High Score: ", 22, WIDTH / 2, 15)
        draw_text(screen, str(highscore), 22, WIDTH / 2 + 200, 15)


    
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "Press ENTER to try again", 22, WIDTH / 2 - 175, HEIGHT / 2 + 200)
    draw_text(screen, str(score), 35, 1050, 500)
    draw_text(screen, "FINAL SCORE: ", 35, 800, 500)
    if score > highscore:
        draw_text(screen, "NEW HIGH SCORE!", 38, WIDTH / 2 - 195, HEIGHT / 4 + 150)
    else:
        draw_text(screen, "High Score: ", 22, 800, 15)
        draw_text(screen, str(highscore), 22, 950, 15)



    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if keystate[pygame.K_RETURN]:
                waiting = False
                mixer.music.play()

def show_newlevel_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "LEVEL COMPLETE!", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "Press the ENTER key to play the next level!", 22, WIDTH / 2 - 200, HEIGHT / 2)
    draw_text(screen, "press 'q' to quit", 22, WIDTH / 2 - 200, HEIGHT / 1.6)
    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if keystate[pygame.K_RETURN]:
                waiting = False

def show_win_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "YOU WIN!!!", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "You defeated all of the aliens!", 22, WIDTH / 2 - 200, HEIGHT / 2 - 100)
    draw_text(screen, "Robot, spaceship, alien, and meteor sprites done by Kenney.nl or www.kenney.nl", 22, WIDTH / 2 - 200, HEIGHT / 2)
    draw_text(screen, "Background done by opengameart.org/users/joshshshsh", 22, WIDTH / 2 - 200, HEIGHT / 2 + 100)
    draw_text(screen, "Song 1 done by opengameart.org/users/yd, song 2 done by opengameart.org/users/nia-mi", 22, WIDTH / 2 - 200, HEIGHT / 2 + 200)
    draw_text(screen, "Game developed by Gabe Pelkey", 22, WIDTH / 2 - 200, HEIGHT / 2 + 300)
    draw_text(screen, "press 'q' to quit", 22, WIDTH / 2 - 200, 900)
    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()

#SHOW INFINITE SCREEN FUNCTION
def show_infinite_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ROBOTS VS ALIENS", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "You have unlocked infinite mode!", 22, WIDTH / 2 - 200, HEIGHT / 2)
    draw_text(screen, "press 'q' to quit", 22, WIDTH / 2 - 200, HEIGHT / 1.6)
    draw_text(screen, "change music by pressing 1, 2, or 3,", 18, WIDTH / 2 - 200, 700)
    draw_text(screen, "Press the enter key to begin...", 18, WIDTH / 2 - 200, HEIGHT * 3 / 4)
    draw_text(screen, "High Score: ", 22, WIDTH / 2, 15)
    draw_text(screen, str(highscore), 22, WIDTH / 2 + 200, 15)
    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if keystate[pygame.K_RETURN]:
                waiting = False

#SHOW PAUSE SCREEN FUNCTION
def show_pause_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME PAUSED", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "press 'Enter' to resume game", 22, WIDTH / 2 - 200, HEIGHT / 1.6)
    draw_text(screen, "change music by pressing 1, 2, or 3,", 18, WIDTH / 2 - 200, 700)
    pygame.display.flip()
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if keystate[pygame.K_RETURN]:
                waiting = False

                    
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.healthbars = [
            pygame.image.load(os.path.join(img_folder, "healthbar_0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "healthbar_1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "healthbar_2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "healthbar_3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "healthbar_4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "healthbar_5.png")).convert()
            ]
        self.healthbar_count = 0

        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.image.set_colorkey(BLACK)

        #ESTABLISH RECT, STARTING POINT
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 5

    def getHealth(self):
        return self.healthbar_count

    #PASS IN +1 OR -1 TO INCREMENT / DECREMENT HEALTH BAR
    def setHealth(self, health):
        
        if health == 1: #INCREASE HEALTH UNLESS self.healthbar_count is at 0
            self.healthbar_count -= 1
            if self.healthbar_count < 0:
                self.healthbar_count = 0

        elif health == -1: #DECREASE HEALTH, UNLESS self.healthbar_count is at 5
            self.healthbar_count += 1
            if self.healthbar_count > 5:
                self.healthbar_count = 5

    def update(self):
        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (300, 100))
        self.image.set_colorkey(BLACK)



class Enemy_HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.healthbars = [
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar5.png")).convert()
            ]
        self.healthbar_count = 0

        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (1, 1))
        self.image.set_colorkey(BLACK)

        #ESTABLISH RECT, STARTING POINT
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 50

    def getHealth(self):
        return self.healthbar_count

    #PASS IN +1 OR -1 TO INCREMENT / DECREMENT HEALTH BAR
    def setHealth(self, health):
        
        if health == 1: #INCREASE HEALTH UNLESS self.healthbar_count is at 0
            self.healthbar_count -= 1
            if self.healthbar_count < 0:
                self.healthbar_count = 0

        elif health == -1: #DECREASE HEALTH, UNLESS self.healthbar_count is at 5
            self.healthbar_count += 1
            if self.healthbar_count > 5:
                self.healthbar_count = 5

    def update(self):

        if score >= 600:
            self.image = self.healthbars[self.healthbar_count]
            self.image = pygame.transform.scale(self.image, (300, 100))
            self.image.set_colorkey(BLACK)
            draw_text(screen, "BOSS HEALTH: ", 15, 1200, 60)

class Enemy2_HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.healthbars = [
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar0.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar1.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar2.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar3.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar4.png")).convert(),
            pygame.image.load(os.path.join(img_folder, "enemy_healthbar5.png")).convert()
            ]
        self.healthbar_count = 0

        self.image = self.healthbars[self.healthbar_count]
        self.image = pygame.transform.scale(self.image, (1, 1))
        self.image.set_colorkey(BLACK)

        #ESTABLISH RECT, STARTING POINT
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 130

    def getHealth(self):
        return self.healthbar_count

    #PASS IN +1 OR -1 TO INCREMENT / DECREMENT HEALTH BAR
    def setHealth(self, health):
        
        if health == 1: #INCREASE HEALTH UNLESS self.healthbar_count is at 0
            self.healthbar_count -= 1
            if self.healthbar_count < 0:
                self.healthbar_count = 0

        elif health == -1: #DECREASE HEALTH, UNLESS self.healthbar_count is at 5
            self.healthbar_count += 1
            if self.healthbar_count > 5:
                self.healthbar_count = 5

    def update(self):

        if score >= 300:
            self.image = self.healthbars[self.healthbar_count]
            self.image = pygame.transform.scale(self.image, (300, 100))
            self.image.set_colorkey(BLACK)
            draw_text(screen, "BOSS HEALTH: ", 15, 1200, 130)

            

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.explosion = [pygame.image.load(os.path.join(img_folder, "bubble_explo1.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo2.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo3.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo4.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo5.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo6.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo7.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo8.png")).convert(),
                          pygame.image.load(os.path.join(img_folder, "bubble_explo9.png")).convert()
                          ]
        self.explosion_count = 0
        self.image = self.explosion[self.explosion_count]
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = x
        self.rect.centery = y


    def update(self):
        self.image = self.explosion[self.explosion_count]
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)

        self.explosion_count += 1
        if self.explosion_count > 8:
            self.kill()


class Catchphrase(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(img_folder, "Catchphrase.png")).convert()
                        

        self.image = pygame.transform.scale(self.image, (100, 75))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = x
        self.rect.centery = y
        self.last_update = pygame.time.get_ticks()
        


    def update(self):
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)
        catchphrase = Catchphrase(player.getX(), player.getY())
        now = pygame.time.get_ticks()
        if now - self.last_update > 500:
            self.last_update = now
            self.kill()
        


             


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if score >= 150:
            PLAYER_ACC = 1.5

        #LOAD ANIMATIONS
        self.running_right = [pygame.image.load(os.path.join(img_folder, "character_robot_run0.png")).convert(),
                      pygame.image.load(os.path.join(img_folder, "character_robot_run1.png")).convert(),
                      pygame.image.load(os.path.join(img_folder, "character_robot_run2.png")).convert()
                     ]

        self.running_left = [pygame.image.load(os.path.join(img_folder, "character_robot_runleft0.png")).convert(),
                      pygame.image.load(os.path.join(img_folder, "character_robot_runleft1.png")).convert(),
                      pygame.image.load(os.path.join(img_folder, "character_robot_runleft2.png")).convert()
                     ]
        
        #SET UP ANIMATION COUNTS
        self.running_right_count = 0
        self.running_left_count = 0
        
        self.image = pygame.image.load(os.path.join(img_folder, "character_robot_idle.png")).convert()
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()



        self.pos = vec(750, GROUND - 60) 
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    
    def shootright(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bulletright(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullet_sound = mixer.Sound("laser5.wav")
            bullet_sound.play()
            bullets.add(bullet)
            self.mask = pygame.mask.from_surface(self.image)

    def shootleft(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bulletleft(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullet_sound = mixer.Sound("laser5.wav")
            bullet_sound.play()
            bullets.add(bullet)
            self.mask = pygame.mask.from_surface(self.image)

        
    def update(self):

        if score >= 500:
            player.shoot_delay = 1000 
        
        self.image.set_colorkey(BLACK)

        self.acc = vec(0, PLAYER_GRAV)
        
        #RETURNS A LIST, keystate, OF ALL PRESSED KEYS
        keystate = pygame.key.get_pressed()

        #CHECKS TO SEE WHICH KEYS WERE IN THE LIST (A.K.A PRESSED)
        if keystate[pygame.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        if keystate[pygame.K_LEFT]:
            self.acc.x += -PLAYER_ACC
        if keystate[pygame.K_UP]:
            self.rect.y += -5
        if keystate[pygame.K_DOWN]:
            self.rect.y += 5
        if self.vel.y == 0 and keystate[pygame.K_UP]:
            self.vel.y = -21
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_jump_left.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            if self.vel.x > 1:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_jump.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)

        if keystate[pygame.K_SPACE] and self.vel.x >= 0.000000001:
            self.shootright()

        self.rect.x += self.speedx


        if keystate[pygame.K_SPACE] and self.vel.x <= -0.00000001:
            self.shootleft()

        self.rect.x += self.speedx
                
        #ANIMATIONS

                #Fall
        if self.vel.y > 0 and self.vel.x > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_fall.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

                #Fall left
        if self.vel.y > 0 and self.vel.x < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_fall_left.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

                #Idle
        if self.vel.y == 0: 
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_idle.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            
                #Duck
        if keystate[pygame.K_DOWN]:
            if self.vel.y == 0 and self.acc.x == 0:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_duck.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)
                
                #Slide       #Not sure if to get rid of the slide animations
        if keystate[pygame.K_DOWN] and self.vel.x >= 2:
            if self.vel.y == 0:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_down.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)
            
                #Slide Left
        if keystate[pygame.K_DOWN] and self.vel.x <= -2:
            if self.vel.y == 0:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_down_left.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)

                #Run Right
        if keystate[pygame.K_RIGHT] and self.vel.y == 0:
            self.image = self.running_right[self.running_right_count]
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

            self.running_right_count += 1
            if self.running_right_count > 2:
                self.running_right_count = 0
                
                #Run Left
        if keystate[pygame.K_LEFT] and self.vel.y == 0:
            self.image = self.running_left[self.running_left_count]
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

            self.running_left_count += 1
            if self.running_left_count > 2:
                self.running_left_count = 0

        #APPLY FRICTION IN THE X DIRECTION
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #EQUATIONS OF MOTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #WRAP AROUND THE SIDES OF THE SCREEN
        if self.pos.x > WIDTH - 60:
            self.pos.x = WIDTH - 60
        if self.pos.x < 0 + 30:
            self.pos.x = 0 + 30

        #SIMULATE THE GROUND
        if self.pos.y > GROUND:
            self.pos.y = GROUND + 1
            self.vel.y = 0

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos

        #HITS PLATFORM
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.rect.top > hits[0].rect.top: #jumping from underneath
                self.vel.y = 0
            else:
                self.pos.y = hits[0].rect.top + 1 #jumping from above
                self.vel.y = 0

    
    def getX(self):
        return self.rect.centerx + 50

    def getY(self):
        return self.rect.centery - 50



class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienBeige_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienBeige_walk2.png")).convert()
                        ]

        self.running_count = 0
        
        self.image = self.running[self.running_count]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 1950
        self.rect.y = 695


        
    def update(self):
        
        if score >= 600:
            
            self.image = self.running[self.running_count]
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (175, 275))

            self.running_count += 1
            if self.running_count > 1:
                self.running_count = 0 

            self.rect.x += -2

            if self.rect.right < 0:
                self.rect.left = WIDTH

            self.mask = pygame.mask.from_surface(self.image)

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery





class Boss2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienGreen_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienGreen_walk2.png")).convert()
                        ]

        self.running_count = 0
        
        self.image = self.running[self.running_count]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 1950
        self.rect.y = 695


        
    def update(self):
        
        if score >= 300:
            
            self.image = self.running[self.running_count]
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (175, 275))

            self.running_count += 1
            if self.running_count > 1:
                self.running_count = 0 

            self.rect.x += 2

            if self.rect.left > WIDTH + 30:
                self.rect.right = 0

            self.mask = pygame.mask.from_surface(self.image)

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery
        

        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienBlue_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienBlue_walk2.png")).convert()
                        ]
                              
        self.running_count = 0
        
        self.image = self.running[self.running_count]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = WIDTH + 10
        self.rect.y = 895


        
    def update(self):
        
        self.image = self.running[self.running_count]
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (50, 75))

        self.running_count += 1
        if self.running_count > 1:
            self.running_count = 0 

        self.rect.x += -3

        if self.rect.right < 0:
            self.rect.left = WIDTH

        self.mask = pygame.mask.from_surface(self.image)

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

            

class Yellow2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienYellow_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienYellow_walk2.png")).convert()
                        ]
                              
        self.running_count = 0
       
        self.image = self.running[self.running_count]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = WIDTH + 20
        self.rect.y = 895

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery


        
    def update(self):
        
        self.image = self.running[self.running_count]
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (60, 80))

        self.running_count += 1
        if self.running_count > 1:
            self.running_count = 0 

        self.rect.x += -7

        if self.rect.right < 0:
            self.rect.left = WIDTH

        self.mask = pygame.mask.from_surface(self.image)

class Pink3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienPink_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienPink_walk2.png")).convert()
                        ]
                              
        self.running_count = 0
        self.image = self.running[self.running_count]
        self.image.set_colorkey(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = -80
        self.rect.y = 895


        
    def update(self):
        
        self.image = self.running[self.running_count]
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (60, 80))

        self.running_count += 1
        if self.running_count > 1:
            self.running_count = 0 

        self.rect.x += 3

        if self.rect.left > WIDTH:
            self.rect.left = 0
            
        self.mask = pygame.mask.from_surface(self.image)

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "shipBlue.png")).convert()
        self.image = pygame.transform.scale(self.image, (135, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 500
        self.rect.y = 850

    def update(self):

        self.rect.x += -5

        if self.rect.right < 0:
            self.rect.left = WIDTH

        self.mask = pygame.mask.from_surface(self.image)
        

class Platform2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "shipGreen.png")).convert()
        self.image = pygame.transform.scale(self.image, (135, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 900
        self.rect.y = 650

    def update(self):

        self.rect.x += +8

        if self.rect.left > WIDTH:
            self.rect.right = 0

        self.mask = pygame.mask.from_surface(self.image)



class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        meteor_image = pygame.image.load(os.path.join(img_folder, "meteorBig.png")).convert()
        self.image_orig = meteor_image
        self.image_orig = pygame.transform.scale(self.image_orig, (50, 50))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(7, 10)
        self.speedx = random.randrange(-5, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-7, 7 )
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            
        
    def update(self):
            self.rotate()
            
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right > WIDTH or self.rect.top > HEIGHT - 83 or self.rect.left < -45:
                self.kill()
                newMeteor()

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery



class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "Spaceship_all.png")).convert()
        self.image = pygame.transform.scale(self.image, (70, 135))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 800
        self.rect.y = 835
        self.mask = pygame.mask.from_surface(self.image)



class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bolt-icon-button-blue.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        

    def update(self):

            if score >= 200:


                self.rect.x += 5

                if self.rect.left > WIDTH:
                    self.kill()
                self.mask = pygame.mask.from_surface(self.image)

            else:
                self.rect.x = -100
                self.rect.y = random.randint(500, 900)

                

class Powerup2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bolt-icon-button-green.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        

    def update(self):

            if score >= 50:


                self.rect.x += 5

                if self.rect.left > WIDTH:
                    self.kill()
                self.mask = pygame.mask.from_surface(self.image)

            else:
                self.rect.x = -100
                self.rect.y = random.randint(500, 900)


class Enemyship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "sampleShip3.png")).convert()
        self.image = pygame.transform.scale(self.image, (105, 75))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 1500
        self.rect.y = 650

    def update(self):

        self.rect.x += -10

        if self.rect.right < 0:
            self.rect.left = WIDTH

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

        self.mask = pygame.mask.from_surface(self.image)

class Enemyship2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "sampleShip2.png")).convert()
        self.image = pygame.transform.scale(self.image, (105, 75))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = random.randrange(1000, 1500)
        self.rect.y = 10

    def update(self):

        self.rect.y += 10

        if self.rect.top > 900:
            self.rect.top = 1
            self.rect.x = random.randrange(200, 1300)
            self.rect.y += 10

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

        self.mask = pygame.mask.from_surface(self.image)
        

        
class Bulletright(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)
        
    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery
        
class Bulletleft(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "laserRed_left.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -20

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

    
#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("My Game")

#BACKGROUND MUSIC
mixer.music.load("Spacecrusher.ogg")

mixer.music.play()

clock = pygame.time.Clock()
draw_text(screen, str(score), 35, 1400, 5)
draw_text(screen, "SCORE: ", 35, 1200, 5)
#ADD BACKGROUND
bkgr_image = pygame.image.load(os.path.join(img_folder, "grid_bg.png")).convert()
background = pygame.transform.scale(bkgr_image, (WIDTH, HEIGHT))
background_rect = background.get_rect()
bkgr_x = 0

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()

player = Player()
powerup = Powerup()
powerup2 = Powerup2()

powerups = pygame.sprite.Group()
powerups.add(powerup)
powerups2 = pygame.sprite.Group()
powerups2.add(powerup2)

platform2 = Platform2()
platform = Platform()
platforms = pygame.sprite.Group()
platforms.add(platform, platform2)

rocket = Rocket()
obstacles = pygame.sprite.Group()
obstacles.add(rocket)

meteors = pygame.sprite.Group()

for i in range(5):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteors.add(meteor)

mob = Mob()

boss = Boss()
boss2 = Boss2()

alien_yellow = Yellow2()
aliens_yellow = pygame.sprite.Group()
aliens_yellow.add(alien_yellow)

alien_pink = Pink3()
aliens_pink = pygame.sprite.Group()
aliens_pink.add(alien_pink)

enemyship = Enemyship()
enemyships = pygame.sprite.Group()
enemyships.add(enemyship)
enemyship2 = Enemyship2()
enemyships2 = pygame.sprite.Group()
enemyships2.add(enemyship2)

mobs = pygame.sprite.Group()
mobs.add(mob)

bosses = pygame.sprite.Group()
bosses.add(boss)

bosses2 = pygame.sprite.Group()
bosses2.add(boss2)

bullets = pygame.sprite.Group()

healthBar = HealthBar()
enemy_healthBar = Enemy_HealthBar()




all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

def newMob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

def newYellow():
    alien_yellow = Yellow2()
    all_sprites.add(alien_yellow)
    aliens_yellow.add(alien_yellow)

def newPink():
    alien_pink = Pink3()
    all_sprites.add(alien_pink)
    aliens_pink.add(alien_pink)

def newMeteor():
    meteor = Meteor()
    all_sprites.add(meteor)
    meteors.add(meteor)

# GAME LOOP:
#   Process Events
#   Update
#   Draw

score = 0
start = True
end = True
running = True
while running:

    #BACKGROUND MUSIC


    #SHOW START SCREEN ONCE
    if start:
        mixer.music.stop()
        show_start_screen()
        start = False
        mixer.music.play(loops= -1)

    
    

    clock.tick(FPS)

    #PROCESS EVENTS
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keystate[pygame.K_q]:
            running = False

        if keystate[pygame.K_g] and keystate[pygame.K_a] and keystate[pygame.K_b] and keystate[pygame.K_e]:
            PLAYER_GRAV = 0.5
            PLAYER_FRICTION = -0.0095

        if keystate[pygame.K_1]:
            mixer.music.load("Spacecrusher.ogg")
            mixer.music.play()
            mixer.music.play(loops= -1)
        elif keystate[pygame.K_2]:
            mixer.music.load("Fun Background.mp3")
            mixer.music.play()
            mixer.music.play(loops= -1)

        elif keystate[pygame.K_3]:
            mixer.music.stop()

        
        if keystate[pygame.K_t]:
            catchphrase = Catchphrase(player.getX(), player.getY()) # x,y position of the player
            all_sprites.add(catchphrase)
            
      
            
            

    #CHECKS TO SEE IF LASER HITS MOB
    #BLUE ALIEN COLLISION
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        score += 10
        newMob()

        
    hits_ship = pygame.sprite.groupcollide(enemyships, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_ship:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        catchphrase = Catchphrase(player.getX(), player.getY() - 10)
        all_sprites.add(catchphrase)
        score += 30
        newMob()

    hit_obstacles = pygame.sprite.groupcollide(obstacles, bullets, False, True, pygame.sprite.collide_mask)
    for hit in hit_obstacles:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()

    hit_mob = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
    for hit in hit_mob:
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        newMob()
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                all_sprites = pygame.sprite.Group()
                player = Player()
                powerup = Powerup()
                powerup2 = Powerup2()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)
                powerups2 = pygame.sprite.Group()
                powerups2.add(powerup2)

                platform2 = Platform2()
                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform, platform2)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

                meteors = pygame.sprite.Group()

                for i in range(5):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

                mob = Mob()

                boss = Boss()

                alien_yellow = Yellow2()
                aliens_yellow = pygame.sprite.Group()
                aliens_yellow.add(alien_yellow)

                alien_pink = Pink3()
                aliens_pink = pygame.sprite.Group()
                aliens_pink.add(alien_pink)

                enemyship = Enemyship()
                enemyships = pygame.sprite.Group()
                enemyships.add(enemyship)

                mobs = pygame.sprite.Group()
                mobs.add(mob)

                bosses = pygame.sprite.Group()
                bosses.add(boss)

                bullets = pygame.sprite.Group()

                healthBar = HealthBar()
                enemy_healthBar = Enemy_HealthBar()

                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)


                score = 0


    #HITS ENEMY SHIP
    hit_ship = pygame.sprite.spritecollide(player, enemyships, True, pygame.sprite.collide_mask)
    for hit in hit_ship:
        enemyship.kill()
        newMob()
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                all_sprites = pygame.sprite.Group()
                player = Player()
                powerup = Powerup()
                powerup2 = Powerup2()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)
                powerups2 = pygame.sprite.Group()
                powerups2.add(powerup2)

                platform2 = Platform2()
                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform, platform2)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

                meteors = pygame.sprite.Group()

                for i in range(5):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

                mob = Mob()

                boss = Boss()

                alien_yellow = Yellow2()
                aliens_yellow = pygame.sprite.Group()
                aliens_yellow.add(alien_yellow)

                alien_pink = Pink3()
                aliens_pink = pygame.sprite.Group()
                aliens_pink.add(alien_pink)

                enemyship = Enemyship()
                enemyships = pygame.sprite.Group()
                enemyships.add(enemyship)

                mobs = pygame.sprite.Group()
                mobs.add(mob)

                bosses = pygame.sprite.Group()
                bosses.add(boss)

                bullets = pygame.sprite.Group()

                healthBar = HealthBar()
                enemy_healthBar = Enemy_HealthBar()

                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

                score = 0




    #YELLOW ALIEN COLLISION
    hit_yellow = pygame.sprite.spritecollide(player, aliens_yellow, True, pygame.sprite.collide_mask)
    for hit in hit_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        alien_yellow.kill()
        newYellow()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                all_sprites = pygame.sprite.Group()
                player = Player()
                powerup = Powerup()
                powerup2 = Powerup2()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)
                powerups2 = pygame.sprite.Group()
                powerups2.add(powerup2)

                platform2 = Platform2()
                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform, platform2)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

                meteors = pygame.sprite.Group()

                for i in range(5):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

                mob = Mob()

                boss = Boss()

                alien_yellow = Yellow2()
                aliens_yellow = pygame.sprite.Group()
                aliens_yellow.add(alien_yellow)

                alien_pink = Pink3()
                aliens_pink = pygame.sprite.Group()
                aliens_pink.add(alien_pink)

                enemyship = Enemyship()
                enemyships = pygame.sprite.Group()
                enemyships.add(enemyship)

                mobs = pygame.sprite.Group()
                mobs.add(mob)

                bosses = pygame.sprite.Group()
                bosses.add(boss)

                bullets = pygame.sprite.Group()

                healthBar = HealthBar()
                enemy_healthBar = Enemy_HealthBar()

                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

                score = 0





    hits_yellow = pygame.sprite.groupcollide(aliens_yellow, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        score += 20
        newYellow()




        
    #PINK ALIEN COLLISION
    hit_pink = pygame.sprite.spritecollide(player, aliens_pink, True, pygame.sprite.collide_mask)
    for hit in hit_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        newPink()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                all_sprites = pygame.sprite.Group()
                player = Player()
                powerup = Powerup()
                powerup2 = Powerup2()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)
                powerups2 = pygame.sprite.Group()
                powerups2.add(powerup2)

                platform2 = Platform2()
                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform, platform2)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

                meteors = pygame.sprite.Group()

                for i in range(5):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

                mob = Mob()

                boss = Boss()

                alien_yellow = Yellow2()
                aliens_yellow = pygame.sprite.Group()
                aliens_yellow.add(alien_yellow)

                alien_pink = Pink3()
                aliens_pink = pygame.sprite.Group()
                aliens_pink.add(alien_pink)

                enemyship = Enemyship()
                enemyships = pygame.sprite.Group()
                enemyships.add(enemyship)

                mobs = pygame.sprite.Group()
                mobs.add(mob)

                bosses = pygame.sprite.Group()
                bosses.add(boss)

                bullets = pygame.sprite.Group()

                healthBar = HealthBar()
                enemy_healthBar = Enemy_HealthBar()

                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

                score = 0


    hit_boss = pygame.sprite.spritecollide(player, bosses, True, pygame.sprite.collide_mask)
    if hit_boss:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        player.kill()
        if end:
            start = False
            mixer.music.stop()
            show_end_screen()
            all_sprites = pygame.sprite.Group()
            player = Player()
            powerup = Powerup()
            powerup2 = Powerup2()

            powerups = pygame.sprite.Group()
            powerups.add(powerup)
            powerups2 = pygame.sprite.Group()
            powerups2.add(powerup2)

            platform2 = Platform2()
            platform = Platform()
            platforms = pygame.sprite.Group()
            platforms.add(platform, platform2)

            rocket = Rocket()
            obstacles = pygame.sprite.Group()
            obstacles.add(rocket)

            meteors = pygame.sprite.Group()

            for i in range(5):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteors.add(meteor)

            mob = Mob()

            boss = Boss()

            alien_yellow = Yellow2()
            aliens_yellow = pygame.sprite.Group()
            aliens_yellow.add(alien_yellow)

            alien_pink = Pink3()
            aliens_pink = pygame.sprite.Group()
            aliens_pink.add(alien_pink)

            enemyship = Enemyship()
            enemyships = pygame.sprite.Group()
            enemyships.add(enemyship)

            mobs = pygame.sprite.Group()
            mobs.add(mob)

            bosses = pygame.sprite.Group()
            bosses.add(boss)

            bullets = pygame.sprite.Group()

            healthBar = HealthBar()
            enemy_healthBar = Enemy_HealthBar()

            all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)


            score = 0

    hit_meteor = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_mask)
    for hit in hit_meteor:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        newMeteor()
        newMeteor()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5:
            start = False
            mixer.music.stop()
            show_end_screen()
            all_sprites = pygame.sprite.Group()
            player = Player()
            powerup = Powerup()
            powerup2 = Powerup2()

            powerups = pygame.sprite.Group()
            powerups.add(powerup)
            powerups2 = pygame.sprite.Group()
            powerups2.add(powerup2)

            platform2 = Platform2()
            platform = Platform()
            platforms = pygame.sprite.Group()
            platforms.add(platform, platform2)

            rocket = Rocket()
            obstacles = pygame.sprite.Group()
            obstacles.add(rocket)

            meteors = pygame.sprite.Group()

            for i in range(5):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteors.add(meteor)

            mob = Mob()

            boss = Boss()

            alien_yellow = Yellow2()
            aliens_yellow = pygame.sprite.Group()
            aliens_yellow.add(alien_yellow)

            alien_pink = Pink3()
            aliens_pink = pygame.sprite.Group()
            aliens_pink.add(alien_pink)

            enemyship = Enemyship()
            enemyships = pygame.sprite.Group()
            enemyships.add(enemyship)

            mobs = pygame.sprite.Group()
            mobs.add(mob)

            bosses = pygame.sprite.Group()
            bosses.add(boss)

            bullets = pygame.sprite.Group()

            healthBar = HealthBar()
            enemy_healthBar = Enemy_HealthBar()

            explosion = Explosion(10, 100)
            catchphrase = Catchphrase(10, 100)

            all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor, explosion, catchphrase)

            score = 0



    hits_bosses = pygame.sprite.groupcollide(bosses, bullets, False, True, pygame.sprite.collide_mask)
    for hit in hits_bosses:
        enemy_healthBar.setHealth(-1)
        if enemy_healthBar.healthbar_count == 5:
            boss.kill()
            catchphrase = Catchphrase(player.getX(), player.getY())
            all_sprites.add(catchphrase)
            score += 500
            newPink()
            newYellow()
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)

        


    hits_pink = pygame.sprite.groupcollide(aliens_pink, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        score += 15
        newPink()

    
    hit_powerup = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
    if hit_powerup:
        powerup_sound = mixer.Sound("SFX_Powerup_01.wav")
        powerup_sound.play()
        powerup.kill()
        player.shoot_delay = 000

    hit_powerup2 = pygame.sprite.spritecollide(player, powerups2, True, pygame.sprite.collide_mask)
    if hit_powerup2 and score < 150:
        powerup_sound = mixer.Sound("SFX_Powerup_01.wav")
        powerup_sound.play()
        powerup2.kill()
        PLAYER_ACC = 3.5
        
    elif score >= 150: 
        PLAYER_ACC = 1.5
        
    elif score == 0:
        PLAYER_ACC = 1.5
        

    hits_meteor = pygame.sprite.groupcollide(meteors, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_meteor:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        score += 20
        newMeteor()

    #COMPLETE LEVEL
    if score >= 1500 and rounds < 1:
        rounds += 1
        score = 0
        show_newlevel_screen()
        all_sprites = pygame.sprite.Group()
        player = Player()
        powerup2 = Powerup2()

        powerups2 = pygame.sprite.Group()
        powerups2.add(powerup2)

        platform2 = Platform2()
        platform = Platform()
        platforms = pygame.sprite.Group()
        platforms.add(platform, platform2)

        rocket = Rocket()
        obstacles = pygame.sprite.Group()
        obstacles.add(rocket)

        meteors = pygame.sprite.Group()

        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteors.add(meteor)

        mob = Mob()

        boss = Boss()
        boss2 = Boss2()

        alien_yellow = Yellow2()
        aliens_yellow = pygame.sprite.Group()
        aliens_yellow.add(alien_yellow)
        all_sprites.add(alien_yellow)

        alien_pink = Pink3()
        aliens_pink = pygame.sprite.Group()
        aliens_pink.add(alien_pink)
        all_sprites.add(alien_pink)

        enemyship = Enemyship()
        enemyships = pygame.sprite.Group()
        enemyships.add(enemyship)
        enemyships2 = pygame.sprite.Group()
        enemyship2 = Enemyship2()
        enemyships2.add(enemyship2)

        mobs = pygame.sprite.Group()
        mobs.add(mob)

        bosses = pygame.sprite.Group()
        bosses.add(boss)
        
        boss2 = Boss2()
        bosses2 = pygame.sprite.Group()
        bosses2.add(boss2)

        healthBar = HealthBar()
        enemy_healthBar = Enemy_HealthBar()
        enemy2_healthBar = Enemy2_HealthBar()

        explosion = Explosion(10, 100)

        all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor, explosion, boss2, enemy2_healthBar, enemyship2)


    #PAUSE SCREEN
    if keystate[pygame.K_p]:
        show_pause_screen()
    #START FOR INFINITE MODE
    if keystate[pygame.K_8]:
        show_infinite_screen()
        score = 0
        rounds = 1.5
        all_sprites = pygame.sprite.Group()
        player = Player()
        powerup2 = Powerup2()

        powerups2 = pygame.sprite.Group()
        powerups2.add(powerup2)

        platform2 = Platform2()
        platform = Platform()
        platforms = pygame.sprite.Group()
        platforms.add(platform, platform2)

        rocket = Rocket()
        obstacles = pygame.sprite.Group()
        obstacles.add(rocket)

        meteors = pygame.sprite.Group()

        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteors.add(meteor)

        mob = Mob()

        boss = Boss()
        boss2 = Boss2()

        alien_yellow = Yellow2()
        aliens_yellow = pygame.sprite.Group()
        aliens_yellow.add(alien_yellow)
        all_sprites.add(alien_yellow)

        alien_pink = Pink3()
        aliens_pink = pygame.sprite.Group()
        aliens_pink.add(alien_pink)
        all_sprites.add(alien_pink)

        enemyship = Enemyship()
        enemyships = pygame.sprite.Group()
        enemyships.add(enemyship)
        enemyships2 = pygame.sprite.Group()
        enemyship2 = Enemyship2()
        enemyships2.add(enemyship2)

        mobs = pygame.sprite.Group()
        mobs.add(mob)

        bosses = pygame.sprite.Group()
        bosses.add(boss)
        
        boss2 = Boss2()
        bosses2 = pygame.sprite.Group()
        bosses2.add(boss2)

        healthBar = HealthBar()
        enemy_healthBar = Enemy_HealthBar()
        enemy2_healthBar = Enemy2_HealthBar()

        explosion = Explosion(10, 100)

        all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor, explosion, boss2, enemy2_healthBar, enemyship2)



    #COLLISION WITH LEVEL 2 BOSS
    hits_bosses2 = pygame.sprite.groupcollide(bosses2, bullets, False, True, pygame.sprite.collide_mask)
    for hit in hits_bosses2:
        enemy2_healthBar.setHealth(-1)
        if enemy2_healthBar.healthbar_count == 5:
            boss2.kill()
            score += 500
            newPink()
            newYellow()
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)

    hit_boss2 = pygame.sprite.spritecollide(player, bosses2, True, pygame.sprite.collide_mask)
    for hit in hit_boss2:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        player.kill()
        if end:
            start = False
            mixer.music.stop()
            show_end_screen()
            all_sprites = pygame.sprite.Group()
            player = Player()
            powerup = Powerup()
            powerup2 = Powerup2()

            powerups = pygame.sprite.Group()
            powerups.add(powerup)
            powerups2 = pygame.sprite.Group()
            powerups2.add(powerup2)

            platform2 = Platform2()
            platform = Platform()
            platforms = pygame.sprite.Group()
            platforms.add(platform, platform2)

            rocket = Rocket()
            obstacles = pygame.sprite.Group()
            obstacles.add(rocket)

            meteors = pygame.sprite.Group()

            for i in range(5):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteors.add(meteor)

            mob = Mob()

            boss = Boss()

            alien_yellow = Yellow2()
            aliens_yellow = pygame.sprite.Group()
            aliens_yellow.add(alien_yellow)

            alien_pink = Pink3()
            aliens_pink = pygame.sprite.Group()
            aliens_pink.add(alien_pink)

            enemyship = Enemyship()
            enemyships = pygame.sprite.Group()
            enemyships.add(enemyship)

            mobs = pygame.sprite.Group()
            mobs.add(mob)

            bosses = pygame.sprite.Group()
            bosses.add(boss)

            bullets = pygame.sprite.Group()

            healthBar = HealthBar()
            enemy_healthBar = Enemy_HealthBar()

            all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

            score = 0

    hit_enemyship2 = pygame.sprite.spritecollide(player, enemyships2, True, pygame.sprite.collide_mask)
    for hit in hit_enemyship2:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        explosion = Explosion(hit.getX(), hit.getY()) # x,y position of mob when it was hit
        all_sprites.add(explosion)
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5:
            start = False
            mixer.music.stop()
            show_end_screen()
            all_sprites = pygame.sprite.Group()
            player = Player()
            powerup = Powerup()
            powerup2 = Powerup2()

            powerups = pygame.sprite.Group()
            powerups.add(powerup)
            powerups2 = pygame.sprite.Group()
            powerups2.add(powerup2)

            platform2 = Platform2()
            platform = Platform()
            platforms = pygame.sprite.Group()
            platforms.add(platform, platform2)

            rocket = Rocket()
            obstacles = pygame.sprite.Group()
            obstacles.add(rocket)

            meteors = pygame.sprite.Group()

            for i in range(5):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteors.add(meteor)

            mob = Mob()

            boss = Boss()

            alien_yellow = Yellow2()
            aliens_yellow = pygame.sprite.Group()
            aliens_yellow.add(alien_yellow)

            alien_pink = Pink3()
            aliens_pink = pygame.sprite.Group()
            aliens_pink.add(alien_pink)

            enemyship = Enemyship()
            enemyships = pygame.sprite.Group()
            enemyships.add(enemyship)

            mobs = pygame.sprite.Group()
            mobs.add(mob)

            bosses = pygame.sprite.Group()
            bosses.add(boss)

            bullets = pygame.sprite.Group()

            healthBar = HealthBar()
            enemy_healthBar = Enemy_HealthBar()

            all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar, platform2, powerup2, meteor)

            score = 0
             

    if score >= 1700 and rounds == 1:
        show_win_screen()

    
    #Work on infinte mode
    
    # DRAW
    rel_x = bkgr_x % background.get_rect().width
    screen.blit(background, (rel_x - background.get_rect().width, 0))
    if rel_x < WIDTH:
        screen.blit(background, (rel_x, 0))
    bkgr_x -= 1

    # UPDATE
    all_sprites.update()
    
    all_sprites.draw(screen)
    draw_text(screen, "ROBOTS VS ALIENS", 24, 10, 10)
    draw_text(screen, "Arrow keys to move. Space to shoot", 20, 10, 35)
    draw_text(screen, str(score), 35, 850, 5)
    draw_text(screen, "SCORE: ", 35, 650, 5)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()
