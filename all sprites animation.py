import pygame
import os
import sys


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


class PacmanSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, t_s, width, height):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = [x, y]
        self.cur_direction = "left"
        self.exp_direction = "left"
        self.move = True
        self.mask = pygame.mask.from_surface(self.image)
        self.t_s = t_s
        self.width = width
        self.height = height
        self.way_searching = False

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
                if cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] == 'empty':
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] + self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'left':
            if ' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])]) in cells_drawing:
                if cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] == 'empty':
                    return True
                else:
                    return False
            else:
                cells_drawing[' '.join([str(self.pos[0] - self.t_s), str(self.pos[1])])] = 'empty'
                return True
        elif direction == 'up':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] - self.t_s)])] == 'empty':
                return True
            else:
                return False
        elif direction == 'down':
            if cells_drawing[' '.join([str(self.pos[0]), str(self.pos[1] + self.t_s)])] == 'empty':
                return True
            else:
                return False

    def make_move(self, direction):
        global pacman_sheets
        if direction == 'right':
            self.pos[0] += self.t_s // 3
        elif direction == 'left':
            self.pos[0] -= self.t_s // 3
        elif direction == 'up':
            self.pos[1] -= self.t_s // 3
        elif direction == 'down':
            self.pos[1] += self.t_s // 3
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
    tile_size = 39
    pygame.init()
    size = width, height = tile_size * x_size, tile_size * y_size
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 18

    for x in range(x_size):
        for y in range(y_size):
            if lines[y][x] == ".":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
            elif lines[y][x] == "#":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'wall'
            elif lines[y][x] == "@":
                cells_drawing[' '.join([str(x * tile_size), str(y * tile_size)])] = 'empty'
                pacman = PacmanSprite(all_sprites, load_image("sprites sheets/pacman/pacman sheet left.png"), 4, 1, x * tile_size, y * tile_size, tile_size, width, height)
            cells.append([x * tile_size, y * tile_size])
                    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.exp_direction = 'right'
                elif event.key == pygame.K_LEFT:
                    pacman.exp_direction = 'left'
                elif event.key == pygame.K_UP:
                    pacman.exp_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    pacman.exp_direction = 'down'
            
        screen.fill((0, 0, 0))
        for i in range(x_size):
            for j in range(y_size):
                if cells_drawing[' '.join([str(i * tile_size), str(j * tile_size)])] == 'wall':
                    pygame.draw.rect(screen, (0, 0, 255), (i * tile_size, j * tile_size, tile_size, tile_size))
        all_sprites.draw(screen)
        if pacman.pos in cells:
            if pacman.try_exp_move():
                pacman.cur_direction = pacman.exp_direction
                pacman.make_move(pacman.cur_direction)
                pacman.move = True
            elif pacman.try_cur_move():
                pacman.make_move(pacman.cur_direction)
                pacman.move  = True
            else:
                    pacman.move = False
        else:
            pacman.make_move(pacman.cur_direction)
        if pacman.move:
            pacman.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    main()
