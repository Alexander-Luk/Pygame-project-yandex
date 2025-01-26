import pygame
import sys



class Animation:
    animation_set_R = [pygame.image.load(f"data/pacman{i}.png") for i in range(0, 3)]
    animation_set_L = [pygame.image.load(f"data/pacman__{i}.png") for i in range(1, 4)]
    animation_set_S = [pygame.image.load(f"data/animka_SS{i}.png") for i in range(1, 4)]
    animation_set_SS = [pygame.image.load(f"data/animka_S{i}.png") for i in range(1, 4)]
    window = pygame.display.set_mode((600, 600))
    i = 0
    x = 200
    y = 20
    z = 0



    def end(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.window.fill((0, 0, 0))
            if event.type == pygame.QUIT:
                run = False
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and self.x > 0:
                self.x -= 8
                self.window.blit(self.animation_set_L[self.i], (self.x, self.y))
                self.i += 1
                if self.i == 2:
                    self.i = 0
                pygame.display.flip()
                pygame.time.Clock().tick(30)
            elif (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and self.x < 564:
                self.x += 8
                self.x += self.speedx
                self.window.blit(self.animation_set_R[self.i], (self.x, self.y))
                self.i += 1
                if self.i == 2:
                    self.i = 0
                pygame.display.flip()
                pygame.time.Clock().tick(30)
            elif (keystate[pygame.K_UP] or keystate[pygame.K_w]) and self.y > 0:
                self.y -= 8
                self.window.blit(self.animation_set_S[self.i], (self.x, self.y))
                self.i += 1
                if self.i == 2:
                    self.i = 0
                pygame.display.flip()
                pygame.time.Clock().tick(30)
            elif (keystate[pygame.K_DOWN] or keystate[pygame.K_s]) and self.y < 560:
                self.y += 8
                self.window.blit(self.animation_set_SS[self.i], (self.x, self.y))
                self.i += 1
                if self.i == 2:
                    self.i = 0
                print(self.x, self.y)
                pygame.display.flip()
                pygame.time.Clock().tick(30)


if __name__ == '__main__':
    app = Animation()
    app.end()
