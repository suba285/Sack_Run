import pygame
import json
from image_loader import img_loader


class Slider:
    def __init__(self, x, y):
        self.knob = img_loader('data/images/slider_knob.PNG', 8, 10)
        self.knob_rect = self.knob.get_rect()
        know_mask = pygame.mask.from_surface(self.knob)
        self.knob_highlight = pygame.Surface((8, 10))
        self.knob_highlight.set_colorkey((0, 0, 0))
        outline = pygame.mask.Mask.outline(know_mask)
        for pixel in outline:
            self.knob_highlight.set_at(pixel, (255, 255, 255))
        self.steps = 10
        self.width = 110
        self.pos = [x, y]
        self.slider_bg = pygame.Surface((120, 10))
        self.slider_bg.fill((77, 41, 78))
        self.slider = img_loader('data/images/slider.PNG', 120, 10)
        self.slider_rect = self.slider.get_rect()
        self.slider_rect.x = x - 5
        self.slider_rect.y = y - 4
        self.slider_highlight = img_loader('data/images/slider_highlight.PNG', 120, 10)
        try:
            with open('data/settings_configuration.json', 'r') as json_file:
                settings_configuration = json.load(json_file)
                self.value = settings_configuration['music_volume']
        except FileNotFoundError:
            self.value = 0.5
        self.step = round(self.value * self.steps)

        self.mouse_btn_is_pressed = False

        self.knob_rect.center = (x + round(self.width * self.value), self.pos[1] + 1)

    def draw_slider(self, screen, mouse_adjustment, events, left_press, right_press):
        pos = pygame.mouse.get_pos()
        mouse_pos = (pos[0] / mouse_adjustment[0] - mouse_adjustment[2],
                     pos[1] / mouse_adjustment[0] - mouse_adjustment[1])

        over_knob = False

        # joystick operations (reduced to left or right)
        self.step = round(self.value * self.steps)
        if left_press and self.step > 0:
            self.step -= 1
            self.value = self.step / 10
        if right_press and self.step < self.steps:
            self.step += 1
            self.value = self.step / 10

        # detecting slider knob press (drag control)
        if self.knob_rect.collidepoint(mouse_pos):
            over_knob = True
            if events['mousebuttondown']:
                self.mouse_btn_is_pressed = True
        # adjusting slider with clicking
        elif self.slider_rect.collidepoint(mouse_pos) and not self.mouse_btn_is_pressed:
            if events['mousebuttondown']:
                if events['mousebuttondown'].button == 1:
                    rel_x = mouse_pos[0] - self.pos[0]
                    self.value = rel_x / self.width
        # turning slider value into knob x
        self.knob_rect.center = (self.pos[0] + round(self.width * self.value), self.pos[1] + 1)
        # dragging slider knob to adjust value
        if self.mouse_btn_is_pressed:
            self.knob_rect.x = mouse_pos[0] - 4
            if self.knob_rect.center[0] < self.pos[0]:
                self.knob_rect.x = self.pos[0] - 4
            if self.knob_rect.center[0] > self.pos[0] + self.width:
                self.knob_rect.x = self.pos[0] + self.width - 4

        if events['mousebuttonup']:
            self.mouse_btn_is_pressed = False

        self.value = (self.knob_rect.center[0] - self.pos[0]) / self.width

        if self.value > 1:
            self.value = 1
        if self.value < 0:
            self.value = 0

        slider_highlight = pygame.transform.scale(self.slider_highlight, (round(self.width * self.value) + 4, 10))
        slider_bg = self.slider_bg.copy()
        slider_bg.blit(slider_highlight, (0, 0))
        slider_bg.blit(self.slider, (0, 0))
        slider_bg.set_colorkey((255, 0, 255))
        screen.blit(slider_bg, self.slider_rect)
        screen.blit(self.knob, self.knob_rect)
        if over_knob or self.mouse_btn_is_pressed:
            screen.blit(self.knob_highlight, self.knob_rect)

        return self.value, self.mouse_btn_is_pressed
