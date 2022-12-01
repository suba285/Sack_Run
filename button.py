import pygame


class Button:
    def __init__(self, x, y, image1, image2, image3):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.mask1 = pygame.mask.from_surface(self.image1)
        self.outline1 = pygame.mask.Mask.outline(self.mask1)
        self.outline1_surf = pygame.Surface((self.image1.get_width(), self.image1.get_height())).convert()
        self.outline1_surf.set_colorkey((0, 0, 0))
        for pixel in self.outline1:
            self.outline1_surf.set_at((pixel[0], pixel[1]), (255, 255, 255))

        self.image = self.image1
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.x = x
        self.y = y
        self.coordinates = (self.x, self.y)
        self.cursor_list = []
        self.clicked = False
        self.cursor_over = False
        self.play_over_sound = True
        self.button_down = False
        self.joystick_over_button = False
        self.joystick_over_counter = 0

    def draw_button(self, screen, card, mouse_adjustment, events, joystick_over):
        action = False
        self.cursor_over = False
        self.image = self.image1
        self.image_rect.x = self.x
        self.image_rect.y = self.y
        joystick_count = pygame.joystick.get_count()
        self.joystick_over_button = joystick_over
        if card:
            joystick_button = 2
        else:
            joystick_button = 0
        if joystick_count == 0:
            self.joystick_over_button = False

        # cursor position
        pos = pygame.mouse.get_pos()

        if joystick_over:
            self.joystick_over_counter += 1
        else:
            self.joystick_over_counter = 0

        if (self.image_rect.collidepoint((pos[0] / mouse_adjustment[0] - mouse_adjustment[2],
                                         pos[1] / mouse_adjustment[0] - mouse_adjustment[1])) and
            pygame.mouse.get_focused() and joystick_count == 0) or \
                self.joystick_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.image2
            self.cursor_over = True
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not joystick_over) or \
                        (event.type == pygame.JOYBUTTONDOWN and event.button == joystick_button):
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True

        for event in events:
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                    (event.type == pygame.JOYBUTTONUP and event.button == joystick_button):
                if self.button_down:
                    action = True
                self.button_down = False

        if self.button_down:
            self.image = self.image3

        screen.blit(self.image, self.image_rect)
        if self.joystick_over_button and not self.button_down and not card:
            if 255 >= self.joystick_over_counter > 0:
                self.outline1_surf.set_alpha(self.joystick_over_counter * 51)
            screen.blit(self.outline1_surf, self.image_rect)

        return action, self.cursor_over


def inactive_button(x, y, image, mouse_adjustment):
    # cursor position
    pos = pygame.mouse.get_pos()
    rect = image.get_rect()
    rect.x = x
    rect.y = y
    if rect.collidepoint((pos[0] / mouse_adjustment[0] - mouse_adjustment[1], pos[1] / mouse_adjustment[0])):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)


