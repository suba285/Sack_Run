import pygame._sdl2

tile_size = 32


class CircleTransition:
    def __init__(self, screen):
        self.surface = screen
        self.final_radius = 400
        self.radius = 0
        self.model_radius = 0
        self.step = 13.3
        self.broken_step = 10
        self.trans = True
        self.x = 0
        self.y = 0
        self.get_small = False
        self.colour = (0, 0, 0)

    def draw_circle_transition(self, sack_rect, fps_adjust):
        self.x = sack_rect.x + tile_size / 2
        self.y = sack_rect.y + 15
        if self.trans:
            if self.radius >= self.final_radius:
                self.get_small = True
            if self.get_small:
                self.model_radius -= self.step * fps_adjust
                self.radius = self.model_radius
            else:
                self.model_radius += self.step * fps_adjust
                self.radius = self.model_radius
            if self.radius > 0:
                pygame.draw.circle(self.surface, self.colour, (self.x, self.y), self.radius)

            if self.radius < 0:
                self.radius = 0
                self.trans = False

        return self.trans
