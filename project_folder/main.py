# Some of the sounds in this project were created by David McKee (ViRiX) soundcloud.com/virix

# import sys
import random as r
import pygame
from os import path

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

APP_VER = "0.01"
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
                # pygame.quit()
                sys.exit()

            if last_key == 0:
                last_key = now
            if now - last_key > 1000:
                if event.type == pygame.KEYUP:
                    last_key = now
                    waiting = False

def new_player():
    player = Player(r.choice([k for k in pics.keys()]), 30, 40, WIDTH * 0.50, HEIGHT * 0.50, GREEN)
    all_sprites.add(player)
    return player


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


# Загрузка всей игровой графики
img_dir = path.join(path.dirname(__file__), 'img')
# background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
# background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "p1.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (85, 150))
# player_mini_img.set_alpha(50)  # transparency
player_mini_img.set_colorkey(BLACK)


class Player(pygame.sprite.Sprite):
    def __init__(self, id_, W, H, coordX, coordY, color):
        super(Player, self).__init__()
        self.image = pygame.Surface((W, H))
        # self.image = player_mini_img
        self.rect = self.image.get_rect()
        self.id_ = id_
        self.color = color
        self.redraw(self.color)
        self.rect.center = (coordX, coordY)
         # individual (import from diff module)
        self.fit_acts = ['act 3', 'act 2', 'act 1']
        self.fit_bin = 'bin 2'


    def redraw(self, color):
        self.image.fill(color)
        draw_text(self.image, str(self.id_), 18, self.rect.w / 2, self.rect.h / 2)


class GarbageBin(pygame.sprite.Sprite):
    def __init__(self, id_, W, H, coordX, coordY, color):
        super(GarbageBin, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((W, H))
        self.rect = self.image.get_rect()
        # collide_rect_ratio(0.75) ??????????????????????

        self.id_ = id_
        self.color = color
        self.redraw(self.color)
        self.rect.center = (coordX, coordY)
        self.recolor_time = pygame.time.get_ticks()

    def redraw(self, color):
        self.image.fill(color)
        draw_text(self.image, str(self.id_), 18, self.rect.w / 2, self.rect.h / 2)

    def update(self):
        if self.color in (RED, GREEN) and pygame.time.get_ticks() - self.recolor_time > 1000:
            # self.color = YELLOW ??
            self.redraw(YELLOW)
            self.recolor_time = pygame.time.get_ticks()


class Action(pygame.sprite.Sprite):
    def __init__(self, id_, W, H, coordX, coordY, color):
        super(Action, self).__init__()
        self.id_ = id_

        # self.image = pygame.Surface((W, H))

        self.filename = pics[self.id_][0]  # заменить на нормальный вариант, сейчас откусываю последний символ
        # filename = '1.png'  # заменить на нормальный вариант, сейчас откусываю последний символ
        print(0, self.filename, type(self.filename))
        t = path.join(img_dir, self.filename)
        print(t)
        img = pygame.image.load(path.join(img_dir, self.filename)).convert()
        self.coordX = coordX
        self.coordY = coordY
        self.redraw(self.coordX,self.coordY)

        # self.image = pygame.transform.scale(img, (120, 120))
        # self.rect = self.image.get_rect()

        # self.color = color
        # self.redraw(self.color)

    # def redraw(self, color):
    def redraw(self, coordX, coordY):
        img = pygame.image.load(path.join(img_dir, self.filename)).convert()
        self.image = pygame.transform.scale(img, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (coordX, coordY)



        # self.image.fill(color)
        # draw_text(self.image, str(self.id_), 18, self.rect.w / 2, self.rect.h / 2)

ids =[1, 2, 3]

pics = {}
pics['d1'] = ['1.png', '1-1.png']
pics['d2'] = ['2.png', '2.png']
pics['d3'] = ['3.png', '2.png']

N_of_BINS = 10
bins = ['bin ' + str(r.randint(1, 3)) for _ in range(N_of_BINS)]
N_of_ACTS = 10
actions = ['d' + str(r.randint(1, 3)) for _ in range(N_of_ACTS)]

hit_bin, hit_act = 0, 0
selected_rect = None
bins_seq = []
actions_seq = []
no_collisions = True
bin_tryed = None


settings_screen = True
running = True
while running:

    if settings_screen:
        show_go_screen()  # Entering to settings_screen
        settings_screen = False

        all_sprites = pygame.sprite.Group()

        # returning from settings_screen
        bin1 = GarbageBin('bin 2', 60, 80, WIDTH * 0.9, HEIGHT * 0.20, YELLOW)
        bin2 = GarbageBin(r.choice(bins), 60, 80, WIDTH * 0.9, HEIGHT * 0.40, YELLOW)
        bin3 = GarbageBin(r.choice(bins), 60, 80, WIDTH * 0.9, HEIGHT * 0.60, YELLOW)
        bin4 = GarbageBin(r.choice(bins), 60, 80, WIDTH * 0.9, HEIGHT * 0.80, YELLOW)

        bins_group = pygame.sprite.Group()
        bins_group.add(bin1)
        bins_group.add(bin2)
        bins_group.add(bin3)
        bins_group.add(bin4)

        all_sprites.add(bin1)
        all_sprites.add(bin2)
        all_sprites.add(bin3)
        all_sprites.add(bin4)



        act1 = Action('d1', 100, 120, WIDTH * 0.10, HEIGHT * 0.90, WHITE)
        # act2 = Action('d2', 100, 120, WIDTH * 0.30, HEIGHT * 0.90, WHITE)
        # act3 = Action('d3', 100, 120, WIDTH * 0.50, HEIGHT * 0.90, WHITE)
        # act4 = Action(str(r.choice(actions)), 100, 120, WIDTH * 0.70, HEIGHT * 0.90, WHITE)

        actions_group = pygame.sprite.Group()
        actions_group.add(act1)
        # actions_group.add(act2)
        # actions_group.add(act3)
        # actions_group.add(act4)

        all_sprites.add(act1)
        # all_sprites.add(act2)
        # all_sprites.add(act3)
        # all_sprites.add(act4)

        player1 = new_player()

    # ================ end of returning from settings_screen


    # for single sprites:
    # hit = pygame.sprite.collide_rect(player1, bin1)
    # hit_bin = 1 if hit else 0
    #
    # hit = pygame.sprite.collide_rect(player1, act1)
    # hit_act = 1 if hit else 0


        # BINS collision checking
    hits_bins = pygame.sprite.spritecollide(player1, bins_group, False)
    for b in hits_bins:
        bin_tryed = b.id_
        print(2, b.id_, actions_seq)

        if actions_seq == player1.fit_acts and b.id_ == player1.fit_bin:
            player1.kill()
            actions_seq.clear()
            selected_rect = None
            player1 = new_player()
            b.color = GREEN
            b.redraw(b.color)
            sound_ok.play()
        else:
            b.color = RED
            b.redraw(b.color)
            actions_seq.clear()
            sound_bad.play()


        # ACTIONS collision checking   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    hits_actions = pygame.sprite.spritecollide(player1, actions_group, False)


    if no_collisions:
        for hit in actions_group:
            hit.filename = pics[hit.id_][0]
            hit.redraw(hit.coordX, hit.coordY)

        for hit in hits_actions:
            hit.filename = pics[hit.id_][1]
            hit.redraw(hit.coordX, hit.coordY)
            sound_water.play()

            if len(actions_seq) == 0:
                actions_seq.append(hit.id_)
            else:
                if hit.id_ != actions_seq[-1]:
                    actions_seq.append(hit.id_)
                    print(1, actions_seq, actions_seq == player1.fit_acts)


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
