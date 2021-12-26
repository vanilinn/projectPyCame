import sys

import pygame
import os

FPS = 50
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
STEP = 50
tile_width = tile_height = 50

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def play():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.rect.x -= STEP
                if event.key == pygame.K_d:
                    player.rect.x += STEP
                if event.key == pygame.K_w:
                    player.rect.y -= STEP
                if event.key == pygame.K_s:
                    player.rect.y += STEP

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()


def menu_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        menu.load_window()
        pygame.display.flip()
        clock.tick(FPS)


class Menu:
    def __init__(self):
        self.list_of_difficult = ['easy', 'medium', 'hard']
        self.difficult = self.list_of_difficult[1]
        self.level = 0

        self.music = False
        pygame.mixer.music.load("data/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def load_window(self):
        fon = load_image('fon.jpg')
        fon.get_rect()
        screen.blit(fon, (2, 2))

        image = load_image('frame_for_levels.png')
        t_w = 7
        t_h = 3
        font = pygame.font.Font('data/font.ttf', 60)
        num = 1
        for i in range(t_h):
            for j in range(t_w):
                if not (j == 0 and i == 0):
                    frame = image.get_rect()
                    screen.blit(image, ((width - t_w * frame.width) // 2 + frame.width * j,
                                        (height - t_h * frame.height) // 2 - 30 + frame.height * i))
                    num_rendered = font.render(str(num), True, pygame.Color('#465945'))
                    num_rect = num_rendered.get_rect()
                    num_rect.y = (height - t_h * frame.height) // 2 - 21 + frame.height * i
                    num_rect.x = (width - t_w * frame.width) // 2 + (12 if num >= 10 else 26) + frame.width * j
                    screen.blit(num_rendered, num_rect)
                    num += 1
        image = load_image('frame_for_classic_level.png')
        frame = image.get_rect()
        screen.blit(image, ((width - t_w * frame.width) // 2,
                            (height - t_h * frame.height) // 2 - 30))

        # image = load_image('start_frame.png')
        # screen.blit(image, (522, 444))
        # font = pygame.font.Font('data/font.ttf', 55)
        # start_rendered = font.render('Start', True, pygame.Color('#465945'))
        # start_rect = start_rendered.get_rect()
        # start_rect.y = 459
        # start_rect.x = 538
        # screen.blit(start_rendered, start_rect)

        # screen.blit(load_image('music_on.png') if self.music else load_image('music_off.png'), (5, 2))
        # screen.blit(load_image('title.png'), ((804 - 342) // 2, 10))

    def sound(self):
        self.music = not self.music
        if self.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()


player_image = load_image("player.jpg")
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# start_screen()

player, level_x, level_y = generate_level(load_level("level.txt"))
menu = Menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    menu_window()

    play()
    pygame.display.flip()

    clock.tick(FPS)

terminate()
