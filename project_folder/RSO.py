# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

import pygame
import random
from os import path
# ==============================================================================
import datetime
import sys
##sys.stdout = open('out.txt', 'w')
##sys.stderr = open('out.txt', 'a')
print('\n','='*10, datetime.datetime.now(), '='*10)
# ==============================================================================
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

APP_VER = "0.01"
APP_NAME = "RSO v" + APP_VER
# POWERUP_TIME= 5000

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# fonts
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # 2й параметр - включение и отключение сглаживания
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, APP_NAME, 64, WIDTH / 2, HEIGHT / 4)
#     draw_text(screen, "Arrow keys move, Space to fire", 22,
#               WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(APP_NAME)
clock = pygame.time.Clock()

# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

ids = [111, 222, 333]


class Player(pygame.sprite.Sprite):
    def __init__(self, id, W, H, coordX, coordY, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((coordX, coordY))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.centerx = W
        self.rect.bottom = H


        self.id = id
       
    def update(self):
        pass
        
        
class GarbageBin(pygame.sprite.Sprite):
    def __init__(self, id):
        self.id = id

    def update(self):
        pass

class Action(pygame.sprite.Sprite):
    def __init__(self, id):
        self.id = id

    def update(self):
        pass




# =======================================================================
# pygame.mixer.music.play(loops=-1)

selected_rect = None
last_shot = 0
# =======================================================================
# GAME CYCLE
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
#         mobs = pygame.sprite.Group()
#         bullets = pygame.sprite.Group()
#         powerups = pygame.sprite.Group()
        player1 = Player("111", 300, 300, 30, 30, GREEN)
#         player2 = Player("222", 300, 200, YELLOW)
        all_sprites.add(player1)
#         all_sprites.add(player2)
        
#         for i in range(8):
#             newmob()
#         score = 0
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button)
            player1.color = RED
            player1.image.fill(player1.color)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            player1.color = GREEN
            player1.image.fill(player1.color)

        elif event.type == pygame.MOUSEMOTION:
            if player1.rect.collidepoint(event.pos):
                player1.color = BLUE
                player1.image.fill(player1.color)
                
                if event.buttons[0]:  # Left mouse button is down.
                    player1.rect.centerx += event.rel[0]
                    player1.rect.centery += event.rel[1]
                elif event.buttons[2]:
                    player1.rect.centerx -= event.rel[0]
                    player1.rect.centery -= event.rel[1]
            
            else:
                player1.color = GREEN
                player1.image.fill(player1.color)
         
        
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)


    # UPDATE
    all_sprites.update()

        # Проверка, не ударил ли моб игрока
    # короткий вариант
#               с использованием collide_rect()
#     hits = pygame.sprite.spritecollide(player, mobs, False)  # spritecollide (сравниваем ОДИН объект)
                # collide_rect() # Тип столкновения по умолчанию в Pygame (Axis-aligned Bounding Box)
                # collide_rect_ratio(koeff) # koeff < 1

#               с использованием collide_circle()
#     hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
                # collide_circle()

    # длинный вариант
#     hits = False
#     for mob in mobs:
#         if mob.rect.right > player.rect.left and \
#            mob.rect.left < player.rect.right and \
#            mob.rect.bottom > player.rect.top and \
#            mob.rect.top < player.rect.bottom:
#                hits = True
#                break

    # действие при столкновении игрока с мобом
#     for hit in hits:
#         player.shield -= hit.radius * 1 # коэфф.повреждений
#         newExplosion(hit.rect.center, 'sm')
#         newmob()
#         if player.shield <= 0:
#             death_explosion = Explosion(player.rect.center, 'player')
#             all_sprites.add(death_explosion)
#             player.hide()
#             player.lives -= 1
#             player.shield = 100

    # Если игрок умер, игра окончена
#     if player.lives == 0 and not death_explosion.alive(): # alive() сообщает, является ли конкретный спрайт живым
#         game_over = True
            
            
    

    # Проверка попадания пуль в мобов
#     hits = pygame.sprite.groupcollide(mobs, bullets, True, True)  # groupcollide (сравниваем ГРУППУ объектов)
#     for hit in hits:
#         score += 50 - hit.radius
#         random.choice(expl_sounds).play()
#         newExplosion(hit.rect.center, 'lg')
#         if random.random() > 0.9:
#             pow = Pow(hit.rect.center)
#             all_sprites.add(pow)
#             powerups.add(pow)
#         newmob()            #  при уничтожении моба - создаем нового
        
#               Тренировочный вариант:
#         c1 = random.randrange(0, 255)
#         c2 = random.randrange(0, 255)
#         c3 = random.randrange(0, 255)
#         hit.image.fill((c1, c2, c3))


    # Проверка столкновений игрока и улучшения
#     hits = pygame.sprite.spritecollide(player, powerups, True)
#     for hit in hits:
#         if hit.type == 'shield':
#             player.shield += random.randrange(10, 30)
#             if player.shield >= 100:
#                 player.shield = 100
#             shield_sound.play()
#         if hit.type == 'gun':
#             player.powerup()
#             power_sound.play()


    # RENDERING
    screen.fill(BLACK)
    screen.blit(background, background_rect) # обозначает прорисовку пикселей одного изображения на другом. В этом случае — прорисовку фона на экране.

    all_sprites.draw(screen)
#     draw_text(screen, str(score), 24, WIDTH / 2, 10)
#     draw_text(screen, str(len(mobs)), 30, WIDTH / 1.4, 10)
#     draw_text(screen, str(pygame.time.get_ticks()), 24, WIDTH / 2, 38)
#     draw_shield_bar(screen, 5, 5, player.shield)
#     draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    # FLIP
    pygame.display.flip()

pygame.quit()
