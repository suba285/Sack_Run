import pygame._sdl2


class ScrollBar:
    def __init__(self, height, space_height, content_height, position):
        self.scrollbar_surface = pygame.Surface((4, height)).convert_alpha()
        self.scrollbar_surface_rect = self.scrollbar_surface.get_rect()
        self.scrollbar_surface_rect.x = position[0]
        self.scrollbar_surface_rect.y = position[1]
        self.scrollbar_surface.set_colorkey((0, 0, 0))
        self.surf_alpha = 0
        self.scrollbar_surface.set_alpha(self.surf_alpha)
        self.scrollbar_colour = (62, 43, 75)
        self.ratio = space_height / content_height
        self.scroll_button = pygame.Surface((4, self.ratio * height)).convert_alpha()
        self.scroll_button_default_colour = (198, 198, 198)
        self.scroll_button_over_colour = (255, 255, 255)
        self.scroll_button.fill(self.scroll_button_default_colour)
        self.scroll_button_rect = self.scroll_button.get_rect()
        self.scroll_button_rect.x = position[0]
        self.scroll_button_rect.y = position[1]

        self.mouse_pos_on_button = 0
        self.scroll_button_clicked = False

        self.over_btn = False
        self.over_scroll = False

        self.percentage = 0
        self.position = position
        self.height = height

        self.existence_counter = 0

        self.scroll_value = 0
        self.scrolling = False
        self.scroll_speed = 2

    def draw_scroll_bar(self, screen, mouse_adjustment, events, joysticks, joystick_controls):

        mouse_pos = pygame.mouse.get_pos()

        hat_value = [0, 0]

        self.surf_alpha += 15
        if self.surf_alpha <= 255:
            self.scrollbar_surface.set_alpha(self.surf_alpha)

        if not joysticks:
            if self.scroll_value > 0:
                self.scroll_value -= 0.2
                if self.scroll_value < 0:
                    self.scroll_value = 0
            if self.scroll_value < 0:
                self.scroll_value += 0.2
                if self.scroll_value > 0:
                    self.scroll_value = 0

        if events['mousebuttondown']:
            if events['mousebuttondown'].button == 1 and self.over_btn:
                self.mouse_pos_on_button = (mouse_pos[1] / mouse_adjustment[0]) - self.scroll_button_rect.y
                self.scroll_button_clicked = True
        if events['mousebuttondown']:
            if events['mousebuttondown'].button == 1 and self.over_scroll:
                self.scroll_button_rect.y = (mouse_pos[1] / mouse_adjustment[0]) - self.scroll_button.get_height() / 2
        if events['mousebuttonup']:
            if events['mousebuttonup'].button == 1:
                self.scroll_button_clicked = False
        if events['mousewheel']:
            event = events['mousewheel']
            if event.y != 0:
                self.scroll_value = self.scroll_speed * -event.y
        if events['joyaxismotion_y']:
            event = events['joyaxismotion_y']
            self.scroll_value = self.scroll_speed * event.value
            self.scrolling = True
            if abs(event.value) < 0.05:
                self.scrolling = False
        if events['joybuttondown']:
            event = events['joybuttondown']
            if joystick_controls[0]:
                if event.button == joystick_controls[0][1]:  # down
                    hat_value[1] = -1
                if event.button == joystick_controls[0][3]:  # up
                    hat_value[1] = 1

        if joysticks and joysticks[0].get_numhats() > 0:
            hat_value = joysticks[0].get_hat(0)

        if not self.scrolling and hat_value[1] != 0:
            self.scroll_value = self.scroll_speed * -hat_value[1]

        if (self.scroll_button_rect.collidepoint(mouse_pos[0] / mouse_adjustment[0],
                                                 mouse_pos[1] / mouse_adjustment[0] - mouse_adjustment[1])
                and pygame.mouse.get_focused()) or (abs(self.scroll_value) > 0 and joysticks):
            self.over_btn = True
            self.scroll_button.fill(self.scroll_button_over_colour)
        else:
            self.over_btn = False

        if self.scrollbar_surface_rect.collidepoint(mouse_pos[0] / mouse_adjustment[0] - mouse_adjustment[2],
                                                    mouse_pos[1] / mouse_adjustment[0] - mouse_adjustment[1])\
                and pygame.mouse.get_focused():
            self.over_scroll = True
        else:
            self.over_scroll = False

        if not self.over_btn and not self.scroll_button_clicked:
            self.scroll_button.fill(self.scroll_button_default_colour)

        self.scroll_button_rect.y += self.scroll_value

        if self.scroll_button_clicked:
            self.scroll_button_rect.y = (mouse_pos[1] / mouse_adjustment[0]) - self.mouse_pos_on_button

        if self.scroll_button_rect.top < self.position[1]:
            self.scroll_button_rect.top = self.position[1]
        if self.scroll_button_rect.bottom > self.position[1] + self.height:
            self.scroll_button_rect.bottom = self.position[1] + self.height

        self.percentage = (self.scroll_button_rect.y - self.position[1]) / (self.height * (1 - self.ratio))

        self.scrollbar_surface.fill(self.scrollbar_colour)
        self.scrollbar_surface.blit(self.scroll_button, (0, self.scroll_button_rect.y - self.position[1]))

        self.scrollbar_surface.set_at((0, 0), (0, 0, 0))
        self.scrollbar_surface.set_at((3, 0), (0, 0, 0))
        self.scrollbar_surface.set_at((3, self.height - 1), (0, 0, 0))
        self.scrollbar_surface.set_at((0, self.height - 1), (0, 0, 0))
        screen.blit(self.scrollbar_surface, self.position)

        return self.percentage


