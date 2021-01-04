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

#BACKGROUND
#start_background = pygame.image.load(os.path.join(img_folder, "platform_background.png")).convert()
#start_background_rect = (WIDTH / 2, HEIGHT / 2)

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
    draw_text(screen, "Robot", 64, WIDTH / 2 - 200, HEIGHT / 4)
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
                print("Key pressed to start the game!")
                waiting = False
    


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



        self.pos = vec(750, GROUND - 60) #10?
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
                self.pos.y = GROUND
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

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bolt-icon-button-blue.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = random.randint(100, 800)
        self.rect.y = random.randint(300, 1000)

    def update(self):

        self.rect.x += 3

        if self.rect.left > WIDTH:
            self.kill()

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
powerup = Powerup()
powerups = pygame.sprite.Group()
powerups.add(powerup)
platform = Platform()
platforms = pygame.sprite.Group()
platforms.add(platform)
mob = Mob()
alien_yellow = Yellow2()
aliens_yellow = pygame.sprite.Group()
aliens_yellow.add(alien_yellow)
alien_pink = Pink3()
aliens_pink = pygame.sprite.Group()
aliens_pink.add(alien_pink)
enemyship = Enemyship()
mobs = pygame.sprite.Group()
mobs.add(mob, enemyship)
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, platform, mob, enemyship, alien_yellow, alien_pink, powerup)

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

# GAME LOOP:
#   Process Events
#   Update
#   Draw

score = 0
start = True
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

    # UPDATE
    all_sprites.update()

    #CHECKS TO SEE IF LASER HITS MOB
    #BLUE ALIEN COLLISION
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 10
        newMob()

    hit_mob = pygame.sprite.spritecollide(player, mobs, False)
    if hit_mob:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        player.kill()
        running = False

    #YELLOW ALIEN COLLISION
    hit_yellow = pygame.sprite.spritecollide(player, aliens_yellow, False)
    if hit_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        player.kill()
        running = False

    hits_yellow = pygame.sprite.groupcollide(aliens_yellow, bullets, True, True)
    for hit in hits_yellow:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 20
        newYellow()
        
    #PINK ALIEN COLLISION
    hit_pink = pygame.sprite.spritecollide(player, aliens_pink, False)
    if hit_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        player.kill()
        running = False

    hits_pink = pygame.sprite.groupcollide(aliens_pink, bullets, True, True)
    for hit in hits_pink:
        explosion_sound = mixer.Sound("explosion.wav")
        explosion_sound.play()
        score += 15
        newPink()

    hit_powerup = pygame.sprite.spritecollide(player, powerups, False)
    if hit_powerup:
        #powerup_sound = mixer.Sound("Picked_Coin_Echo.wav")
        #powerup_sound.play()
        powerup.kill()
        player.shoot_delay = 000 # WORK ON THIS SHOOT DELAY = 0
       

    # DRAW
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "PLATFORMER", 24, 10, 10)
    draw_text(screen, "Arrow keys to move. Space to shoot", 20, 10, 35)
    draw_text(screen, str(score), 35, 1400, 5)
    draw_text(screen, "SCORE: ", 35, 1200, 5)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()



