import pygame
from image_loader import img_loader
from font_manager import Text
from button import Button
from button import inactive_button

tile_size = 32

sheight = 264
swidth = 352


class LevelSelection:
    def __init__(self, world_count):
        button_size = tile_size * 0.75

        self.world_count = world_count

        self.menu_background = img_loader('data/images/menu_background.PNG', swidth, sheight)

        self.left_button = img_loader('data/images/button_left.PNG', button_size, button_size)
        self.left_button_press = img_loader('data/images/button_left_press.PNG', button_size, button_size)
        self.left_button_down = img_loader('data/images/button_left_down.PNG', button_size, button_size)

        self.right_button = pygame.transform.flip(self.left_button, True, False)
        self.right_button_press = pygame.transform.flip(self.left_button_press, True, False)
        self.right_button_down = pygame.transform.flip(self.left_button_down, True, False)

        self.right_button_grey = img_loader('data/images/button_right_grey.PNG', button_size, button_size)
        self.left_button_grey = pygame.transform.flip(self.right_button_grey, True, False)

        self.arrow_button_mask = pygame.mask.from_surface(self.right_button)
        self.arrow_button_outline = pygame.mask.Mask.outline(self.arrow_button_mask)
        self.arrow_button_outline_surf = pygame.Surface((button_size, button_size))
        self.arrow_button_outline_surf.set_colorkey((0, 0, 0))
        for pixel in self.arrow_button_outline:
            self.arrow_button_outline_surf.set_at((pixel[0], pixel[1]), (255, 255, 255))

        self.menu_button = img_loader('data/images/button_back.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_press = img_loader('data/images/button_back_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_down = img_loader('data/images/button_back_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.play_button = img_loader('data/images/button_play2.PNG', tile_size, tile_size * 0.75)
        self.play_button_press = img_loader('data/images/button_play2_press.PNG', tile_size, tile_size * 0.75)
        self.play_button_down = img_loader('data/images/button_play_down.PNG', tile_size, tile_size * 0.75)

        self.tut = Text()
        self.tutorial = self.tut.make_text(["'tutorial'"])

        self.tut_desc = Text()
        self.tutorial_description = self.tut_desc.make_text(["learn the basics the game"])

        self.wrld1 = Text()
        self.world1_txt = self.wrld1.make_text(["'world 1'"])

        self.wrld1_desc = Text()
        self.world1_description = self.wrld1_desc.make_text(["a run through 'climbton farm' where bees are kept"])

        self.wrld2 = Text()
        self.world2_txt = self.wrld2.make_text(["'world 2'"])

        self.wrld2_desc = Text()
        self.world2_description = self.wrld2_desc.make_text(["coming soon..."])
        # caves stretching below the farm, bats live there

        self.wrld3 = Text()
        self.world3_txt = self.wrld3.make_text(["'world 3'"])

        self.wrld3_desc = Text()
        self.world3_description = self.wrld3_desc.make_text(["coming soon..."])
        # an ancient forest with ancient inhabitants

        spacing = 20
        self.button_y = sheight / 3

        self.left_x = swidth / 2 - self.world1_txt.get_width() / 2 - spacing - button_size
        self.right_x = swidth / 2 + self.world1_txt.get_width() / 2 + spacing

        menu_w = self.menu_button.get_width()
        play_w = self.play_button.get_width()

        self.left_btn = Button(self.left_x, self.button_y,
                               self.left_button, self.left_button_press, self.left_button_down)
        self.right_btn = Button(self.right_x, self.button_y,
                                self.right_button, self.right_button_press, self.right_button_down)
        self.menu_btn = Button(swidth * (1/3) - menu_w / 2 + 10, sheight * (2/3),
                               self.menu_button, self.menu_button_press, self.menu_button_down)

        self.play_btn = Button(swidth * (2/3) - play_w / 2 - 8, sheight * (2/3),
                               self.play_button, self.play_button_press, self.play_button_down)

        self.joystick_counter = -1
        self.joystick_moved = False

    def draw_level_selection(self, level_screen, mouse_adjustment, events):

        level_screen.blit(self.menu_background, (0, 0))

        update_value = 0

        left_press = False
        right_press = False
        menu_press = False
        play_press = False
        over = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        text = self.world1_txt
        description = self.world1_description

        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if abs(event.value) > 0.3 and not self.joystick_moved:
                        self.joystick_counter = self.joystick_counter * -1
                        self.joystick_moved = True
                    if event.value == 0:
                        self.joystick_moved = False
                if event.axis == 1:
                    if event.value > 0.3 and not self.joystick_moved:
                        if self.joystick_counter >= 1:
                            self.joystick_counter -= 1
                            if self.joystick_counter < 1:
                                self.joystick_counter = 1
                            self.joystick_moved = True
                        if self.joystick_counter <= -1:
                            self.joystick_counter += 1
                            if self.joystick_counter > -1:
                                self.joystick_counter = -1
                            self.joystick_moved = True
                    if event.value < -0.3 and not self.joystick_moved:
                        if self.joystick_counter >= 1:
                            self.joystick_counter += 1
                            if self.joystick_counter > 2:
                                self.joystick_counter = 2
                            self.joystick_moved = True
                        if self.joystick_counter <= -1:
                            self.joystick_counter -= 1
                            if self.joystick_counter < -2:
                                self.joystick_counter = -2
                            self.joystick_moved = True
                    if event.value == 0:
                        self.joystick_moved = False

        joystick_over1 = False
        joystick_over2 = False
        joystick_over_1 = False
        joystick_over_2 = False

        if self.joystick_counter == 1:
            joystick_over1 = True
        if self.joystick_counter == 2:
            joystick_over2 = True
        if self.joystick_counter == -1:
            joystick_over_1 = True
        if self.joystick_counter == -2:
            joystick_over_2 = True

        if self.world_count > 1:
            left_press, over1 = self.left_btn.draw_button(level_screen, False, mouse_adjustment, events, joystick_over2)
        else:
            level_screen.blit(self.left_button_grey, (self.left_x, self.button_y))
            inactive_button(self.left_x, self.button_y, self.left_button_grey,
                            mouse_adjustment)
            if joystick_over2:
                level_screen.blit(self.arrow_button_outline_surf, (self.left_x, self.button_y))
        if self.world_count < 4:
            right_press, over2 = self.right_btn.draw_button(level_screen, False, mouse_adjustment, events,
                                                            joystick_over_2)
        else:
            level_screen.blit(self.right_button_grey, (self.right_x, self.button_y))
            inactive_button(self.right_x, self.button_y, self.right_button_grey,
                            mouse_adjustment)
            if joystick_over_2:
                level_screen.blit(self.arrow_button_outline_surf, (self.right_x, self.button_y))

        menu_press, over3 = self.menu_btn.draw_button(level_screen, False, mouse_adjustment, events, joystick_over1)
        if self.world_count <= 2:
            play_press, over4 = self.play_btn.draw_button(level_screen, False, mouse_adjustment, events,
                                                          joystick_over_1)

        if left_press:
            update_value = -1
        elif right_press:
            update_value = 1

        self.world_count += update_value
        if self.world_count < 1:
            self.world_count = 1
        if self.world_count > 4:
            self.world_count = 4

        if self.world_count == 1:
            text = self.tutorial
            description = self.tutorial_description
        if self.world_count == 2:
            text = self.world1_txt
            description = self.world1_description
        elif self.world_count == 3:
            text = self.world2_txt
            description = self.world2_description
        elif self.world_count == 4:
            text = self.world3_txt
            description = self.world3_description

        level_screen.blit(text, (swidth / 2 - text.get_width() / 2, self.button_y + 6))
        level_screen.blit(description, (swidth / 2 - description.get_width() / 2, self.button_y + 40))

        if over1 or over2 or over3 or over4:
            over = True

        return play_press, menu_press, over, self.world_count



