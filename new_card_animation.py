import pygame

tile_size = 32


class CardAnimation:
    def __init__(self):
        self.counter = 0
        self.y_mover = -17
        self.img_raw = pygame.image.load('data/images/card_mini_2.PNG').convert()
        self.img = pygame.transform.scale(self.img_raw, (tile_size/2, tile_size/2))
        self.img.set_colorkey((0, 0, 0))
        self.x = 0
        self.y = 0
        self.blit = True

    def animate_card(self, screen, x, y, fps_adjust):
        self.counter += 1*fps_adjust

        self.x = x
        self.y = y - 100 + round((1/3) * self.y_mover ** 2 + 32)

        if self.counter > 3 and self.y_mover < 20:
            self.y_mover += 1*fps_adjust

        if self.y_mover >= 20:
            self.blit = False

        if self.blit:
            screen.blit(self.img, (self.x + 8, self.y))




