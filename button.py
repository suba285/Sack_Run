import pygame


class Button:
    def __init__(self, x, y, image1, image2, image3):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3

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
        self.joystick_over_button = joystick_over
        if card:
            joystick_button = 2
        else:
            joystick_button = 0

        # cursor position
        pos = pygame.mouse.get_pos()

        if joystick_over:
            self.joystick_over_counter += 1
        else:
            self.joystick_over_counter = 0

        if (self.image_rect.collidepoint((pos[0] / mouse_adjustment[0] - mouse_adjustment[2],
                                         pos[1] / mouse_adjustment[0] - mouse_adjustment[1])) and
            pygame.mouse.get_focused()) or \
                self.joystick_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.image2
            self.cursor_over = True
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not joystick_over) or \
                        (event.type == pygame.JOYBUTTONDOWN and event.button == joystick_button) or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_k and card):
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True

        for event in events:
            if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                    (event.type == pygame.JOYBUTTONUP and event.button == joystick_button) or \
                    (event.type == pygame.KEYUP and event.key == pygame.K_k and card):
                if self.button_down:
                    action = True
                self.button_down = False

        if self.button_down:
            self.image = self.image3

        screen.blit(self.image, self.image_rect)

        return action, self.cursor_over



