import pygame


class ScrollBar:
    def __init__(self, height, space_height, content_height, position):
        self.scrollbar_surface = pygame.Surface((4, height))
        self.scrollbar_surface_rect = self.scrollbar_surface.get_rect()
        self.scrollbar_surface_rect.x = position[0]
        self.scrollbar_surface_rect.y = position[1]
        self.scrollbar_surface.set_colorkey((0, 0, 0))
        self.surf_alpha = 0
        self.scrollbar_surface.set_alpha(self.surf_alpha)
        self.scrollbar_colour = (62, 43, 75)
        self.ratio = space_height / content_height
        self.scroll_button = pygame.Surface((4, self.ratio * height))
        self.scroll_button_default_colour = (198, 198, 198)
        self.scroll_button_over_colour = (255, 255, 255)
        self.scroll_button.fill(self.scroll_button_default_colour)
        self.scroll_button_rect = self.scroll_button.get_rect()
        self.scroll_button_rect.x = position[0]
        self.scroll_button_rect.y = position[1]

        self.mouse_pos_on_button = 0
        self.scroll_button_clicked = False

        self.percentage = 0
        self.position = position
        self.height = height

        self.existence_counter = 0

    def draw_scroll_bar(self, screen, mouse_adjustment, events):

        mouse_pos = pygame.mouse.get_pos()

        self.surf_alpha += 15
        if self.surf_alpha <= 255:
            self.scrollbar_surface.set_alpha(self.surf_alpha)

        over_btn = False
        over_scroll = False

        if self.scroll_button_rect.collidepoint(mouse_pos[0] / mouse_adjustment, mouse_pos[1] / mouse_adjustment) \
                and pygame.mouse.get_focused():
            over_btn = True
            self.scroll_button.fill(self.scroll_button_over_colour)

        if self.scrollbar_surface_rect.collidepoint(mouse_pos[0] / mouse_adjustment, mouse_pos[1] / mouse_adjustment) \
                and pygame.mouse.get_focused():
            over_scroll = True

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and over_btn:
                self.mouse_pos_on_button = (mouse_pos[1] / mouse_adjustment) - self.scroll_button_rect.y
                self.scroll_button_clicked = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and over_scroll:
                self.scroll_button_rect.y = (mouse_pos[1] / mouse_adjustment) - self.scroll_button.get_height() / 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.scroll_button_clicked = False

        if not over_btn and not self.scroll_button_clicked:
            self.scroll_button.fill(self.scroll_button_default_colour)

        if self.scroll_button_clicked:
            self.scroll_button_rect.y = (mouse_pos[1] / mouse_adjustment) - self.mouse_pos_on_button

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


