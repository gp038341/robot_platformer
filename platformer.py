import pygame, sys
import random
import os
import time
from pygame import mixer
                                   
WIDTH = 1500
HEIGHT = 1000
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8
score = 0

#CONSTANTS - PHYSICS
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.12
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
    screen.fill(BLACK)
    draw_text(screen, "ROBOTS VS ALIENS", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, space to shoot", 22, WIDTH / 2 - 200, HEIGHT / 2)
    draw_text(screen, "Press a key to begin...", 18, WIDTH / 2 - 200, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_end_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH / 2 - 200, HEIGHT / 4)
    draw_text(screen, "Press ENTER to try again", 22, WIDTH / 2 - 200, HEIGHT / 2 + 200)
    draw_text(screen, str(score), 35, 850, 500)
    draw_text(screen, "FINAL SCORE: ", 35, 550, 500)
    pygame.display.flip()
    waiting = True
    while waiting:
        time.sleep(1.55)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                mixer.music.play()


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

        if score >= 500:
            self.image = self.healthbars[self.healthbar_count]
            self.image = pygame.transform.scale(self.image, (300, 100))
            self.image.set_colorkey(BLACK)
            draw_text(screen, "BOSS HEALTH: ", 15, 1200, 60)


                


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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
                
                #Slide
        if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT] and self.vel.y == 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_down.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            
                #Slide Left
        if keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT] and self.vel.y == 0:
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
        if self.pos.x > WIDTH - 30:
            self.pos.x = WIDTH - 30
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
                self.pos.y = GROUND
                self.vel.y = 0
            else:
                self.pos.y = hits[0].rect.top + 1 #jumping from above
                self.vel.y = 0

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
        self.rect.x = 1500
        self.rect.y = 695


        
    def update(self):
        
        if score >= 500:
            
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
        self.rect.x = 1500
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
        self.rect.x = 1500
        self.rect.y = 895


        
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
        self.rect.x = random.randint(100, 400)
        self.rect.y = random.randint(500, 900)


    def update(self):

        self.rect.x += 3

        if self.rect.left > WIDTH:
            self.kill()
        self.mask = pygame.mask.from_surface(self.image)            

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

    
#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

#BACKGROUND MUSIC
mixer.music.load("Spacecrusher.ogg")

mixer.music.play()

clock = pygame.time.Clock()
draw_text(screen, str(score), 35, 1400, 5)
draw_text(screen, "SCORE: ", 35, 1200, 5)
#ADD BACKGROUND
bkgr_image = pygame.image.load(os.path.join(img_folder, "space.png")).convert()
background = pygame.transform.scale(bkgr_image, (WIDTH, HEIGHT))
background_rect = background.get_rect()
bkgr_x = 0

#SPRITE GROUPS

player = Player()
powerup = Powerup()

powerups = pygame.sprite.Group()
powerups.add(powerup)

platform = Platform()
platforms = pygame.sprite.Group()
platforms.add(platform)

rocket = Rocket()
obstacles = pygame.sprite.Group()
obstacles.add(rocket)

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

all_sprites = pygame.sprite.Group()
all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

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

def newBoss():
    boss = Boss()
    all_sprites.add(boss)
    bosses.add(boss)

# GAME LOOP:
#   Process Events
#   Update
#   Draw

score = 0
start = True
end = True
running = True
while running:

    #SHOW START SCREEN ONCE
    if start:
        mixer.music.stop()
        show_start_screen()
        start = False
        mixer.music.play()

    

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #CHECKS TO SEE IF LASER HITS MOB
    #BLUE ALIEN COLLISION
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 10
        newMob()

        
    hits_ship = pygame.sprite.groupcollide(enemyships, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_ship:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 30
        newMob()

    hit_obstacles = pygame.sprite.groupcollide(obstacles, bullets, False, True, pygame.sprite.collide_mask)
    for hit in hit_obstacles:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()

    hit_mob = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
    if hit_mob:
        mob.kill()
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
                player = Player()
                powerup = Powerup()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)

                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

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

                all_sprites = pygame.sprite.Group()
                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

                score = 0


    #HITS ENEMY SHIP
    hit_ship = pygame.sprite.spritecollide(player, enemyships, True, pygame.sprite.collide_mask)
    if hit_ship:
        enemyship.kill()
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
                player = Player()
                powerup = Powerup()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)

                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

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

                all_sprites = pygame.sprite.Group()
                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

                score = 0




    #YELLOW ALIEN COLLISION
    hit_yellow = pygame.sprite.spritecollide(player, aliens_yellow, True, pygame.sprite.collide_mask)
    if hit_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        alien_yellow.kill()
        newYellow()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                player = Player()
                powerup = Powerup()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)

                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

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

                all_sprites = pygame.sprite.Group()
                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

                score = 0





    hits_yellow = pygame.sprite.groupcollide(aliens_yellow, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 20
        newYellow()




        
    #PINK ALIEN COLLISION
    hit_pink = pygame.sprite.spritecollide(player, aliens_pink, True, pygame.sprite.collide_mask)
    if hit_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        alien_pink.kill()
        newPink()
        healthBar.setHealth(-1)
        if healthBar.healthbar_count == 5: 
            player.kill()
            if end:
                start = False
                mixer.music.stop()
                show_end_screen()
                player = Player()
                powerup = Powerup()

                powerups = pygame.sprite.Group()
                powerups.add(powerup)

                platform = Platform()
                platforms = pygame.sprite.Group()
                platforms.add(platform)

                rocket = Rocket()
                obstacles = pygame.sprite.Group()
                obstacles.add(rocket)

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

                all_sprites = pygame.sprite.Group()
                all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

                score = 0


    hit_boss = pygame.sprite.spritecollide(player, bosses, True, pygame.sprite.collide_mask)
    if hit_boss:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play() 
        player.kill()
        if end:
            start = False
            mixer.music.stop()
            show_end_screen()
            player = Player()
            powerup = Powerup()

            powerups = pygame.sprite.Group()
            powerups.add(powerup)

            platform = Platform()
            platforms = pygame.sprite.Group()
            platforms.add(platform)

            rocket = Rocket()
            obstacles = pygame.sprite.Group()
            obstacles.add(rocket)

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

            all_sprites = pygame.sprite.Group()
            all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup, rocket, healthBar, boss, enemy_healthBar)

            score = 0


    hits_bosses = pygame.sprite.groupcollide(bosses, bullets, False, True, pygame.sprite.collide_mask)
    for hit in hits_bosses:
        enemy_healthBar.setHealth(-1)
        if enemy_healthBar.healthbar_count == 5:
            boss.kill()
            score += 500
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        


    hits_pink = pygame.sprite.groupcollide(aliens_pink, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 15
        newPink()

    
    hit_powerup = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
    if hit_powerup:
        #powerup_sound = mixer.Sound("Picked_Coin_Echo.wav")
        #powerup_sound.play()
        powerup.kill()
        player.shoot_delay = 000 # WORK ON THIS SHOOT DELAY = 0        

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



