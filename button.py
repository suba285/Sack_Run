import pygame._sdl2


class Button:
    def __init__(self, x, y, image1, image2, image3, fast_action=False):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.mask1 = pygame.mask.from_surface(self.image1)
        self.outline1 = pygame.mask.Mask.outline(self.mask1)
        self.outline1_surf = pygame.Surface((self.image1.get_width(), self.image1.get_height())).convert()
        self.outline1_surf.set_colorkey((0, 0, 0))
        for pixel in self.outline1:
            self.outline1_surf.set_at((pixel[0], pixel[1]), (255, 255, 255))

        self.fast_action = fast_action

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
        self.joystick_connected = False

    def draw_button(self, screen, card, mouse_adjustment, events, joystick_over, use_btn, use_key=False):
        action = False
        self.cursor_over = False
        self.image = self.image1
        self.image_rect.x = self.x
        self.image_rect.y = self.y
        self.joystick_over_button = joystick_over
        joystick_button = use_btn

        # cursor position
        pos = pygame.mouse.get_pos()
        try:
            if events['joyconnected']:
                self.joystick_connected = True
            else:
                self.joystick_connected = False
        except KeyError:
            self.joystick_connected = False

        if joystick_over:
            self.joystick_over_counter += 1
        else:
            self.joystick_over_counter = 0

        cursor_over = False
        if self.image_rect.collidepoint((pos[0] / mouse_adjustment[0] - mouse_adjustment[2],
                                         pos[1] / mouse_adjustment[0] - mouse_adjustment[1])):
            cursor_over = True
        if self.joystick_connected:
            cursor_over = False

        if cursor_over or self.joystick_over_button:
            self.image = self.image2
            self.cursor_over = True
            if events['mousebuttondown'] and not joystick_over:
                if events['mousebuttondown'].button == 1:
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True
                    if self.fast_action:
                        action = True
            if events['joybuttondown']:
                if events['joybuttondown'].button == joystick_button:
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True
                    if self.fast_action:
                        action = True
            if events['keydown'] and card:
                if events['keydown'].key == use_key:
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True
                    if self.fast_action:
                        action = True

        if events['mousebuttonup']:
           if events['mousebuttonup'].button == 1:
               if self.button_down and not self.fast_action:
                   action = True
               self.button_down = False
        if events['joybuttonup']:
            if events['joybuttonup'].button == joystick_button:
                if self.button_down and not self.fast_action:
                    action = True
                self.button_down = False
        if events['keyup'] and card:
            if events['keyup'].key == use_key:
                if self.button_down and not self.fast_action:
                    action = True
                self.button_down = False

        if self.button_down:
            self.image = self.image3

        screen.blit(self.image, self.image_rect)
        if (self.joystick_over_button or cursor_over) and not self.button_down and not card:
            if 255 >= self.joystick_over_counter * 40 > 0:
                self.outline1_surf.set_alpha(self.joystick_over_counter * 40)
            screen.blit(self.outline1_surf, self.image_rect)

        return action, self.cursor_over



