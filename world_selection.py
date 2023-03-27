import pygame._sdl2
import json
import random
import math
from image_loader import img_loader
from font_manager import Text
from button import Button
from screen_info import swidth, sheight

tile_size = 32


class LevelSelection:
    def __init__(self, world_count):
        text = Text()
        self.text = Text()

        button_size = tile_size * 0.75

        try:
            with open('data/unlocked_worlds.json', 'r') as json_file:
                self.world_status = json.load(json_file)

        except FileNotFoundError:
            self.world_status = [True, False, False, False]

        try:
            with open('data/times.json', 'r') as json_file:
                times_data = json.load(json_file)
                time1 = text.make_text([times_data['1']])
                time2 = text.make_text([times_data['2']])
                time3 = text.make_text([times_data['3']])
                time4 = text.make_text([times_data['4']])
        except FileNotFoundError:
            no_data_txt = text.make_text(['no data'])
            time1 = no_data_txt
            time2 = no_data_txt
            time3 = no_data_txt
            time4 = no_data_txt

        self.times = {
            '1': time1,
            '2': time2,
            '3': time3,
            '4': time4
        }

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

        self.rb_button = img_loader('data/images/buttons/button_rb.PNG', tile_size / 2, tile_size / 2)
        self.rb_button_press = img_loader('data/images/buttons/button_rb_press.PNG', tile_size / 2, tile_size / 2)
        self.lb_button = img_loader('data/images/buttons/button_lb.PNG', tile_size / 2, tile_size / 2)
        self.lb_button_press = img_loader('data/images/buttons/button_lb_press.PNG', tile_size / 2, tile_size / 2)

        self.lock_animation = {}
        for file in range(1, 12):
            self.lock_animation[file - 1] = img_loader(f'data/images/lock_animation/lock{file}.PNG',
                                                       tile_size, tile_size)

        tutorial_txt = text.make_text(["The Beginning"])

        tutorial_description = text.make_text(["An introduction to the game"])

        world1_txt = text.make_text(["Climbton Farm"])

        world1_description = text.make_text(["A run through the farm where bees are kept"])

        world2_txt = text.make_text(["Sizzle Caves"])

        world2_description = text.make_text(["Lava caves beneath the farm, numerous sightings of bats"])

        world3_txt = text.make_text(["'Home' Run"])

        world3_description = text.make_text(["A barn obstacle course"])

        self.world_locked_txt = text.make_text(['LEVEL LOCKED'])

        self.descriptions = {
            0: tutorial_description,
            1: world1_description,
            2: world2_description,
            3: world3_description
        }

        self.titles = {
            0: tutorial_txt,
            1: world1_txt,
            2: world2_txt,
            3: world3_txt
        }

        spacing = 20
        self.button_y = sheight / 3

        self.left_x = swidth / 2 - world1_txt.get_width() / 2 - spacing - button_size
        self.right_x = swidth / 2 + world1_txt.get_width() / 2 + spacing

        menu_w = self.menu_button.get_width()
        play_w = self.play_button.get_width()

        self.left_btn = Button(self.left_x, self.button_y,
                               self.left_button, self.left_button_press, self.left_button_down, True)
        self.right_btn = Button(self.right_x, self.button_y,
                                self.right_button, self.right_button_press, self.right_button_down, True)
        self.menu_btn = Button(swidth * (1/3) - menu_w / 2 + 10, sheight * (2/3),
                               self.menu_button, self.menu_button_press, self.menu_button_down)

        self.play_btn = Button(swidth * (2/3) - play_w / 2 - 8, sheight * (2/3),
                               self.play_button, self.play_button_press, self.play_button_down)

        self.new_world_animation_counter = 0
        self.lock_animation_counter = 0
        self.new_world_dim_surf = pygame.Surface((swidth, sheight))
        self.new_world_dim_surf.fill((0, 0, 0))
        self.new_world_dim_surf.set_alpha(0)
        self.new_world_dim_surf_max_alpha = 80
        self.new_world_dim_surf_alpha = 0
        self.new_world_dim_surf.set_colorkey((255, 255, 255))
        self.new_world_circle_radius = 0

        self.new_world_animation_stage0 = - 2 * 60
        self.new_world_animation_stage1 = -1.5 * 60
        self.new_world_animation_stage2 = -0.5 * 60
        self.new_world_animation_stage3 = -0.3 * 60

        self.joystick_counter = -1
        self.joystick_moved = False
        self.hat_x_pressed = False

        self.left_bumper_press = False
        self.right_bumper_press = False

        self.object_wobble_counter = 0
        self.text_wobble_default_value = 10

        self.lock_sound_played = False

    def update_times(self):
        try:
            with open('data/unlocked_worlds.json', 'r') as json_file:
                self.world_status = json.load(json_file)

        except FileNotFoundError:
            self.world_status = [True, False, False, False]

        try:
            with open('data/times.json', 'r') as json_file:
                times_data = json.load(json_file)
                time1 = self.text.make_text([times_data['1']])
                time2 = self.text.make_text([times_data['2']])
                time3 = self.text.make_text([times_data['3']])
                time4 = self.text.make_text([times_data['4']])
        except FileNotFoundError:
            no_data_txt = self.text.make_text(['no data'])
            time1 = no_data_txt
            time2 = no_data_txt
            time3 = no_data_txt
            time4 = no_data_txt

        self.times = {
            '1': time1,
            '2': time2,
            '3': time3,
            '4': time4
        }

    def draw_level_selection(self, level_screen, mouse_adjustment, events, controls, joysticks, fps_adjust,
                             world_count, new_world_unlocked, speedrun_mode):

        level_screen.blit(self.menu_background, (0, 0))
        self.new_world_dim_surf.fill((0, 0, 0))

        self.world_count = world_count

        update_value = 0

        sounds = {
            'lock': False,
            'swoosh': False,
            'button': False
        }

        self.new_world_animation_counter += 1 * fps_adjust

        local_events = events
        if self.new_world_animation_counter < 0:
            local_events = {
                'quit': False,
                'keydown': False,
                'keyup': False,
                'mousebuttondown': False,
                'mousebuttonup': False,
                'joyaxismotion_x': False,
                'joyaxismotion_y': False,
                'joybuttondown': False,
                'joybuttonup': False,
                'joydeviceadded': False,
                'joydeviceremoved': False,
                'videoresize': False
            }

        if 0 > self.new_world_animation_counter > self.new_world_animation_stage1:
            self.lock_animation_counter += 1/3

        if new_world_unlocked:
            self.lock_sound_played = False
            self.new_world_animation_counter = self.new_world_animation_stage0
            self.lock_animation_counter = 0
            self.new_world_circle_radius = 0
            self.new_world_dim_surf.set_alpha(self.new_world_dim_surf_max_alpha)
            self.new_world_dim_surf_alpha = self.new_world_dim_surf_max_alpha
            self.world_count += 1
            new_world_unlocked = False

        self.object_wobble_counter -= 1 * fps_adjust

        left_press = False
        right_press = False
        play_press = False
        left_bumper_press = False
        right_bumper_press = False
        over = False
        over1 = False
        over2 = False
        over3 = False
        over4 = False

        if events['joyaxismotion_x']:
            event = events['joyaxismotion_x']
            # right and left
            if abs(event.value) > 0.3 and not self.joystick_moved:
                self.joystick_counter *= -1
                self.joystick_moved = True
            if event.value == 0:
                self.joystick_moved = False
        if events['joybuttondown']:
            event = events['joybuttondown']
            if event.button == controls['configuration'][1]:
                self.left_bumper_press = True
                left_bumper_press = True
            if event.button == controls['configuration'][2]:
                self.right_bumper_press = True
                right_bumper_press = True
        if events['joybuttonup']:
            self.left_bumper_press = False
            self.right_bumper_press = False

        # D-pad input
        if joysticks:
            hat_value = joysticks[0].get_hat(0)
            if not self.hat_x_pressed:
                # left and right
                if abs(hat_value[0]) == 1:
                    self.joystick_counter *= -1
                    self.hat_x_pressed = True
            if hat_value[0] == 0:
                self.hat_x_pressed = False

        joystick_over1 = False
        joystick_over2 = False
        joystick_over_1 = False
        joystick_over_2 = False

        description = self.descriptions[self.world_count - 1]
        title = self.titles[self.world_count - 1]
        time = self.times[str(self.world_count)]

        if self.object_wobble_counter > 0:
            object_wobble = math.sin((self.text_wobble_default_value - self.object_wobble_counter)) * 3
        else:
            object_wobble = 0

        level_screen.blit(title, (swidth / 2 - title.get_width() / 2 + object_wobble, self.button_y + 6))
        if speedrun_mode == 2:
            level_screen.blit(time, (swidth / 2 - time.get_width() / 2, 50))
        if self.world_status[self.world_count - 1] and self.new_world_animation_counter > 0:
            level_screen.blit(description, (swidth / 2 - description.get_width() / 2, self.button_y + 40))

        if self.new_world_animation_stage3 < self.new_world_animation_counter < 0:
            if self.new_world_circle_radius == 0:
                sounds['swoosh'] = True
            self.new_world_circle_radius += 20 * fps_adjust
            pygame.draw.circle(self.new_world_dim_surf, (255, 255, 255), (swidth / 2, sheight / 2),
                               self.new_world_circle_radius, 0)
            if self.new_world_circle_radius > 200 and self.new_world_dim_surf_alpha > 0:
                self.new_world_dim_surf_alpha = 0

        if self.new_world_animation_counter >= 0:
            if not self.world_status[self.world_count - 1]:
                self.new_world_dim_surf_alpha += 4 * fps_adjust
                if self.new_world_dim_surf_alpha <= self.new_world_dim_surf_max_alpha:
                    self.new_world_dim_surf.set_alpha(self.new_world_dim_surf_alpha)
                if self.new_world_dim_surf_alpha > self.new_world_dim_surf_max_alpha:
                    self.new_world_dim_surf_alpha = self.new_world_dim_surf_max_alpha
            if self.world_status[self.world_count - 1]:
                self.new_world_dim_surf_alpha -= 4 * fps_adjust
                if self.new_world_dim_surf_alpha >= 0:
                    self.new_world_dim_surf.set_alpha(self.new_world_dim_surf_alpha)
                if self.new_world_dim_surf_alpha < 0:
                    self.new_world_dim_surf_alpha = 0
        if self.new_world_dim_surf_alpha > 0:
            level_screen.blit(self.new_world_dim_surf, (0, 0))

        # lock icon
        if not self.world_status[self.world_count - 1]:
            img = self.lock_animation[0]
            level_screen.blit(img, (swidth / 2 - tile_size / 2 - object_wobble / 2, sheight / 2 - tile_size / 2))

        # new world unlock animation
        if self.new_world_animation_counter < 0:
            lock_frame = int(self.lock_animation_counter)
            animation_length = len(self.lock_animation)
            if lock_frame > animation_length - 1:
                lock_frame = animation_length - 1
            if lock_frame == 3 and not self.lock_sound_played:
                sounds['lock'] = True
                self.lock_sound_played = True
            anim_img = self.lock_animation[lock_frame]
            lock_vibration = [0, 0]
            if self.new_world_animation_stage3 > self.new_world_animation_counter > self.new_world_animation_stage2:
                lock_vibration = [random.choice([-2, 0, 2]), random.choice([-2, 0, 2])]
            if self.new_world_animation_counter < self.new_world_animation_stage3:
                level_screen.blit(anim_img,
                                  (swidth / 2 - tile_size / 2 + lock_vibration[0],
                                   sheight / 2 - tile_size / 2 + lock_vibration[1]))

        if joysticks:
            if self.joystick_counter == 1 or not self.world_status[self.world_count - 1]:
                joystick_over1 = True
            elif self.joystick_counter == -1:
                joystick_over_1 = True

        if not joysticks:
            if self.world_count > 1:
                left_press, over1 = self.left_btn.draw_button(level_screen, False, mouse_adjustment, local_events,
                                                              joystick_over2)
            else:
                level_screen.blit(self.left_button_grey, (self.left_x, self.button_y))
                if joystick_over2:
                    level_screen.blit(self.arrow_button_outline_surf, (self.left_x, self.button_y))
            if self.world_count < 4:
                right_press, over2 = self.right_btn.draw_button(level_screen, False, mouse_adjustment, local_events,
                                                                joystick_over_2)
            else:
                level_screen.blit(self.right_button_grey, (self.right_x, self.button_y))
                if joystick_over_2:
                    level_screen.blit(self.arrow_button_outline_surf, (self.right_x, self.button_y))
        else:
            bumper1 = self.lb_button
            bumper2 = self.rb_button
            if self.left_bumper_press:
                bumper1 = self.lb_button_press
            if self.right_bumper_press:
                bumper2 = self.rb_button_press
            level_screen.blit(bumper1, (self.left_x + 4, self.button_y + 2))
            level_screen.blit(bumper2, (self.right_x + 4, self.button_y + 2))

        menu_press, over3 = self.menu_btn.draw_button(level_screen, False, mouse_adjustment, local_events,
                                                      joystick_over1)
        if self.world_status[self.world_count - 1]:
            play_press, over4 = self.play_btn.draw_button(level_screen, False, mouse_adjustment, local_events,
                                                          joystick_over_1)

        if left_press or left_bumper_press:
            update_value = -1
            self.object_wobble_counter = self.text_wobble_default_value
        elif right_press or right_bumper_press:
            update_value = 1
            self.object_wobble_counter = self.text_wobble_default_value

        self.world_count += update_value
        if self.world_count < 1:
            self.world_count = 1
        if self.world_count > 4:
            self.world_count = 4

        if over1 or over2 or over3 or over4:
            sounds['button'] = True

        return play_press, menu_press, self.world_count, new_world_unlocked, sounds



