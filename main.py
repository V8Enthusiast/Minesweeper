import random
from random import choice, randint, uniform
from particles import Particle
import pygame
from pygame import mixer
import time
import configparser

def read_theme_from_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    theme = {}
    for key, value in config.items('Colors'):
        theme[key] = tuple(map(int, value.split(',')))

    return theme

def read_settings_from_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    settings = {}
    for key, value in config.items('Settings'):
        settings[key] = int(value)
    return settings

theme_file = "theme.ini"
settings_file = "settings.ini"
theme_colors = read_theme_from_ini(theme_file)
settings = read_settings_from_ini(settings_file)

ROWS = settings['rows']
COLUMNS = settings['columns']
BOMBS = settings['bombs']
TILE_SIZE = settings['tile_size']
BORDER = settings['border']

main_tile_color = theme_colors['main_tile_color']
covered_tile_color = theme_colors['covered_tile_color']
empty_tile_color = theme_colors['empty_tile_color']
bomb_tile_color = theme_colors['bomb_tile_color']
flagged_tile_color = theme_colors['flagged_tile_color']
BORDER_COLOR = theme_colors['border_color']

board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
bombs_left = BOMBS

for r in range(ROWS):
    for c in range(COLUMNS):
        random1 = random.randint(0, 1)
        randomxcoord = random.randint(0, COLUMNS-1)
        randomycoord = random.randint(0, ROWS-1)

        if random1 == 1 and board[randomycoord][randomxcoord] == 0 and bombs_left > 0:
            board[randomycoord][randomxcoord] = -1
            bombs_left -= 1

def explode(Mouse_x, Mouse_y):
    mixer.music.play()
    for _ in range(2024):
        color = choice(((227, 23, 10), (225, 96, 54), (234, 196, 53), (42, 45, 52)))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(60, 400)
        Particle(particle_group, (Mouse_x, Mouse_y), color, direction, speed)
    for _ in range(2024):
        color = choice(((227, 23, 10), (225, 96, 54), (234, 196, 53), (42, 45, 52)))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(400, 700)
        Particle(particle_group, (Mouse_x, Mouse_y), color, direction, speed)

class Tile:
    def __init__(self,x ,y, value):
        self.x = x
        self.y = y
        self.value = value
        self.revealed = False
        self.flagged = False

    def calculate_value(self, board):
        neighbouring_mines = 0
        x = self.x
        y = self.y

        if x - 1 >= 0 and board[x - 1][y] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and board[x + 1][y] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and y + 1 < COLUMNS and board[x + 1][y + 1] == -1:
            neighbouring_mines += 1
        if x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] == -1:
            neighbouring_mines += 1
        if x + 1 < ROWS and y - 1 >= 0 and board[x + 1][y - 1] == -1:
            neighbouring_mines += 1
        if x - 1 >= 0 and y + 1 < COLUMNS and board[x - 1][y + 1] == -1:
            neighbouring_mines += 1
        if y + 1 < COLUMNS and board[x][y + 1] == -1:
            neighbouring_mines += 1
        if y - 1 >= 0 and board[x][y - 1] == -1:
            neighbouring_mines += 1

        self.value = neighbouring_mines
        return neighbouring_mines

gameboard = board

x = 0
y = 0
for r in board:

    for c in r:
        if c != -1:
            tile = Tile(x, y, 0)
            gameboard[x][y] = tile.calculate_value(board)
        y += 1
    x += 1
    y = 0

WIDTH = (COLUMNS) * TILE_SIZE
HEIGHT = (ROWS) * TILE_SIZE
MAIN_HEIGHT = HEIGHT + 100

pygame.font.init()
mixer.init()
mixer.music.load('sounds/explosion.mp3')
mixer.music.set_volume(0.6)

font = pygame.font.Font('font.ttf', TILE_SIZE//2)
pygame.display.set_caption("Minesweeper")

screen = pygame.display.set_mode((WIDTH, MAIN_HEIGHT))

clock = pygame.time.Clock()

particle_group = pygame.sprite.Group()

small_tile_size = int(.75*TILE_SIZE)

bomb_img = pygame.image.load("img/bomb.png").convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (TILE_SIZE, TILE_SIZE))

flag_img = pygame.image.load("img/flag.png").convert_alpha()
flag_img = pygame.transform.scale(flag_img, (small_tile_size, small_tile_size))

img = pygame.image.load("img/gameover.jpg").convert()

pygame.display.set_icon(bomb_img)

running = True

hidden_board = [[-2 for _ in range(COLUMNS)] for i in range(ROWS)]
temp = gameboard
gameboard = hidden_board
hidden_board = temp

checked_tiles = []
def draw_empty_tiles(point):
    x = point[0]
    y = point[1]
    tiles_to_check = []
    if x - 1 >= 0:
        if board[x - 1][y] == 0:
            gameboard[x - 1][y] = 0
            tiles_to_check.append((x - 1, y))
        if board[x - 1][y] > 0:
            gameboard[x - 1][y] = board[x - 1][y]
    if x + 1 < ROWS:
        if board[x + 1][y] == 0:
            gameboard[x + 1][y] = 0
            tiles_to_check.append((x + 1, y))
        if board[x + 1][y] > 0:
            gameboard[x + 1][y] = board[x + 1][y]
    if x + 1 < ROWS and y + 1 < COLUMNS:
        if board[x + 1][y + 1] == 0:
            gameboard[x + 1][y + 1] = 0
            tiles_to_check.append((x + 1, y + 1))
        if board[x + 1][y + 1] > 0:
            gameboard[x + 1][y + 1] = board[x + 1][y + 1]
    if x - 1 >= 0 and y - 1 >= 0:
        if board[x - 1][y - 1] == 0:
            gameboard[x - 1][y - 1] = 0
            tiles_to_check.append((x - 1, y - 1))
        if board[x - 1][y - 1] > 0:
            gameboard[x - 1][y - 1] = board[x - 1][y - 1]
    if x + 1 < ROWS and y - 1 >= 0:
        if board[x + 1][y - 1] == 0:
            gameboard[x + 1][y - 1] = 0
            tiles_to_check.append((x + 1, y - 1))
        if board[x + 1][y - 1] > 0:
            gameboard[x + 1][y - 1] = board[x + 1][y - 1]
    if x - 1 >= 0 and y + 1 < COLUMNS:
        if board[x - 1][y + 1] == 0:
            gameboard[x - 1][y + 1] = 0
            tiles_to_check.append((x - 1, y + 1))
        if board[x - 1][y + 1] > 0:
            gameboard[x - 1][y + 1] = board[x - 1][y + 1]
    if y + 1 < COLUMNS:
        if board[x][y + 1] == 0:
            gameboard[x][y + 1] = 0
            tiles_to_check.append((x, y + 1))
        if board[x][y + 1] > 0:
            gameboard[x][y + 1] = board[x][y + 1]
    if y - 1 >= 0:
        if board[x][y - 1] == 0:
            gameboard[x][y - 1] = 0
            tiles_to_check.append((x, y - 1))
        if board[x][y - 1] > 0:
            gameboard[x][y - 1] = board[x][y - 1]
    checked_tiles.append(point)
    return tiles_to_check

failed = False
render_fail_text = False
solved = False
bombs_left_to_find = BOMBS
placed_flags = 0
main_text_message = "Minesweeper"
start_time = time.time()
update_timer = True
display_time = "00 : 00"
animation = False
animation_start_time = None

while running:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if failed or solved:
                board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
                bombs_left = BOMBS

                for r in range(ROWS):
                    for c in range(COLUMNS):
                        random1 = random.randint(0, 1)
                        randomxcoord = random.randint(0, COLUMNS - 1)
                        randomycoord = random.randint(0, ROWS - 1)

                        if random1 == 1 and board[randomycoord][randomxcoord] == 0 and bombs_left > 0:
                            board[randomycoord][randomxcoord] = -1
                            bombs_left -= 1
                gameboard = board
                x = 0
                y = 0
                for r in board:

                    for c in r:
                        if c != -1:
                            tile = Tile(x, y, 0)
                            gameboard[x][y] = tile.calculate_value(board)
                        y += 1
                    x += 1
                    y = 0

                WIDTH = (COLUMNS) * TILE_SIZE
                HEIGHT = (ROWS) * TILE_SIZE

                hidden_board = [[-2 for _ in range(COLUMNS)] for i in range(ROWS)]
                temp = gameboard
                gameboard = hidden_board
                hidden_board = temp

                checked_tiles = []
                main_text_message = "Minesweeper"
                failed = False
                solved = False
                bombs_left_to_find = BOMBS
                placed_flags = 0
                update_timer = True
                render_fail_text = False
                display_time = "00 : 00"
                start_time = time.time()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if failed:
                    if render_fail_text:
                        render_fail_text = False
                        main_text_message = "Press any key to restart"
                    else:
                        Mouse_x, Mouse_y = pygame.mouse.get_pos()
                        clicked_row = int(Mouse_y) // TILE_SIZE
                        clicked_column = int(Mouse_x) // TILE_SIZE
                        if clicked_column >= COLUMNS or clicked_row >= ROWS:
                            break
                        if gameboard[clicked_column][clicked_row] == -3:
                            break
                        if hidden_board[clicked_column][clicked_row] == -1:
                            gameboard[clicked_column][clicked_row] = hidden_board[clicked_column][clicked_row]
                            explode(Mouse_x, Mouse_y)
                else:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    clicked_row = int(Mouse_y) // TILE_SIZE
                    clicked_column = int(Mouse_x) // TILE_SIZE
                    if clicked_column >= COLUMNS or clicked_row >= ROWS:
                        break
                    if gameboard[clicked_column][clicked_row] == -3:
                        break
                    gameboard[clicked_column][clicked_row] = hidden_board[clicked_column][clicked_row]
                    if gameboard[clicked_column][clicked_row] == -1:
                        #running = False
                        failed = True
                        main_text_message = "Your computer has exploded!"
                        update_timer = False
                        explode(Mouse_x, Mouse_y)
                        animation = True
                        animation_start_time = time.time()

                    if gameboard[clicked_column][clicked_row] == 0:
                        empty_list = draw_empty_tiles((clicked_column, clicked_row))
                        while empty_list != []:
                            new_empty_list = []
                            for coord in empty_list:
                                if coord not in checked_tiles:
                                    temp_list = draw_empty_tiles(coord)
                                    for coordinate in temp_list:
                                        new_empty_list.append(coordinate)
                            empty_list = new_empty_list

            if event.button == 3:
                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                clicked_row = int(Mouse_y) // TILE_SIZE
                clicked_column = int(Mouse_x) // TILE_SIZE
                if clicked_column >= COLUMNS or clicked_row >= ROWS:
                    break
                if not failed:
                    if gameboard[clicked_column][clicked_row] == -3:
                        gameboard[clicked_column][clicked_row] = -2
                        placed_flags -= 1
                    elif gameboard[clicked_column][clicked_row] == -2 and placed_flags < BOMBS:
                        gameboard[clicked_column][clicked_row] = -3
                        placed_flags += 1
    if placed_flags == BOMBS:
        correct = 0
        for r in range(ROWS):
            for c in range(COLUMNS):
                if gameboard[r][c] == -2:
                    break
                if board[r][c] == -1 and gameboard[r][c] == -3:
                   correct += 1
        if correct == BOMBS:
            solved = True
            main_text_message = "Congrats! You beat the game!"
            update_timer = False

    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(r * TILE_SIZE, c * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if gameboard[r][c] == -3:
                tile_rect = pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER)
                flag_rect = pygame.Rect(r * TILE_SIZE + BORDER + (TILE_SIZE - small_tile_size)/2, c * TILE_SIZE + BORDER + (TILE_SIZE - small_tile_size)/2, TILE_SIZE - BORDER,TILE_SIZE - BORDER)
                pygame.draw.rect(screen, flagged_tile_color, tile_rect)
                # text = font.render('!', True, (0, 0, 0), None)
                # textRect = text.get_rect()
                # textRect.center = (
                #     r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2,
                #     c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(flag_img, flag_rect)
            if gameboard[r][c] == -2:
                pygame.draw.rect(screen, covered_tile_color, pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
            if gameboard[r][c] == -1:
                tile_rect = pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER)
                pygame.draw.rect(screen, bomb_tile_color, tile_rect)
                screen.blit(bomb_img, tile_rect)
            if gameboard[r][c] == 0:
                pygame.draw.rect(screen, empty_tile_color,pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
            if gameboard[r][c] == 1:
                pygame.draw.rect(screen, main_tile_color,pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
                text = font.render('1', True, (35, 69, 168), None)
                textRect = text.get_rect()
                textRect.center = (r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
            if gameboard[r][c] == 2:
                pygame.draw.rect(screen, main_tile_color, pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
                text = font.render('2', True, (35, 107, 22), None)
                textRect = text.get_rect()
                textRect.center = (
                r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
            if gameboard[r][c] == 3:
                pygame.draw.rect(screen, main_tile_color, pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
                text = font.render('3', True, (107, 22, 22), None)
                textRect = text.get_rect()
                textRect.center = (
                r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
            if gameboard[r][c] == 4:
                pygame.draw.rect(screen, main_tile_color, pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER,TILE_SIZE - BORDER))
                text = font.render('4', True, (7, 7, 48), None)
                textRect = text.get_rect()
                textRect.center = (
                r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
            if gameboard[r][c] == 5:
                pygame.draw.rect(screen, main_tile_color,
                pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER, TILE_SIZE - BORDER))
                text = font.render('5', True, (105, 50, 19), None)
                textRect = text.get_rect()
                textRect.center = (
                    r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
            if gameboard[r][c] > 5:
                pygame.draw.rect(screen, main_tile_color,
                pygame.Rect(r * TILE_SIZE + BORDER, c * TILE_SIZE + BORDER, TILE_SIZE - BORDER, TILE_SIZE - BORDER))
                text = font.render(str(gameboard[r][c]), True, (40, 173, 142), None)
                textRect = text.get_rect()
                textRect.center = (
                    r * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2, c * TILE_SIZE + BORDER + (TILE_SIZE - BORDER) // 2)
                screen.blit(text, textRect)
    #pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(ROWS * TILE_SIZE, COLUMNS * TILE_SIZE, BORDER, WIDTH))

    if update_timer:
        current_time = time.time()
        timer_time = current_time - start_time
        minutes = int(timer_time // 60)
        seconds = int(timer_time % 60)
        display_time = f'{minutes:02d} : {seconds:02d}'

    main_text = font.render(main_text_message, True, main_tile_color, None)
    main_textRect = main_text.get_rect()
    main_textRect.center = (
        WIDTH // 2,
        MAIN_HEIGHT -50)
    screen.blit(main_text, main_textRect)

    timer_text = font.render(display_time, True, main_tile_color, None)
    timer_textRect = timer_text.get_rect()
    timer_textRect.center = (
        WIDTH // 2 - 200,
        MAIN_HEIGHT - 50)
    screen.blit(timer_text, timer_textRect)

    flag_text = font.render(f'Flags: {placed_flags}/{BOMBS}', True, main_tile_color, None)
    flag_textRect = flag_text.get_rect()
    flag_textRect.center = (
        WIDTH // 2 + 200,
        MAIN_HEIGHT - 50)
    screen.blit(flag_text, flag_textRect)

    delta_time = clock.tick() / 1000

    particle_group.draw(screen)

    particle_group.update(delta_time)

    if animation:
        now = time.time()
        if now - animation_start_time > 2 and failed:
            render_fail_text = True
            animation = False
            animation_start_time = None

    if failed and render_fail_text:
        screen.blit(img, (WIDTH//2 - 320, HEIGHT//2 - 180))

    pygame.display.update()