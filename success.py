import pygame
import random
import os
#won't change if using capital char
FPS = 60 # 60 times per second
WIDTH,HEIGHT = 900, 500

WHITE = (255,255,255) #use RGB colors setting
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0) 
BLACK = (0,0,0)
pygame.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('POP CAT--your best friend')
icon_img = pygame.image.load(os.path.join('picture','icon.tiff')).convert()
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock() 
 # upload the picture
background_jpg = pygame.image.load(os.path.join('picture','background.jpg')).convert()
player_png1 = pygame.image.load(os.path.join('picture','pop_cat.png')).convert()
player_png2 = pygame.image.load(os.path.join('picture','pop_cat2.png')).convert()
player_mini_img = pygame.transform.scale(player_png1, (25,19))
player_mini_img.set_colorkey(BLACK)

#rock_png = pygame.image.load(os.path.join('picture','rock.png')).convert()
bullet_png = pygame.image.load(os.path.join('picture','bullet.png')).convert()
rock_imgs = []
for i in range(11):
    rock_imgs.append(pygame.image.load(os.path.join('picture' ,f'rock{i}.png')).convert())
# import font
font_name = pygame.font.match_font('arial')
shoot_sound =  pygame.mixer.Sound(os.path.join('sound', 'pop-cat-sound.mp3'))
die_sound =  pygame.mixer.Sound(os.path.join('sound', 'die.ogg'))
die_sound.set_volume(0.3)
coin_sound =  pygame.mixer.Sound(os.path.join('sound', 'collectcoin-6075.ogg'))
shield_sound =  pygame.mixer.Sound(os.path.join('sound', 'pow0.wav'))
shield_sound.set_volume(0.5)
bonus_sound =  pygame.mixer.Sound(os.path.join('sound', 'pow1.wav'))
bonus_sound.set_volume(0.3)
expl_sounds = [
    pygame.mixer.Sound(os.path.join('sound','expl0.wav')),
    pygame.mixer.Sound(os.path.join('sound','expl1.wav'))
]
for snd in expl_sounds:  
    snd.set_volume(0.3)
 
pygame.mixer.music.load(os.path.join('sound', 'Wii-Music_.ogg'))
pygame.mixer.music.set_volume(0.5) 

expl_anim = {}  
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join('picture', f'expl{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(40,40)))
    player_expl_img = pygame.image.load(os.path.join('picture', f'player_expl{i}.png')).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_img = {}
power_img['shield'] = pygame.image.load(os.path.join('picture', 'shield.png')).convert()
power_img['shield'] = pygame.transform.scale(power_img['shield'], (50,50))
power_img['bonus'] = pygame.image.load(os.path.join('picture', 'bonus.png')).convert()
power_img['bonus'] = pygame.transform.scale(power_img['bonus'], (50,50))
power_img['coin'] = pygame.image.load(os.path.join('picture', 'coin.png')).convert()
power_img['coin'] = pygame.transform.scale(power_img['coin'], (70,70))
def new_rock():
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)
        
def draw_helth(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def draw_lives(surf, lives, img, x, y):   
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i  # 30p
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_text(surf ,text ,size, x, y): 
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
       
class Bullet(pygame.sprite.Sprite):
    def __init__(self ,x ,y): # get yhe parameter of spaceship
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_png, (80,30))
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((10,20)) 
        # self.image.fill(YELLOW) 
        self.rect = self.image.get_rect() # get the position with boundary
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = 10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.top < 0 :
            self.kill()
                     
class Explosion(pygame.sprite.Sprite):      
    def __init__(self ,center ,size): # get yhe parameter of spaceship
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect() # get the position with boundary
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
                
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori = pygame.transform.scale(self.image_ori, (70,70))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() # get the position with boundary
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(900, 1000)
        self.rect.y = random.randrange(0, HEIGHT-self.rect.width) #coordinate
        self.speedx = random.randrange(2,12)
        self.speedy = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-2,2)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self):
        self.rotate()
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.x = random.randrange(900, 1000)
            self.rect.y = random.randrange(0, HEIGHT-self.rect.width) #coordinate
            self.speedx = random.randrange(3,12)
            self.speedy = random.randrange(-3,3)
            
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_png1, (40,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # get the position with boundary
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center ,self.radius )
        self.rect.x = 200
        self.rect.y = 200 # coordinate
        self.speed = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
            self.gun = 1
            self.gun_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 2000: # 2000 ms
            self.hidden = False
            self.rect.x = 200
            self.rect.y = 200 # reposition
            
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        # confine to the window #
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet)    
                bullets.add(bullet)  
                shoot_sound.play() 
            elif self.gun >= 2:
                #bonus 
                bullet1 = Bullet(self.rect.centerx, self.rect.centery)
                bullet2 = Bullet(self.rect.bottom, self.rect.bottom)
                all_sprites.add(bullet1)    
                all_sprites.add(bullet2) 
                bullets.add(bullet1)  
                bullets.add(bullet2)  
                shoot_sound.play() 
                
             
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
        
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','bonus','coin'])
        self.image = power_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -3
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0 :
            self.kill()
 

    
def draw_init():
    WIN.blit(background_jpg, (0,0)) 
    draw_text(WIN, 'POP CAT ! Your best friend !',64,WIDTH/2,HEIGHT/4)
    draw_text(WIN, 'Arrow keys to move and space to shoot', 30, WIDTH/2, HEIGHT/2)
    draw_text(WIN, 'Press any key to continue...', 25, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:  
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
                
#screen
def draw_window():
    #WIN.fill(white)
    WIN.blit(background_jpg, (0,0)) 
    all_sprites.draw(WIN) 
    draw_text(WIN, str(score), 20, WIDTH/2, 10)
    draw_helth(WIN, player.health, 5, 15)
    draw_lives(WIN, player.lives, player_mini_img, WIDTH-100, 15)
    draw_text(WIN, 'Coin: X'+str(coin), 20, 150, 15)
    pygame.display.update() #updating automatically


pygame.mixer.music.play(-1)
###############################################################################
show_init = True
run = True
while run:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group() #this group can store lots of sprites object
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            new_rock()
        score = 0
        coin = 0
    clock.tick(FPS) # control the speed of the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.image = pygame.transform.scale(player_png2, (40,60))
                player.image.set_colorkey(BLACK)
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.image = pygame.transform.scale(player_png1, (40,60))
                player.image.set_colorkey(BLACK)
                
    draw_window()
    all_sprites.update() 
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # return a dict {hit rock :hit bullet}
    # the third and forth represents whether to elimate the object
    for hit in hits: # how many rocks are elimated ,add the same amount of them
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    if player.hidden == False:
        hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) # bool: whether rocks should be elimated
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 5
            if player.health > 100 :
                player.health = 100
            shield_sound.play()
        elif hit.type == 'bonus':
            player.gunup()
            bonus_sound.play()
        elif hit.type == 'coin':
            coin += 1
            coin_sound.play()
        
    if player.lives == 0 and not(death_expl.alive()):
        show_init = True
    
        #run = False
pygame.quit()   

