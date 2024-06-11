import pygame
import random
import time
import math

screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption('Avoid Enemies')

clock = pygame.time.Clock()
FPS = 60

black = (0, 0, 0)
white = (255, 255, 255)
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)

running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image = pygame.image.load("Programing/Python/Enemies/spaceship.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(center = (360, 240))
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 720:
            self.rect.right = 720
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 480:
            self.rect.bottom = 480

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image = pygame.image.load("Programing/Python/Enemies/bulet.png")
        self.image = pygame.transform.scale(self.image, (10,10))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        # self.speedy = pygame.mouse.get_pos()[1] / 100
        # self.speedx = pygame.mouse.get_pos()[0] / 100
        self.speed = 0.05
        self.target = mouse_pos
        self.direction = pygame.math.Vector2(self.target[0] - self.rect.centerx, self.target[1] - self.rect.centery)
        self.direction.normalize()
        self.directionx = self.target[0] - self.rect.centerx
        self.directiony = self.target[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(-self.directionx, -self.directiony))
        self.vector = round(self.direction * self.speed)
        # self.angle = self.direction.angle_to(pygame.math.Vector2(1,2))
        self.image = pygame.transform.rotate(self.image, self.angle)
        # if self.angle > 315 or self.angle < 45:
        #     self.image = pygame.Surface((5, 10))
        # if self.angle > 45 and self.angle < 135:
        #     self.image = pygame.Surface((10, 5))
        # if self.angle > 315 and self.angle < 45:
        #     self.image = pygame.Surface((5, 10))
        # if self.angle > 315 or self.angle < 45:
        #     self.image = pygame.Surface((5, 10))

    
    def update(self):
        # self.rect.y += self.speed * self.direction.y
        # self.rect.x += self.speed * self.direction.x
        if self.vector == [0,0]:
            self.vector = [0,1]
        self.rect.move_ip(self.vector)
        if self.rect.bottom <= 0:
            self.kill()
        print(self.vector)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image = pygame.image.load("Programing/Python/Enemies/enemy.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(670)
        self.rect.y = 0
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.randomnum = random.randrange(0, 2)

    def update(self):
        if self.randomnum == 1:
            self.rect.x += self.speedx 
        self.rect.y += self.speedy
        if self.rect.x <= 0 or self.rect.x >= 670:
            self.speedx *= -1
        if self.rect.y > 480:
            self.kill()
            count()

def count():
    global enemy_count
    enemy_count += 1

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemy_count = 0
enemy_timer = 0
paused = False
bullet_time = 0
bullet_time_text = "3"


while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(black)
    bullet_time += 1
    mouse_pos = pygame.mouse.get_pos()

    if bullet_time >= 0 and bullet_time <= 60:
        bullet_time_text = "3"
    if bullet_time == 60:
        bullet_time_text = "2"
    if bullet_time == 120:
        bullet_time_text = "1"
    if bullet_time >= 180:
        bullet_time_text = "0"


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.velocity[1] = -200 * dt
            elif event.key == pygame.K_s:
                player.velocity[1] = 200 * dt
            elif event.key == pygame.K_a:
                player.velocity[0] = -200 * dt
            elif event.key == pygame.K_d:
                player.velocity[0] = 200 * dt
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0
            elif event.key == pygame.K_RETURN and paused:
                paused = False
                enemy_count = 0
                enemies.empty()
                all_sprites.empty()
                player.rect.center = (720/2, 480/2)
                all_sprites.add(player)
        elif pygame.mouse.get_pressed() == (True, False, False):
            if bullet_time >= 180:
                bullet = Bullet(player.rect.x + 25, player.rect.y, mouse_pos)
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullet_time = 0

    if not paused:
        enemy_timer += dt
        if enemy_timer > 1:
            enemy_timer = 0
            new_enemy = Enemy()
            #enemies.add(new_enemy)
            #all_sprites.add(new_enemy)
        player.update()
        #enemies.update()
        bullets.update()
        screen.blit(player.image, player.rect)
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)
        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)
            if pygame.sprite.spritecollide(bullet, enemies, dokill=True):
                enemy_count += 1
                bullet.kill()
        enemy_count_text = myfont.render('Enemies Passed: {}'.format(enemy_count), False, (255, 255, 255))
        screen.blit(enemy_count_text, (430, 0))
        cooldown_text = myfont.render('Cooldown: {}'.format(bullet_time_text), False, (255, 255, 255))
        screen.blit(cooldown_text, (230, 0))
        if pygame.sprite.spritecollide(player, enemies, dokill=False):
            paused = True
    else:
        paused_text = myfont.render('Enemies Passed: {}'.format(enemy_count), False, (255, 255, 255))
        screen.blit(paused_text, (240 ,220))

    pygame.display.update()

pygame.quit()