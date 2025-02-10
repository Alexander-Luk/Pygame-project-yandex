import pygame
import os
import sys
import random
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image


class SpiritSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, t_s, width, height, lines, name):
        super().__init__(all_sprites)
        self.name = name
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = [x, y]
        self.start_pos = [x, y]
        self.cur_direction = "left"
        self.exp_direction = "up"
        self.move = True
        self.mask = pygame.mask.from_surface(self.image)
        self.t_s = t_s
        self.width = width
        self.height = height
        self.way_searching = False
        self.lines = lines
        self.speed = 6
        self.injured = False
        self.injured_image = 'sprites sheets/injured start sheet.png'

    def cut_sheet(self, sheet, columns, rows, x, y):
        self.frames = []
        self.rect = pygame.Rect(x, y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def on_the_border(self):
        if self.pos[0] >= self.width - self.t_s:
            return True
        elif self.pos[0] <= 0:
            return True

    def try_cell(self, direction):
        global cells_drawing
        if direction == 'right':
            if ' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])]) in cells_drawing:
                if cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] in tales_to_go:
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'left':
            if ' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])]) in cells_drawing:
                if cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] in tales_to_go:
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'up':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] - self.t_s)])] == 'gate':
                return True
            elif cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] - self.t_s)])] in tales_to_go:
                return True
            else:
                return False
        elif direction == 'down':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] + self.t_s)])] in tales_to_go:
                return True
            else:
                return False

    def make_move(self, direction):
        if ' '.join([str(self.pos[0]), str(self.pos[1])]) in cells_drawing:
            if self.injured:
                self.speed = 3
            elif cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1])])] == 'tunel':
                self.speed = 3
            else:
                self.speed = 6
        global spirit_sheets
        if direction == 'right':
            self.pos[0] += self.speed
        elif direction == 'left':
            self.pos[0] -= self.speed
        elif direction == 'up':
            self.pos[1] -= self.speed
        elif direction == 'down':
            self.pos[1] += self.speed
        self.cut_sheet(spirit_sheets[self.name][direction], 4, 1, self.pos[0], self.pos[1])

    def try_cur_move(self):
        if self.try_cell(self.cur_direction):
            return True
        else:
            return False

    def try_exp_move(self):
        if self.try_cell(self.exp_direction):
            self.cur_direction = self.exp_direction
            return True
        else:
            return False

    def find_the_way(self, direction):
        pass

    def update(self):
        global spirit_sheets
        if self.injured:
            if self.injured_image == 'sprites sheets/injured end sheet.png':
                self.cut_sheet(load_image(self.injured_image), 8, 1, self.pos[0],
                               self.pos[1])
            else:
                self.cut_sheet(load_image(self.injured_image), 4, 1, self.pos[0],
                               self.pos[1])
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.pos[0] == 0 - self.t_s:
            self.pos[0] = self.width
        elif self.pos[0] == self.width:
            self.pos[0] = 0 - self.t_s


class PacmanSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, t_s, width, height, lines):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = [x, y]
        self.start_pos = [x, y]
        self.cur_direction = "left"
        self.exp_direction = "left"
        self.move = True
        self.mask = pygame.mask.from_surface(self.image)
        self.t_s = t_s
        self.width = width
        self.height = height
        self.way_searching = False
        self.eaten = False
        self.lines = lines

    def cut_sheet(self, sheet, columns, rows, x, y):
        self.frames = []
        self.rect = pygame.Rect(x, y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def on_the_border(self):
        if self.pos[0] >= self.width - self.t_s:
            return True
        elif self.pos[0] <= 0:
            return True

    def try_cell(self, direction):
        global cells_drawing
        global tales_to_go
        if direction == 'right':
            if ' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])]) in cells_drawing:
                if cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] in tales_to_go:
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'left':
            if ' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])]) in cells_drawing:
                if cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] in tales_to_go:
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'up':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] - self.t_s)])] in tales_to_go:
                return True
            else:
                return False
        elif direction == 'down':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] + self.t_s)])] in tales_to_go:
                return True
            else:
                return False

    def make_move(self, direction):
        global pacman_sheets
        if direction == 'right':
            self.pos[0] += 6
        elif direction == 'left':
            self.pos[0] -= 6
        elif direction == 'up':
            self.pos[1] -= 6
        elif direction == 'down':
            self.pos[1] += 6
        self.cut_sheet(pacman_sheets[direction], 4, 1, self.pos[0], self.pos[1])

    def try_cur_move(self):
        if self.try_cell(self.cur_direction):
            return True
        else:
            return False

    def try_exp_move(self):
        if self.try_cell(self.exp_direction):
            self.cur_direction = self.exp_direction
            return True
        else:
            return False

    def update(self):
        global pacman_sheets
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.pos[0] == 0 - self.t_s:
            self.pos[0] = self.width
        elif self.pos[0] == self.width:
            self.pos[0] = 0 - self.t_s


cells_drawing = {}
cells = []
all_directions = ['right', 'left', 'up', 'down']
opposite_directions = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}
tales_to_go = ['empty', 'tunel', 'power']

spirit_sheets = {'red': {"up": load_image("sprites sheets/red spirit/red sheet top.png"),
                         "down": load_image("sprites sheets/red spirit/red sheet bottom.png"),
                         "right": load_image("sprites sheets/red spirit/red sheet right.png"),
                         "left": load_image("sprites sheets/red spirit/red sheet left.png")},
                 'orange': {"up": load_image("sprites sheets/orange spirit/orange sheet top.png"),
                            "down": load_image("sprites sheets/orange spirit/orange sheet bottom.png"),
                            "right": load_image("sprites sheets/orange spirit/orange sheet right.png"),
                            "left": load_image("sprites sheets/orange spirit/orange sheet left.png")},
                 'blue': {"up": load_image("sprites sheets/blue spirit/blue sheet top.png"),
                          "down": load_image("sprites sheets/blue spirit/blue sheet bottom.png"),
                          "right": load_image("sprites sheets/blue spirit/blue sheet right.png"),
                          "left": load_image("sprites sheets/blue spirit/blue sheet left.png")},
                 'pink': {"up": load_image("sprites sheets/pink spirit/pink sheet top.png"),
                          "down": load_image("sprites sheets/pink spirit/pink sheet bottom.png"),
                          "right": load_image("sprites sheets/pink spirit/pink sheet right.png"),
                          "left": load_image("sprites sheets/pink spirit/pink sheet left.png")}}

pacman_sheets = {"up": load_image("sprites sheets/pacman/pacman sheet top.png"),
                 "down": load_image("sprites sheets/pacman/pacman sheet bottom.png"),
                 "right": load_image("sprites sheets/pacman/pacman sheet right.png"),
                 "left": load_image("sprites sheets/pacman/pacman sheet left.png")}


def main():
    file = open("data/map.txt")
    lines = file.readlines()
    file.close()

    x_size = len(lines[0][:-1])
    y_size = len(lines)
    tile_size = 42
    pygame.init()
    size = width, height = tile_size * x_size, tile_size * y_size
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 36
    countdown = 0
    power_countdown = 0
    power_eaten = False
    death_frame = 0
    lives = 3

    for x in range(x_size):
        for y in range(y_size):
            if lines[y][x] == ".":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
            elif lines[y][x] == "#":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'wall'
            elif lines[y][x] == "_":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'gate'
            elif lines[y][x] == '-':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'tunel'
            elif lines[y][x] == '*':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'power'
            elif lines[y][x] == 'o':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                orange_spirit = SpiritSprite(all_sprites,
                                             load_image("sprites sheets/orange spirit/orange sheet top.png"), 4, 1,
                                             x * tile_size, y * tile_size, tile_size, width, height, lines, 'orange')
                orange_spirit.exp_direction = 'left'
            elif lines[y][x] == 'p':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                pink_spirit = SpiritSprite(all_sprites, load_image("sprites sheets/pink spirit/pink sheet bottom.png"),
                                           4,
                                           1, x * tile_size, y * tile_size, tile_size, width, height, lines, 'pink')
                pink_spirit.exp_direction = 'up'
            elif lines[y][x] == 'b':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                blue_spirit = SpiritSprite(all_sprites, load_image("sprites sheets/blue spirit/blue sheet top.png"), 4,
                                           1, x * tile_size, y * tile_size, tile_size, width, height, lines, 'blue')
                blue_spirit.exp_direction = 'right'
            elif lines[y][x] == 'r':
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                red_spirit = SpiritSprite(all_sprites, load_image("sprites sheets/red spirit/red sheet left.png"), 4, 1,
                                          x * tile_size, y * tile_size, tile_size, width, height, lines, 'red')
                red_spirit.exp_direction = 'left'
            elif lines[y][x] == "@":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                pacman = PacmanSprite(all_sprites, load_image("sprites sheets/pacman/pacman sheet left.png"), 4, 1,
                                      x * tile_size, y * tile_size, tile_size, width, height, lines)
                pacman.exp_direction = 'left'
            cells.append([x * tile_size, y * tile_size])

    ready_word = pygame.sprite.Sprite()
    ready_word.image = load_image("words/ready.png")
    ready_word.rect = ready_word.image.get_rect()
    ready_word.rect.x = tile_size * 8
    ready_word.rect.y = tile_size * 12 + tile_size // 4
    ready.add(ready_word)

    running = True
    while running:
        if lives == 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.exp_direction = 'right'
                    if countdown >= FPS * 5:
                        pacman.move = True
                elif event.key == pygame.K_LEFT:
                    pacman.exp_direction = 'left'
                    if countdown >= FPS * 5:
                        pacman.move = True
                elif event.key == pygame.K_UP:
                    pacman.exp_direction = 'up'
                    if countdown >= FPS * 5:
                        pacman.move = True
                elif event.key == pygame.K_DOWN:
                    pacman.exp_direction = 'down'
                    if countdown >= FPS * 5:
                        pacman.move = True

        screen.fill((0, 0, 0))
        for i in range(x_size):
            for j in range(y_size):
                if cells_drawing[' '.join([str(i * tile_size), str(j * tile_size)])] == 'wall':
                    pygame.draw.rect(screen, (0, 0, 255), (i * tile_size, j * tile_size, tile_size, tile_size))
                elif cells_drawing[' '.join([str(i * tile_size), str(j * tile_size)])] == 'power':
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (i * tile_size + (tile_size // 2), j * tile_size + (tile_size // 2)), 14)
        if countdown < FPS * 3:
            ready.draw(screen)
        else:
            all_sprites.draw(screen)
        if countdown >= FPS * 5:
            if power_countdown < 3 * FPS:
                red_spirit.injured_image = 'sprites sheets/injured start sheet.png'
                orange_spirit.injured_image  = 'sprites sheets/injured start sheet.png'
                blue_spirit.injured_image = 'sprites sheets/injured start sheet.png'
                pink_spirit.injured_image = 'sprites sheets/injured start sheet.png'
            elif 3 * FPS <= power_countdown < 5 * FPS:
                red_spirit.injured_image = 'sprites sheets/injured end sheet.png'
                orange_spirit.injured_image = 'sprites sheets/injured end sheet.png'
                blue_spirit.injured_image = 'sprites sheets/injured end sheet.png'
                pink_spirit.injured_image = 'sprites sheets/injured end sheet.png'
            else:
                red_spirit.injured = False
                orange_spirit.injured = False
                blue_spirit.injured = False
                pink_spirit.injured = False
                power_eaten = False
                power_countdown = 0
            if [round(pacman.pos[0] / tile_size, 0), round(pacman.pos[1] / tile_size, 1)] == [
                round(red_spirit.pos[0] / tile_size, 0), round(red_spirit.pos[1] / tile_size, 0)]:
                if red_spirit.injured:
                    red_spirit.pos = red_spirit.start_pos
                    red_spirit.injured = False
                    red_spirit.exp_direction = 'up'
                else:
                    pacman.move = False
                    red_spirit.move = False
                    orange_spirit.move = False
                    blue_spirit.move = False
                    pink_spirit.move = False
                    pacman.cut_sheet(load_image("sprites sheets/pacman/pacman death sheet.png"), 14, 1, pacman.pos[0],
                                     pacman.pos[1])
                    pacman.eaten = True
                    FPS = 5
            elif [round(pacman.pos[0] / tile_size, 0), round(pacman.pos[1] / tile_size, 1)] == [
                round(orange_spirit.pos[0] / tile_size, 0), round(orange_spirit.pos[1] / tile_size, 0)]:
                if orange_spirit.injured:
                    orange_spirit.pos = orange_spirit.start_pos
                    orange_spirit.injured = False
                    orange_spirit.exp_direction = 'up'
                else:
                    pacman.move = False
                    red_spirit.move = False
                    orange_spirit.move = False
                    blue_spirit.move = False
                    pink_spirit.move = False
                    pacman.cut_sheet(load_image("sprites sheets/pacman/pacman death sheet.png"), 14, 1, pacman.pos[0],
                                     pacman.pos[1])
                    pacman.eaten = True
                    FPS = 5
            elif [round(pacman.pos[0] / tile_size, 0), round(pacman.pos[1] / tile_size, 1)] == [
                round(blue_spirit.pos[0] / tile_size, 0), round(blue_spirit.pos[1] / tile_size, 0)]:
                if blue_spirit.injured:
                    blue_spirit.pos = blue_spirit.start_pos
                    blue_spirit.injured = False
                    blue_spirit.exp_direction = 'up'
                else:
                    pacman.move = False
                    red_spirit.move = False
                    orange_spirit.move = False
                    blue_spirit.move = False
                    pink_spirit.move = False
                    pacman.cut_sheet(load_image("sprites sheets/pacman/pacman death sheet.png"), 14, 1, pacman.pos[0],
                                     pacman.pos[1])
                    pacman.eaten = True
                    FPS = 5
            elif [round(pacman.pos[0] / tile_size, 0), round(pacman.pos[1] / tile_size, 1)] == [
                round(pink_spirit.pos[0] / tile_size, 0), round(pink_spirit.pos[1] / tile_size, 0)]:
                if pink_spirit.injured:
                    pink_spirit.pos = pink_spirit.start_pos
                    pink_spirit.injured = False
                    pink_spirit.exp_direction = 'up'
                else:
                    pacman.move = False
                    red_spirit.move = False
                    orange_spirit.move = False
                    blue_spirit.move = False
                    pink_spirit.move = False
                    pacman.cut_sheet(load_image("sprites sheets/pacman/pacman death sheet.png"), 14, 1, pacman.pos[0],
                                     pacman.pos[1])
                    pacman.eaten = True
                    FPS = 5
            else:
                if red_spirit.move:
                    if red_spirit.pos in cells:
                        if cells_drawing[
                            ' '.join([str(red_spirit.pos[0]), str(red_spirit.pos[1] - red_spirit.t_s)])] == 'gate':
                            red_spirit.exp_direction = 'up'
                            red_spirit.make_move(red_spirit.exp_direction)
                        else:
                            while True:
                                choice = random.choice(all_directions)
                                if red_spirit.try_cell(choice) and choice != opposite_directions[
                                    red_spirit.exp_direction]:
                                    red_spirit.exp_direction = choice
                                    red_spirit.make_move(red_spirit.exp_direction)
                                    break
                    else:
                        red_spirit.make_move(red_spirit.exp_direction)
                    red_spirit.update()
                if orange_spirit.move:
                    if orange_spirit.pos in cells:
                        if cells_drawing[' '.join(
                                [str(orange_spirit.pos[0]), str(orange_spirit.pos[1] - orange_spirit.t_s)])] == 'gate':
                            orange_spirit.exp_direction = 'up'
                            orange_spirit.make_move(orange_spirit.exp_direction)
                        else:
                            while True:
                                choice = random.choice(all_directions)
                                if orange_spirit.try_cell(choice) and choice != opposite_directions[
                                    orange_spirit.exp_direction]:
                                    orange_spirit.exp_direction = choice
                                    orange_spirit.make_move(orange_spirit.exp_direction)
                                    break
                    else:
                        orange_spirit.make_move(orange_spirit.exp_direction)
                    orange_spirit.update()
                if pink_spirit.move:
                    if pink_spirit.pos in cells:
                        if cells_drawing[
                            ' '.join([str(pink_spirit.pos[0]), str(pink_spirit.pos[1] - pink_spirit.t_s)])] == 'gate':
                            pink_spirit.exp_direction = 'up'
                            pink_spirit.make_move(pink_spirit.exp_direction)
                        else:
                            while True:
                                choice = random.choice(all_directions)
                                if pink_spirit.try_cell(choice) and choice != opposite_directions[
                                    pink_spirit.exp_direction]:
                                    pink_spirit.exp_direction = choice
                                    pink_spirit.make_move(pink_spirit.exp_direction)
                                    break
                    else:
                        pink_spirit.make_move(pink_spirit.exp_direction)
                    pink_spirit.update()
                if blue_spirit.move:
                    if blue_spirit.pos in cells:
                        if cells_drawing[
                            ' '.join([str(blue_spirit.pos[0]), str(blue_spirit.pos[1] - blue_spirit.t_s)])] == 'gate':
                            blue_spirit.exp_direction = 'up'
                            blue_spirit.make_move(blue_spirit.exp_direction)
                        else:
                            while True:
                                choice = random.choice(all_directions)
                                if blue_spirit.try_cell(choice) and choice != opposite_directions[
                                    blue_spirit.exp_direction]:
                                    blue_spirit.exp_direction = choice
                                    blue_spirit.make_move(blue_spirit.exp_direction)
                                    break
                    else:
                        blue_spirit.make_move(blue_spirit.exp_direction)
                    blue_spirit.update()
                if pacman.move:
                    if pacman.pos in cells:
                        if cells_drawing[' '.join([str(pacman.pos[0]), str(pacman.pos[1])])] == 'power':
                            power_eaten = True
                            cells_drawing[' '.join([str(pacman.pos[0]), str(pacman.pos[1])])] = 'empty'
                            power_countdown = 0
                            red_spirit.injured = True
                            blue_spirit.injured = True
                            orange_spirit.injured = True
                            pink_spirit.injured = True
                        if pacman.try_exp_move():
                            pacman.cur_direction = pacman.exp_direction
                            pacman.make_move(pacman.cur_direction)
                            pacman.move = True
                        elif pacman.try_cur_move():
                            pacman.make_move(pacman.cur_direction)
                            pacman.move = True
                        else:
                            pacman.move = False
                    else:
                        pacman.make_move(pacman.cur_direction)
                    pacman.update()
            if pacman.eaten:
                orange_spirit.kill()
                red_spirit.kill()
                blue_spirit.kill()
                pink_spirit.kill()
                if death_frame < len(pacman.frames) - 4:
                    pacman.update()
                    death_frame += 1
                else:
                    pacman.kill()
                    pacman.eaten = False
                    death_frame = 0
                    for x in range(x_size):
                        for y in range(y_size):
                            if lines[y][x] == 'r':
                                red_spirit = SpiritSprite(all_sprites,
                                                          load_image("sprites sheets/red spirit/red sheet left.png"), 4,
                                                          1, x * tile_size, y * tile_size, tile_size, width, height,
                                                          lines, 'red')
                                red_spirit.move = True
                            elif lines[y][x] == 'o':
                                orange_spirit = SpiritSprite(all_sprites,
                                                             load_image(
                                                                 "sprites sheets/orange spirit/orange sheet top.png"),
                                                             4,
                                                             1, x * tile_size, y * tile_size, tile_size, width, height,
                                                             lines, 'orange')
                                orange_spirit.move = True
                            elif lines[y][x] == 'b':
                                blue_spirit = SpiritSprite(all_sprites,
                                                           load_image("sprites sheets/blue spirit/blue sheet top.png"),
                                                           4,
                                                           1, x * tile_size, y * tile_size, tile_size, width, height,
                                                           lines, 'blue')
                                blue_spirit.move = True
                            elif lines[y][x] == 'p':
                                pink_spirit = SpiritSprite(all_sprites,
                                                           load_image(
                                                               "sprites sheets/pink spirit/pink sheet bottom.png"), 4,
                                                           1, x * tile_size, y * tile_size, tile_size, width, height,
                                                           lines, 'pink')
                                pink_spirit.move = True
                            elif lines[y][x] == "@":
                                pacman = PacmanSprite(all_sprites,
                                                      load_image("sprites sheets/pacman/pacman sheet left.png"), 4, 1,
                                                      x * tile_size, y * tile_size, tile_size, width, height, lines)
                                pacman.move = True
                    countdown = -1
                    FPS = 36
                    lives -= 1
        if power_eaten:
            power_countdown += 1
        countdown += 1
        pygame.display.flip()
        clock.tick(FPS)
    final_countdown = 0
    game_over = pygame.sprite.Sprite()
    game_over.image = load_image("words/game over.png")
    game_over.rect = game_over.image.get_rect()
    game_over.rect.x = tile_size * 6.5
    game_over.rect.y = tile_size * 12 + tile_size // 4
    over.add(game_over)
    while final_countdown < 3 * FPS:
        screen.fill((0, 0, 0))
        for i in range(x_size):
            for j in range(y_size):
                if cells_drawing[' '.join([str(i * tile_size), str(j * tile_size)])] == 'wall':
                    pygame.draw.rect(screen, (0, 0, 255), (i * tile_size, j * tile_size, tile_size, tile_size))
                elif cells_drawing[' '.join([str(i * tile_size), str(j * tile_size)])] == 'power':
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (i * tile_size + (tile_size // 2), j * tile_size + (tile_size // 2)), 14)
        over.draw(screen)
        final_countdown += 1
        pygame.display.flip()
        clock.tick(FPS)



if __name__ == '__main__':
    ready = pygame.sprite.Group()
    over = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    main()
