import pygame, sys
import random
import os
from pygame import mixer
                                   
WIDTH = 1500
HEIGHT = 1000
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8

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

#BACKGROUND
#background = pygame.image.load(os.path.join(img_folder, "space.png")).convert()


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



        self.pos = vec(10, GROUND - 60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 500
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

    def shootleft(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bulletleft(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullet_sound = mixer.Sound("laser5.wav")
            bullet_sound.play()
            bullets.add(bullet)

        
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
        if self.vel.y == 0: #and self.acc.x == 0:
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
                self.pos.y = hits[0].rect.bottom + 25 + 1
                self.vel.y = 0
            else:
                self.pos.y = hits[0].rect.top + 1 #jumping from above
                self.vel.y = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.running = [pygame.image.load(os.path.join(img_folder, "alienBlue_walk1.png")).convert(),
                        pygame.image.load(os.path.join(img_folder, "alienBlue_walk2.png")).convert()
                        ]
                              
        self.running_count = 0
        
        self.image = self.running[self.running_count]
        #self.image = pygame.transform.scale(self.image, (10, 10))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 1000
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


class Bulletright(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

            

class Bulletleft(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "laserRed_left.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()


    
#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

#BACKGROUND MUSIC
mixer.music.load("Spacecrusher.ogg")
mixer.music.play()

clock = pygame.time.Clock()

#ADD BACKGROUND
bkgr_image = pygame.image.load(os.path.join(img_folder, "space.png")).convert()
background = pygame.transform.scale(bkgr_image, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#SPRITE GROUPS

player = Player()
platform = Platform()
platforms = pygame.sprite.Group()
platforms.add(platform)
mob = Mob()
mobs = pygame.sprite.Group()
mobs.add(mob)
bullets = pygame.sprite.Group()
enemy_ship = Enemyship()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, platform, mob, enemy_ship)



# GAME LOOP:
#   Process Events
#   Update
#   Draw
running = True
while running:

    

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # UPDATE
    all_sprites.update()

    #CHECKS TO SEE IF LASER HITS MOB
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()

    # DRAW
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "PLATFORMER", 24, 10, 10)
    draw_text(screen, "Arrow keys to move. Space to shoot", 20, 10, 35)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()



