import random
import sys
import time

import pygame
import os

FPS = 50
clock = pygame.time.Clock()
STEP = 50
tile_width = tile_height = 50

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
dragon_sprite = pygame.sprite.Group()

ENEMY_DMG = [1, 2, 5]
MOB_IMAGES = ['mob1.png',
              'mob2.png',
              'boss.png']
MOBDAMAGEEVENT = pygame.USEREVENT + 1


def load_level(filename):  # загрузка уровня
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name):  # загрузка изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():  # выход из приложения
    pygame.quit()
    sys.exit()


def start_screen():  # стартовый экран
    intro_text = "Project PyGame"
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font.ttf', 100)
    image = font.render(intro_text, True, pygame.Color('#463445'))
    rect = image.get_rect()
    screen.blit(image, ((WIDTH - rect.width) // 2, (HEIGHT - rect.height) // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(game_over=True):  # экран окончания
    if game_over:
        intro_text = "GAME OVER"
    else:
        intro_text = "YOU'RE WIN"
    fon = pygame.transform.scale(load_image('end.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font.ttf', 100)
    image = font.render(intro_text, True, pygame.Color('#463445'))
    rect = image.get_rect()
    screen.blit(image, ((WIDTH - rect.width) // 2, (HEIGHT - rect.height) // 2))
    if not game_over:
        score_time = time.time() - start_time
        intro_text = 'Time {}:{}'.format(int(score_time) // 60, int(score_time) % 60)
        font = pygame.font.Font('data/font.ttf', 60)
        image = font.render(intro_text, True, pygame.Color('#463445'))
        rect = image.get_rect()
        screen.blit(image, ((WIDTH - rect.width) // 2, (HEIGHT - rect.height) // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        dragon_sprite.draw(screen)
        dragon_sprite.update()
        pygame.display.flip()
        clock.tick(FPS)


class Item(pygame.sprite.Sprite):  # класс предмета
    def __init__(self, x, y, dmg):
        super().__init__(item_group, all_sprites)
        self.image = pygame.transform.scale(load_image("weapon.png"),
                                            (tile_width, tile_height))
        self.rect = self.image.get_rect().move(x, y)
        self.damage = dmg

    def update(self):
        self.rect.x = 0
        self.rect.y = 550
        player.damage += self.damage


class Enemy(pygame.sprite.Sprite):  # класс монстров для генерации уровня
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type],
                                            (tile_width, tile_height))
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Mob(pygame.sprite.Sprite):  # класс монстра для игры
    def __init__(self, mob_type, pos_x, pos_y, dmg, hp):
        super().__init__(mobs_group, all_sprites)
        self.image = pygame.transform.scale(load_image(MOB_IMAGES[mob_type]), (50, 50))
        self.rect = self.image.get_rect().move(tile_width
                                               * pos_x, tile_height * pos_y)
        self.hp = hp
        self.hp_max = hp
        self.damage = dmg * ENEMY_DMG[0]

    def update(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            return True


class AnimatedSprite(pygame.sprite.Sprite):  # класс для анимации
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(dragon_sprite, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self, pos_x, pos_y, dmg, hp):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width
                                               * pos_x, tile_height * pos_y)
        self.hp = hp
        self.hp_max = hp
        self.damage = dmg

    def change_hp(self, dmg=0, hp=0):
        self.hp -= dmg
        self.hp += hp
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def change_dmg(self, dmg_of_item):
        self.damage += dmg_of_item


class Border(pygame.sprite.Sprite):  # класс поля
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def generate_level(level, final=False):  # генератор уровня
    new_player, x, y = None, None, None
    mob_list = []
    if not final:
        number_of_mobs = random.randrange(2, 5)
        while len(mob_list) < number_of_mobs:
            mob_y, mob_x = random.randrange(1, len(level) - 1), \
                           random.randrange(1, len(level[0]) - 1)
            if level[mob_y][mob_x] in ['.'] and level[mob_y - 1][mob_x] in \
                    ['.', '#'] and level[mob_y + 1][mob_x] in \
                    ['.', '#'] and level[mob_y][mob_x - 1] in ['.', '#'] \
                    and level[mob_y][mob_x + 1] in ['.', '#']:
                mob_list.append(Mob(random.randrange(2), mob_x, mob_y, 10, 100))
    else:
        Mob(2, random.randrange(7, 15), random.randrange(11), 20, 200)

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Enemy('empty', x, y)
            elif level[y][x] == '#':
                Enemy('wall', x, y)
            elif level[y][x] == '@':
                Enemy('empty', x, y)
                new_player = [x, y]
    return new_player


def hp_draw(type_of_enemy, hp_now, hp_max, above=0):  # класс отображения здоровья
    step = 0 if type_of_enemy == 'player' else 450
    pygame.draw.rect(screen, (255, 255, 255),
                     (step + 50, 565 - above * tile_height, 250, 20))
    if type_of_enemy == 'player':
        pygame.draw.rect(screen, (0, 255, 0),
                         (50, 565 - above * tile_height,
                          int(250 * hp_now / hp_max), 20))
    else:
        pygame.draw.rect(screen, (0, 255, 0),
                         (step + 50 + 250 - int(250 * hp_now / hp_max),
                          565 - above * tile_height,
                          int(250 * hp_now / hp_max), 20))
    pygame.draw.rect(screen, (0, 0, 0), (step + 50, 565 - above * tile_height, 250, 20), 2)


def get_item(x, y):  # функция для получения предмета
    global weapon
    if weapon:
        return
    if random.randrange(10) == 1:
        Item(x, y, 20)
        weapon = True


def play():  # игровая функция
    global weapon
    list_of_mobs = []
    if menu.clas == 'fire':
        player.damage += 10
    for i in range(5):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == MOBDAMAGEEVENT:
                    if mobs_group.sprites():
                        player.change_hp(dmg=mobs_group.sprites()[0].__getattribute__('damage') *
                                             len(list_of_mobs))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for mob in list_of_mobs:
                        if event.pos[0] in range(mob.rect.x,
                                                 mob.rect.x + mob.rect.width + 1) and \
                                event.pos[1] in range(mob.rect.y,
                                                      mob.rect.y + mob.rect.height + 1):
                            mob.update(player.damage)
                    if weapon:
                        if event.pos[0] in \
                                range(item_group.sprites()[0].rect.x,
                                      item_group.sprites()[0].rect.x
                                      + item_group.sprites()[0].rect.w + 1) \
                                and event.pos[1] in range(item_group.sprites()[0].rect.y,
                                                          item_group.sprites()[0].rect.y +
                                                          item_group.sprites()[0].rect.h + 1):
                            item_group.sprites()[0].update()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.rect.x -= STEP
                        if pygame.sprite.spritecollideany(player, vertical_borders) \
                                or pygame.sprite.spritecollideany(
                            player, mobs_group):
                            player.rect.x += STEP
                    if event.key == pygame.K_d:
                        player.rect.x += STEP
                        if pygame.sprite.spritecollideany(player, vertical_borders) \
                                or pygame.sprite.spritecollideany(
                            player, mobs_group):
                            player.rect.x -= STEP
                    if event.key == pygame.K_w:
                        player.rect.y -= STEP
                        if pygame.sprite.spritecollideany(player, horizontal_borders) \
                                or pygame.sprite.spritecollideany(
                            player, mobs_group):
                            player.rect.y += STEP
                    if event.key == pygame.K_s:
                        player.rect.y += STEP
                        if pygame.sprite.spritecollideany(player, horizontal_borders) \
                                or pygame.sprite.spritecollideany(
                            player, mobs_group):
                            player.rect.y -= STEP

            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            mobs_group.draw(screen)
            item_group.draw(screen)
            hp_draw('player', player.hp, player.hp_max)
            for mob in list_of_mobs:
                if mob.update(0):
                    pos = [mob.rect.x, mob.rect.y]
                    mob.kill()
                    get_item(pos[0], pos[1])
            list_of_mobs = []
            for mob in mobs_group:
                if player.rect.x + player.rect.width == mob.rect.x \
                        and player.rect.y == mob.rect.y \
                        or player.rect.x == mob.rect.x + mob.rect.width \
                        and player.rect.y == mob.rect.y \
                        or player.rect.y + player.rect.height == mob.rect.y \
                        and player.rect.x == mob.rect.x \
                        or player.rect.y == mob.rect.y + mob.rect.height \
                        and player.rect.x == mob.rect.x:
                    hp_draw('mob', mob.__getattribute__('hp'),
                            mob.__getattribute__('hp_max'), above=len(list_of_mobs))
                    list_of_mobs.append(mob)

            if player.hp == 0:
                end_screen(True)
                return
            if not mobs_group.sprites():
                screen.blit(pygame.transform.scale(load_image('portal.png'), (60, 60)),
                            (5 * tile_width - 5, 1 * tile_height - 5))
                if player.rect.x == 5 * tile_width and player.rect.y == 1 * tile_height:
                    player_group.draw(screen)
                    pygame.display.flip()
                    time.sleep(1)
                    break
            pygame.display.flip()
            clock.tick(FPS)
        if i + 1 == 4:
            pos = generate_level(load_level("level.txt"), final=True)
        else:
            pos = generate_level(load_level("level.txt"))
        player.rect.x, player.rect.y = pos[0] * tile_width, pos[1] * tile_height
    end_screen(False)


def menu_window():  # функция меню
    global running
    name = ''
    input = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(420, 781) and \
                        event.pos[1] in range(20, 61):
                    input = True
                else:
                    if input:
                        input = False
                    if event.pos[0] in range(220, 360) and \
                            event.pos[1] in range(20, 85):
                        menu.difficult = menu.list_of_difficult[0]
                    elif event.pos[0] in range(20, 160) and \
                            event.pos[1] in range(120, 185):
                        menu.difficult = menu.list_of_difficult[1]
                    elif event.pos[0] in range(220, 360) and \
                            event.pos[1] in range(120, 185):
                        menu.difficult = menu.list_of_difficult[2]
                    elif event.pos[0] in range(20, 160) and \
                            event.pos[1] in range(435, 500):
                        menu.clas = menu.list_of_classes[0]
                    elif event.pos[0] in range(220, 360) and \
                            event.pos[1] in range(435, 500):
                        menu.clas = menu.list_of_classes[1]
                    elif event.pos[0] in range(500, 700) and \
                            event.pos[1] in range(435, 500):
                        return
            elif event.type == pygame.KEYDOWN:
                if input:
                    if event.unicode == '\x08':
                        if len(name) > 1:
                            name = name[:len(name) - 1]
                        else:
                            name = ''
                    elif event.unicode == '\r':
                        input = False
                    else:
                        name = (name + event.unicode) if len(name) < 13 else name
                else:
                    return
        menu.load_window()

        font = pygame.font.Font('data/font.ttf', 30)
        image = font.render(name, True, pygame.Color('#463445'))
        rect = image.get_rect()
        screen.blit(image, (426, 25))

        if input:
            pygame.draw.rect(screen, (0, 0, 0), (428 + rect.w, 23, 2, 32), 1)

        pygame.display.flip()
        clock.tick(FPS)


class Menu:  # класс меню
    def __init__(self):
        self.list_of_difficult = ['easy', 'normal', 'hard']
        self.list_of_classes = ['fire', 'freeze']
        self.difficult = self.list_of_difficult[1]
        self.clas = self.list_of_classes[1]
        self.level = 0

    def load_window(self):
        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        fon.get_rect()
        screen.blit(fon, (0, 0))

        for i in range(2):
            for j in range(2):
                if i == 0 and j == 0:
                    font = pygame.font.Font('data/font.ttf', 50)
                    image = font.render('Difficult', True, pygame.Color('black'))
                    screen.blit(image, (j * 200 + 20, i * 150 + 35))
                else:
                    col = pygame.Color('#ADC341') if \
                        self.list_of_difficult[i * 2 + j - 1] == self.difficult \
                        else pygame.Color('#D3E18E')
                    pygame.draw.rect(screen, col, (j * 200 + 20, i * 100 + 20, 140, 65))
                    font = pygame.font.Font('data/font.ttf', 35)
                    image = font.render(self.list_of_difficult[i * 2 + j - 1],
                                        True, pygame.Color('black'))
                    screen.blit(image, (j * 220 + 30, i * 102 + 34))
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (j * 200 + 20, i * 100 + 20, 140, 65), 4)

        font = pygame.font.Font('data/font.ttf', 50)
        image = font.render('Class', True, pygame.Color('black'))
        screen.blit(image, (120, 350))
        for i in range(2):
            col = pygame.Color('#ADC341') if self.list_of_classes[i] == \
                                             self.clas else pygame.Color('#D3E18E')
            pygame.draw.rect(screen, col, (i * 200 + 20, 435, 140, 65))
            font = pygame.font.Font('data/font.ttf', 35)
            image = font.render(self.list_of_classes[i], True, pygame.Color('black'))
            screen.blit(image, (i * 178 + 58, 449))
            pygame.draw.rect(screen, (0, 0, 0), (i * 200 + 20, 435, 140, 65), 4)

        pygame.draw.rect(screen, (255, 255, 255), (420, 20, 360, 38))
        pygame.draw.rect(screen, (0, 0, 0), (420, 20, 360, 38), 1)

        pygame.draw.rect(screen, pygame.Color('#D3E18E'), (500, 435, 200, 65))
        font = pygame.font.Font('data/font.ttf', 50)
        image = font.render('Start', True, pygame.Color('black'))
        screen.blit(image, (420 + 123, 445))
        pygame.draw.rect(screen, pygame.Color('black'), (500, 435, 200, 65), 4)


player_image = pygame.transform.scale(load_image("player.png"), (tile_width, tile_height))
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png')
}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

Border(0, 49, WIDTH, 49)
Border(0, HEIGHT - 49, WIDTH, HEIGHT - 49)
Border(49, 0, 49, HEIGHT)
Border(WIDTH - 49, 0, WIDTH - 49, HEIGHT)

menu = Menu()

start_screen()

dragon = AnimatedSprite(load_image("dragon.png"), 8, 2, 350, 440)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    menu_window()
    if not running:
        break
    pos = generate_level(load_level("level.txt"))
    player = Player(pos[0], pos[1], 20, 100)
    pygame.time.set_timer(MOBDAMAGEEVENT, 2000 if menu.clas == 'freeze' else 1000)
    weapon = False
    start_time = time.time()
    play()
    player.kill()
    [mob.kill() for mob in mobs_group]
    item_group.remove()
    pygame.display.flip()

    clock.tick(FPS)

terminate()
