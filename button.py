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

    def draw_button(self, screen, card, mouse_adjustment, events):
        action = False
        self.cursor_over = False
        self.image = self.image1
        self.image_rect.x = self.x
        self.image_rect.y = self.y

        # cursor position
        pos = pygame.mouse.get_pos()

        if self.image_rect.collidepoint((pos[0] / mouse_adjustment,
                                         pos[1] / mouse_adjustment)) and pygame.mouse.get_focused():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.image2
            self.cursor_over = True
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.image = self.image1
                    self.image_rect.x = self.x
                    self.image_rect.y = self.y
                    self.button_down = True

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.button_down:
                    action = True
                self.button_down = False

        if self.button_down:
            self.image = self.image3

        screen.blit(self.image, self.image_rect)

        return action, self.cursor_over


def inactive_button(x, y, image, mouse_adjustment):
    # cursor position
    pos = pygame.mouse.get_pos()
    rect = image.get_rect()
    rect.x = x
    rect.y = y
    if rect.collidepoint((pos[0] / mouse_adjustment, pos[1] / mouse_adjustment)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)


