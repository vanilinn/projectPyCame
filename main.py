import pygame


class Player:
    def __init__(self, player_hp, player_damage, player_x_pos, player_y_pos):
        self.player_hp = player_hp
        self.player_damage = player_damage
        self.player_x_pos = player_x_pos
        self.player_y_pos = player_y_pos


class RangeMob:
    def __init__(self, range_hp, range_damage, range_x_pos, range_y_pos):
        self.range_hp = range_hp
        self.range_damage = range_damage
        self.range_x_pos = range_x_pos
        self.range_y_pos = range_y_pos


class MeleeMob:
    def __init__(self, melee_hp, melee_damage, melee_x_pos, melee_y_pos):
        self.range_hp = melee_hp
        self.range_damage = melee_damage
        self.range_x_pos = melee_x_pos
        self.range_y_pos = melee_y_pos


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                temp_color = (255, 255, 255)
                pygame.draw.rect(screen, temp_color,
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                                  self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                                  self.cell_size), 1)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    board = Board(5, 7)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()
