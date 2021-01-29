# Some of the sounds in this project were created by David McKee (ViRiX) soundcloud.com/virix

# import sys
import random as r
import pygame
from os import path
import csv

r'''
# Python
# "C:\Users\Yuriy\AppData\Local\Programs\Python\Python38-32\python.exe" "%File%"
# %FilePath% out.txt
'''

# with open('out.txt') as f:
#    n = int(f.readline().rstrip())
# 
# sys.stdout = open('out.txt', 'w')
# sys.stderr = open('out.txt', 'a')
# print(n + 1)

# ==============================================================================
import datetime
import sys

##sys.stdout = open('out.txt', 'w')
##sys.stderr = open('out.txt', 'a')
print('\n', '=' * 10, datetime.datetime.now(), '=' * 10)
# ==============================================================================

WIDTH, HEIGHT = 900, 600
FPS = 30

APP_VER = "0.02"
APP_NAME = "RSO v" + APP_VER

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# fonts
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y, place="center"):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLUE)
    text_rect = text_surface.get_rect()
    if place == "center":
        text_rect.center = (x, y)
    elif place == "left":
        text_rect.left = x
        text_rect.y = y
    surf.blit(text_surface, text_rect)

def draw_img(img, width, height):
    bin_img = pygame.image.load(path.join(img_dir, img)).convert()
    bin_mini_img = pygame.transform.scale(bin_img, (width, height))
    bin_mini_img.set_colorkey(BLACK)
    return bin_mini_img



def show_go_screen():
    # screen.blit(background, background_rect)
    screen.fill(BLACK)
    draw_text(screen, APP_NAME, 64, WIDTH / 2, HEIGHT / 4)
    #     draw_text(screen, "Arrow keys move, Space to fire", 22,
    #               WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    last_key = 0
    while waiting:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if last_key == 0:
                last_key = now
            if now - last_key > 200:
                if event.type == pygame.KEYUP:
                    last_key = now
                    waiting = False


player_data = {}
with open('data/players.csv') as f:
    f.readline()
    reader = csv.reader(f) 
    for row in reader:
        player_data[row[0]] = row[1:]


def new_player():
    rand_pl = r.choice(list(player_data.keys()))
    print(rand_pl)
    player = Player(rand_pl, player_data[rand_pl], 30, 40, WIDTH * 0.50, HEIGHT * 0.50, GREEN)
    all_sprites.add(player)
    return player

def new_bin(id_, x, y):
    bin = GarbageBin(str(id_), bins[str(id_)], 200, 240, x, y, YELLOW)
    bins_group.add(bin)
    all_sprites.add(bin)

def new_act(id_, x, y):
    act = Action(str(id_), acts[str(id_)], 100, 120, x, y, WHITE)
    actions_group.add(act)
    all_sprites.add(act)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(APP_NAME)
clock = pygame.time.Clock()

# sound
snd_dir = path.join(path.dirname(__file__), 'snd')
sound_ok = pygame.mixer.Sound(path.join(snd_dir, '1.wav'))
sound_bad = pygame.mixer.Sound(path.join(snd_dir, '2.wav'))
sound_water = pygame.mixer.Sound(path.join(snd_dir, '3.mp3'))
sound_scissors = pygame.mixer.Sound(path.join(snd_dir, '4.mp3'))

# =========== read from CSV =========================


bins = {}
with open('data/bins.csv') as f:  # TODO переместить файл в папку 'data'
    f.readline()
    reader = csv.reader(f)
    for row in reader:
        bins[row[0]] = row[1:]
# print(bins)

acts = {}
with open('data/acts.csv') as f:  # TODO переместить файл в папку 'data'
    f.readline()
    reader = csv.reader(f)
    for row in reader:
        acts[row[0]] = row[1:]
# print(acts)


# Загрузка всей игровой графики
img_dir = path.join(path.dirname(__file__), 'img')
# background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
# background_rect = background.get_rect()

# Попробую назначать img при инициализации Player
# player_img = {}
# for i in player_data:
#     filename = player_data[i][1]
#     img = pygame.image.load(path.join(img_dir, filename)).convert()
#     img.set_colorkey(BLACK)
#     img_small = pygame.transform.scale(img, (75, 75))
#     player_img(player_data[0]) = player_data[1]
# 
# print(player_img)

class Player(pygame.sprite.Sprite):
    def __init__(self, id_, player_data, W, H, coordX, coordY, color=RED):
        super(Player, self).__init__()

        self.id_ = id_
        self.img = player_data[0]
        self.fit_acts = self.fit_seq(player_data[1])
        self.bonus_acts = player_data[2]
        self.fit_bin = player_data[3]

        player_img = pygame.image.load(path.join(img_dir, self.img)).convert()
        player_mini_img = pygame.transform.scale(player_img, (30, 100))
        player_mini_img.set_colorkey(BLACK)
        self.image = player_mini_img

        self.rect = self.image.get_rect()
        self.rect.center = (coordX, coordY)
        
    def fit_seq(self, acts):
        res = acts.split('_')
        print(res)
        return res
        


class GarbageBin(pygame.sprite.Sprite):
    def __init__(self, id_, bins, W, H, coordX, coordY, color=YELLOW):
        super(GarbageBin, self).__init__()
        self.id_ = id_
        self.img1 = bins[0]
        self.img2 = bins[1]
        self.image = draw_img(self.img1, int(80*0.8), int(140*0.8))

        # ДЛЯ ОТЛАДКИ:
#         self.image = pygame.Surface((W, H))
#         self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = (coordX, coordY)

        # НАДПИСЬ НА ИЗОБРАЖЕНИИ
#         draw_text(image, str(self.id_), 18, self.rect.w / 2, self.rect.h / 2)

##===========

    def update(self):
        pass
##        if self.color in (RED, GREEN) and pygame.time.get_ticks() - self.recolor_time > 1000:
##            # self.color = YELLOW ??
##            self.redraw(YELLOW)
##            self.recolor_time = pygame.time.get_ticks()


class Action(pygame.sprite.Sprite):
    def __init__(self, id_, acts, W, H, coordX, coordY, color=RED):
        super(Action, self).__init__()
        self.id_ = id_
        self.img1 = acts[0]
        self.img2 = acts[1]
        self.sound = pygame.mixer.Sound(path.join(snd_dir, acts[2]))

        self.image = draw_img(self.img1, 100, 80)
                
        self.rect = self.image.get_rect()
        self.rect.center = (coordX, coordY)


hit_bin, hit_act = 0, 0
selected_rect = None
 
actions_seq = [] # Последовательность произведенных операций с элементом
no_collisions = True
bin_tryed = None
hits_actions_prev = None

all_sprites = pygame.sprite.Group()
bins_group = pygame.sprite.Group() 
actions_group = pygame.sprite.Group()

new_act(1,  WIDTH * 0.9, HEIGHT * 0.20)
new_act(2,  WIDTH * 0.9, HEIGHT * 0.40)
new_act(3,  WIDTH * 0.9, HEIGHT * 0.60)

new_bin(1, WIDTH * 0.10, HEIGHT * 0.90)
new_bin(2, WIDTH * 0.30, HEIGHT * 0.90)
new_bin(3, WIDTH * 0.50, HEIGHT * 0.90)

player1 = new_player()


settings_screen = True
running = True
while running:

    if settings_screen:
        show_go_screen()  # Entering to settings_screen
        settings_screen = False

        # returning from settings_screen


    # ================ end of returning from settings_screen


    # for single sprites:
    # hit = pygame.sprite.collide_rect(player1, bin1)
    # hit_bin = 1 if hit else 0
    #
    # hit = pygame.sprite.collide_rect(player1, act1)
    # hit_act = 1 if hit else 0


        # BINS collision checking
    hits_bins = pygame.sprite.spritecollide(player1, bins_group, False)
    if no_collisions:  # чтобы фиксировать только переход, а не в течение всего времени нахождения над картинки действия
        for b in bins_group:
            b.image = draw_img(b.img1, b.rect.w, b.rect.h)  # рисуем бак с закрытой крышкой

        for hit in hits_bins:
            bin_tryed = hit.id_
            hit.image = draw_img(hit.img2, hit.rect.w, hit.rect.h)  # рисуем бак с открытой крышкой

            print('=============')
            print(hit.id_, player1.fit_bin)
            print(actions_seq, player1.fit_acts)

            # ДОБАВИТЬ: если действие == отпускание кнопки мыши
            if actions_seq == player1.fit_acts and hit.id_ == player1.fit_bin:
                player1.kill()
                selected_rect = None
                player1 = new_player()
                sound_ok.play()
##                b.color = GREEN
##                b.redraw(b.coordX, b.coordY)
            else:
                sound_bad.play()
##                b.color = RED
##                b.redraw(b.coordX, b.coordY)

            actions_seq.clear()

        # ACTIONS collision checking
    hits_actions = pygame.sprite.spritecollide(player1, actions_group, False)

    # if no_collisions:  # чтобы фиксировать только переход, а не в течение всего времени нахождения над картинки действия
    if hits_actions != hits_actions_prev:
        # for a in actions_group:
        #     a.image = draw_img(a.img1, a.rect.w, a.rect.h)

        hit_prev = hit

        for hit in hits_actions:
#             print(hit)
#             print(hit.sound)
            hit.image = draw_img(hit.img2, hit.rect.w, hit.rect.h)
            hit.sound.play()

            # составление списка последовательности действий             
            if len(actions_seq) == 0:
                actions_seq.append(hit.id_)
            else:
                if hit.id_ != actions_seq[-1]:
                    actions_seq.append(hit.id_)
#                     print(1, actions_seq, actions_seq == player1.fit_acts)

    hits_actions_prev = hits_actions

    no_collisions = True if not hits_bins and not hits_actions else False

        # ================ EVENTS ================
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settings_screen = True

        # Select the player
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.button)
            if player1.rect.collidepoint(event.pos):
                selected_rect = player1  # Select the colliding rect.
                # player1.redraw(color=RED)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_rect = None  # De-select the rect.


            # player1.redraw(color=GREEN)

        # Moving the player
        elif event.type == pygame.MOUSEMOTION:
            if selected_rect is not None:
                if event.buttons[0]:  # Left mouse key
                    player1.rect.centerx += event.rel[0]
                    player1.rect.centery += event.rel[1]

    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # UPDATE
    all_sprites.update()

    # RENDERING
    screen.fill(BLACK)
    #     screen.blit(background, background_rect) # обозначает прорисовку пикселей одного изображения на другом. В этом случае — прорисовку фона на экране.
    all_sprites.draw(screen)
    draw_text(screen, 'hit_bin= ' + str(hit_bin), 18, 60, 20, place='left')
    draw_text(screen, 'hit_act= ' + str(hit_act), 18, 60, 40, place='left')
    # draw_text(screen, 'player1.rect= ' + str(player1.rect), 18, 60, 60, place='left')
    # draw_text(screen, 'bin.rect= ' + str(bin1.rect), 18, 60, 80, place='left')
    draw_text(screen, 'actions_seq= ' + (' '.join(b for b in actions_seq)), 18, 60, 60, place='left')
    draw_text(screen, 'bin= ' + str(bin_tryed), 18, 60, 80, place='left')


    # FLIP
    pygame.display.flip()  # в конце

pygame.quit()
