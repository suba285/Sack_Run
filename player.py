import pygame._sdl2
from level_transition import CircleTransition
from image_loader import img_loader
from font_manager import Text
from screen_info import swidth, sheight
import random
import math

pygame.init()
tile_size = 32
player_size_y = 32
player_size_x = 20

jump_offset_amount = 5

sack_level_positions = {
    '1_1': (200, 200),
    '2_1': (200, 200),
    '3_1': (200, 200)
}


# hey particles coming off the player ----------------------------------------------------------------------------------
class HeyParticle:
    def __init__(self, img1, img2, img3, sack_rect):
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.sack_rect = sack_rect
        self.x1 = sack_rect.x
        self.y1 = sack_rect.y
        self.x2 = sack_rect.x
        self.y2 = sack_rect.y
        self.x3 = sack_rect.x
        self.y3 = sack_rect.y
        self.part_counter1 = 0
        self.part_counter2 = 140
        self.part_counter3 = 250
        pass

    def update_particle(self, sack_rect, fps_adjust, new_level, camera_move_x, camera_move_y):
        # three particles being recycled to create an illusion of infinite particles

        # updating particles' positions
        self.part_counter1 += 1*fps_adjust
        self.part_counter2 += 1*fps_adjust
        self.part_counter3 += 1*fps_adjust
        self.x1 -= 1*fps_adjust - camera_move_x
        self.y1 += 0.2*fps_adjust + camera_move_y
        self.x2 -= 0.8 * fps_adjust - camera_move_x
        self.y2 += 0.3 * fps_adjust + camera_move_y
        self.x3 -= 1.1 * fps_adjust - camera_move_x
        self.y3 += 0.1 * fps_adjust + camera_move_y

        # updating individual particles
        if self.part_counter1 >= 360:
            self.x1 = sack_rect.x
            self.y1 = sack_rect.y
            self.part_counter1 = 0
        if self.part_counter2 >= 360:
            self.x2 = sack_rect.x
            self.y2 = sack_rect.y
            self.part_counter2 = 0
        if self.part_counter3 >= 360:
            self.x3 = sack_rect.x
            self.y3 = sack_rect.y
            self.part_counter3 = 0

        # new level reset
        if new_level:
            self.x1 = 0
            self.y1 = 0
            self.x2 = 0
            self.y2 = 0
            self.x3 = 0
            self.y3 = 0
            self.part_counter1 = 0
            self.part_counter2 = 140
            self.part_counter3 = 250

    def blit_particle(self, screen):
        screen.blit(self.img1, (self.x1, self.y1))
        screen.blit(self.img2, (self.x2, self.y2))
        screen.blit(self.img3, (self.x3, self.y3))


# player death animation (to be redone) --------------------------------------------------------------------------------
def death_animation_counter(self, fps_adjust):
    self.dead_counter += 1 * fps_adjust
    blit_sack = False
    if self.dead_counter > 24:
        blit_sack = False
    elif self.dead_counter > 18:
        blit_sack = True
    elif self.dead_counter > 12:
        blit_sack = False
    elif self.dead_counter > 6:
        blit_sack = True

    return blit_sack


# player animation used for teleportation and healing ------------------------------------------------------------------
def magic_animation(self, screen, counter, particle_x):
    blit = True
    img = self.particles1

    if counter > 90:
        img = self.particles2
    elif counter > 80:
        img = self.particles1
    elif counter > 70:
        img = self.particles2
    elif counter > 60:
        img = self.particles3
    elif counter > 50:
        img = self.particles4
    elif counter > 40:
        img = self.particles3
    elif counter > 30:
        img = self.particles1
    elif counter > 20:
        img = self.particles2
    elif counter > 10:
        img = self.particles3
    elif counter > 0:
        img = self.particles1
    else:
        blit = False

    if blit:
        screen.blit(img, (particle_x, self.sack_rect.y - 4))


# ======================================================================================================================

class Player:
    def __init__(self, screen, controls, settings_counters, world_count):
        text = Text()

        # player sprite assets -----------------------------------------------------------------------------------------
        self.sack = img_loader('data/images/sack_animations/sack.PNG', player_size_x, player_size_y)
        self.sack_idle1 = {
            1: img_loader('data/images/sack_animations/sack_idle1/sack1.PNG', player_size_x, player_size_y),
            2: img_loader('data/images/sack_animations/sack_idle1/sack2.PNG', player_size_x, player_size_y),
            3: img_loader('data/images/sack_animations/sack_idle1/sack3.PNG', player_size_x, player_size_y),
            4: img_loader('data/images/sack_animations/sack_idle1/sack4.PNG', player_size_x, player_size_y),
        }
        self.sack_idle2 = {
            1: img_loader('data/images/sack_animations/sack_idle2/sack1.PNG', player_size_x, player_size_y),
            2: img_loader('data/images/sack_animations/sack_idle2/sack2.PNG', player_size_x, player_size_y),
            3: img_loader('data/images/sack_animations/sack_idle2/sack3.PNG', player_size_x, player_size_y),
            4: img_loader('data/images/sack_animations/sack_idle2/sack2.PNG', player_size_x, player_size_y),
            5: img_loader('data/images/sack_animations/sack_idle2/sack1.PNG', player_size_x, player_size_y),
        }
        self.sack_walk = {
            1: img_loader('data/images/sack_animations/sack_walk/sack1.PNG', player_size_x, player_size_y),
            2: img_loader('data/images/sack_animations/sack_walk/sack2.PNG', player_size_x, player_size_y),
            3: img_loader('data/images/sack_animations/sack_walk/sack3.PNG', player_size_x, player_size_y),
            4: img_loader('data/images/sack_animations/sack_walk/sack4.PNG', player_size_x, player_size_y),
            5: img_loader('data/images/sack_animations/sack_walk/sack5.PNG', player_size_x, player_size_y),
            6: img_loader('data/images/sack_animations/sack_walk/sack6.PNG', player_size_x, player_size_y),
            7: img_loader('data/images/sack_animations/sack_walk/sack7.PNG', player_size_x, player_size_y),
            8: img_loader('data/images/sack_animations/sack_walk/sack8.PNG', player_size_x, player_size_y),
        }
        self.sack_jump = {
            1: img_loader('data/images/sack_animations/sack_jump/sack1.PNG', player_size_x, player_size_y),
            2: img_loader('data/images/sack_animations/sack_jump/sack2.PNG', player_size_x, player_size_y),
            3: img_loader('data/images/sack_animations/sack_jump/sack3.PNG', player_size_x, player_size_y),
            4: img_loader('data/images/sack_animations/sack_jump/sack4.PNG', player_size_x, player_size_y),
            5: img_loader('data/images/sack_animations/sack_jump/sack5.PNG', player_size_x, player_size_y),
            6: img_loader('data/images/sack_animations/sack_jump/sack6.PNG', player_size_x, player_size_y),
        }
        self.sack_speed_dash = {
            1: img_loader('data/images/sack_animations/sack_speed_dash/sack1.PNG', player_size_x, 22),
            2: img_loader('data/images/sack_animations/sack_speed_dash/sack2.PNG', player_size_x, 22),
            3: img_loader('data/images/sack_animations/sack_speed_dash/sack3.PNG', player_size_x, 22),
            4: img_loader('data/images/sack_animations/sack_speed_dash/sack4.PNG', player_size_x, 22)
        }
        self.sack_speed_dash_transition = {
            1: img_loader('data/images/sack_animations/sack_speed_dash_transition/sack1.PNG',
                          player_size_x, player_size_y),
            2: img_loader('data/images/sack_animations/sack_speed_dash_transition/sack2.PNG',
                          player_size_x, player_size_y),
            3: img_loader('data/images/sack_animations/sack_speed_dash_transition/sack3.PNG',
                          player_size_x, player_size_y),
            4: img_loader('data/images/sack_animations/sack_speed_dash_transition/sack4.PNG',
                          player_size_x, player_size_y),
        }

        self.sack_img = self.sack
        self.sack_rect = pygame.Rect(0, 0, 18, 28)
        self.sack_rect.x = swidth / 2 - self.sack_rect.width / 2
        self.sack_rect.y = sheight / 2 - self.sack_rect.height / 2

        self.player_speed = 2
        self.slide = 0.4
        self.default_on_ground_counter = 6
        self.on_ground_counter = self.default_on_ground_counter
        self.sack_width = self.sack_rect.width
        self.sack_height = self.sack_rect.height
        self.vel_y = 0
        self.vel_x_l = 0
        self.vel_x_r = 0
        self.vel_x = 0
        self.jumped = False
        self.jump_adder = 0
        self.sack_offset = 0
        self.squash_counter_x = 10
        self.squash_counter_y = 10

        self.sack_silhouette = pygame.mask.Mask.to_surface(pygame.mask.from_surface(self.sack),
                                                           setcolor=(255, 255, 255), unsetcolor=(0, 0, 0)).convert()
        self.sack_silhouette.set_colorkey((0, 0, 0))

        self.controls = controls
        self.settings_counters = settings_counters
        self.world_count = world_count

        # teleportation particles frames -------------------------------------------------------------------------------
        self.particles1 = img_loader('data/images/particles1.PNG', tile_size, tile_size)
        self.particles2 = img_loader('data/images/particles2.PNG', tile_size, tile_size)
        self.particles3 = img_loader('data/images/particles3.PNG', tile_size, tile_size)
        self.particles4 = img_loader('data/images/particles4.PNG', tile_size, tile_size)

        # bridge
        self.bridge_section = img_loader('data/images/bridge_section.PNG', tile_size, 7)

        # respawn instruction images and variables ---------------------------------------------------------------------
        self.respawn_text = []
        self.respawn_text.append([text.make_text(['R']), 0])
        self.respawn_text.append([text.make_text(['E']), -2])
        self.respawn_text.append([text.make_text(['S']), -4])
        self.respawn_text.append([text.make_text(['P']), -6])
        self.respawn_text.append([text.make_text(['A']), -8])
        self.respawn_text.append([text.make_text(['W']), -10])
        self.respawn_text.append([text.make_text(['N']), -12])

        self.a_button = img_loader('data/images/buttons/button_a.PNG', tile_size / 2, tile_size / 2)
        self.cross_button = img_loader('data/images/buttons/button_cross.PNG', tile_size / 2, tile_size / 2)
        self.respawn_keys = {
            '1': img_loader('data/images/buttons/key_space.PNG', tile_size, tile_size / 2),
            '1_press': img_loader('data/images/buttons/key_space_press.PNG', tile_size, tile_size / 2),
            '2': img_loader('data/images/buttons/key_w.PNG', tile_size / 2, tile_size / 2),
            '2_press': img_loader('data/images/buttons/key_w_press.PNG', tile_size / 2, tile_size / 2),
            '3': img_loader('data/images/buttons/key_up.PNG', tile_size / 2, tile_size / 2),
            '3_press': img_loader('data/images/buttons/key_up_press.PNG', tile_size / 2, tile_size / 2),
        }

        self.respawn_press_counter = 0

        self.restart_level = False
        self.restart_trigger = False
        self.restart_counter = 0
        self.single_restart = True

        # extra card powers and their counters -------------------------------------------------------------------------
        self.mid_air_jump = False
        self.mid_air_jump_counter = 0
        self.mid_air_jumps_num = 3
        self.speed_dash = False
        self.speed_dash_activated = False
        self.speed_dash_landed = True
        self.speed_dash_direction = 1
        self.speed_dash_speed = 5

        # animation variables ------------------------------------------------------------------------------------------
        self.animation_counter = 0
        self.walk_counter = 1
        self.idle_counter = 1
        self.speed_dash_counter = 1
        self.idle_animation = 1
        self.idle_animation_lengths = {
            1: 4,
            2: 5
        }
        self.walk_animation_speed = 3.1
        self.idle_animation_speed = 7
        self.speed_dash_animation_speed = 7

        # other player variables ---------------------------------------------------------------------------------------
        self.direction = 1
        self.animate_walk = True
        self.walking = False
        self.new_level = False
        self.new_level_cooldown = 70
        self.teleport_count = 0
        self.health = 2
        self.harmed = False
        self.dead = False
        self.transition = False
        self.dead_counter = 0
        self.airborn = True
        self.lowest_tile = 0
        self.highest_tile = 264
        self.speed = 0
        self.speed_adder = 0
        self.player_moved = False
        self.blit_plr = True
        self.harm_counter = 40
        self.harm_flash_counter = 0
        self.init_flash = False
        self.lowering_cooldown = 15
        self.surface_type = 'grass'

        self.screen_shake_counter = 0

        self.bridge_cutscene_walk = False

        self.speed_dash_sine_counter = 0
        self.speed_dash_sine_offset_counter = 9
        self.speed_dash_animation_surface = pygame.Surface((40, 40)).convert()
        self.speed_dash_animation_surface.set_colorkey((0, 0, 0))
        self.speed_dash_animation_surface.fill((0, 0, 0))

        # music and sounds ---------------------------------------------------------------------------------------------
        self.first_level_play_music = True
        self.play_music = False
        self.fadeout = False
        self.single_fadeout = True

        # collisions ---------------------------------------------------------------------------------------------------
        self.top_col = False
        self.btm_col = False
        self.right_col = False
        self.left_col = False
        self.col_types = {'left': False, 'right': False, 'top': False, 'bottom': False}
        self.first_collision = False

        # --------------------------------------------------------------------------------------------------------------
        self.camera_movement_x = 0
        self.camera_movement_y = 0
        self.camera_movement_amount = 0
        self.camera_falling_assist = False

        # --------------------------------------------------------------------------------------------------------------
        self.joystick_left = False
        self.joystick_right = False
        self.player_jump = False

        # --------------------------------------------------------------------------------------------------------------
        self.power_indicator_list = []

        # power particle variables -------------------------------------------------------------------------------------
        self.power_particle_surface = pygame.Surface((swidth, sheight)).convert()
        self.power_particle_surface.set_alpha(170)
        self.power_particle_list = []
        self.power_particle_counter = 0
        self.particle_colour = (255, 255, 255)

        # map borders --------------------------------------------------------------------------------------------------
        self.right_border = 0
        self.left_border = 0

        # player movement per frame ------------------------------------------------------------------------------------
        self.dx = 0
        self.dy = 0

        # mouse animation ----------------------------------------------------------------------------------------------
        self.mouse0 = img_loader('data/images/mouse0.PNG', tile_size / 2, tile_size)
        self.mouse1 = img_loader('data/images/mouse1.PNG', tile_size / 2, tile_size)
        self.mouse2 = img_loader('data/images/mouse2.PNG', tile_size / 2, tile_size)
        self.mouse3 = img_loader('data/images/mouse3.PNG', tile_size / 2, tile_size)

        self.inst_button_counter = 0
        self.inst_mouse_counter = 0

        # hey particle images ------------------------------------------------------------------------------------------
        self.hey_part1 = img_loader('data/images/hey_particle1.PNG', tile_size / 2.5, tile_size / 2.5)
        self.hey_part2 = img_loader('data/images/hey_particle2.PNG', tile_size / 2.5, tile_size / 2.5)
        self.hey_part3 = img_loader('data/images/hey_particle3.PNG', tile_size / 2.5, tile_size / 2.5)

        # healing animation list ---------------------------------------------------------------------------------------
        self.anim_list = []
        # 1 - speed
        # 2 - x position
        # 3 - y position

        # class initiations --------------------------------------------------------------------------------------------
        self.circle_transition = CircleTransition(screen)

    def update_pos_animation(self, screen, tile_list, next_level_list, level_count, harm_in, fps_adjust,
                             mid_air_jump_trigger, speed_dash_trigger,
                             left_border, right_border,
                             move, shockwave_mush_list, events, gem_equipped, joysticks, restart_level_procedure):

        dx = 0
        dy = 0

        sounds = {
            'step_grass': False,
            'step_wood': False,
            'step_rock': False,
            'jump': False,
            'mid_air_jump': False,
            'mushroom': False,
            'land': False,
            'death': False,
        }

        self.animation_counter += 1 * fps_adjust

        self.screen_shake_counter -= 1 * fps_adjust

        self.squash_counter_y += 0.5 * fps_adjust

        if self.airborn:
            self.slide = 0.2
        else:
            self.slide = 0.4

        if self.vel_x_l < 0:
            self.vel_x_l += self.slide * fps_adjust
        else:
            self.vel_x_l = 0

        if self.vel_x_r > 0:
            self.vel_x_r -= self.slide * fps_adjust
        else:
            self.vel_x_r = 0

        self.restart_level = False

        key = pygame.key.get_pressed()

        # borders
        self.left_border = left_border
        self.right_border = right_border
        top_border = 50 / 270 * sheight

        harm = False

        if self.world_count == 1 and level_count == 1 and self.lowering_cooldown == 15:
            self.screen_shake_counter = 10

        if self.screen_shake_counter > 0:
            screen_shake = True
        else:
            screen_shake = False

        # music
        self.play_music = False
        self.fadeout = False

        if self.first_level_play_music:
            self.play_music = True
            self.first_level_play_music = False

        # setting all collisions to false
        self.top_col = False
        self.btm_col = False
        self.right_col = False
        self.left_col = False

        # new level cooldown, so the player can't move immediately after progressing to a new level
        self.new_level_cooldown += 1*fps_adjust

        # turning the 'harm' boolean into a single variable
        if harm_in and self.teleport_count <= 10:
            harm = True

        # joystick input management
        if events['keydown']:
            if events['keydown'].key == self.controls['jump']:
                self.player_jump = True
        if events['keyup']:
            if events['keyup'].key == self.controls['jump']:
                self.player_jump = False
        if events['joybuttondown']:
            if events['joybuttondown'].button == 0:
                self.player_jump = True
        if events['joybuttonup']:
            if events['joybuttonup'].button == 0:
                self.player_jump = False
        if events['joyaxismotion_x']:
            event = events['joyaxismotion_x']
            if event.value > 0.4:
                self.joystick_right = True
            else:
                self.joystick_right = False
            if event.value < -0.4:
                self.joystick_left = True
            else:
                self.joystick_left = False
        if events['joydeviceremoved']:
            self.joystick_left = False
            self.joystick_right = False
            self.player_jump = False

        # D-pad input
        if joysticks:
            hat_value = joysticks[0].get_hat(0)
        else:
            hat_value = (0, 0)

        # special power cards effects ----------------------------------------------------------------------------------
        if mid_air_jump_trigger and not self.mid_air_jump:
            self.mid_air_jump = True
            self.power_indicator_list.append('jump_boost')
            self.mid_air_jump_counter = 0
        if speed_dash_trigger and not self.speed_dash:
            self.speed_dash = True
            self.speed_dash_sine_counter = 0
            self.speed_dash_sine_offset_counter = 9

        # updating special power cards counters ------------------------------------------------------------------------
        append = self.power_particle_list.append
        if self.mid_air_jump:
            if self.mid_air_jump_counter == 0:
                self.particle_colour = (57, 182, 86)
            elif self.mid_air_jump_counter == 1:
                self.particle_colour = (100, 215, 96)
            else:
                self.particle_colour = (200, 226, 151)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            append([random.randrange(x_value, x_value + self.sack_width),
                   random.randrange(y_value, y_value + self.sack_height),
                   random.randrange(6, 14),
                   self.particle_colour])
            if gem_equipped:
                self.mid_air_jump_counter = 0
                gem_equipped = False
        if self.speed_dash:
            self.particle_colour = (70, 161, 193)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            append([random.randrange(x_value, x_value + self.sack_width),
                   random.randrange(y_value, y_value + self.sack_height),
                   random.randrange(6, 14),
                   self.particle_colour])

        # special power cards duration counters ------------------------------------------------------------------------
        if self.mid_air_jump_counter >= self.mid_air_jumps_num:
            self.mid_air_jump_counter = 0
            self.power_indicator_list.remove('jump_boost')
            self.mid_air_jump = False

        # subtracting health if player is being harmed
        if not self.harmed and harm and self.player_moved:
            self.health = 0
            sack_mask = pygame.mask.from_surface(self.sack_img)
            self.sack_silhouette = pygame.mask.Mask.to_surface(sack_mask, setcolor=(255, 255, 255),
                                                               unsetcolor=(0, 0, 0))
            self.sack_silhouette.set_colorkey((0, 0, 0))
            self.dead = True
            sounds['death'] = True
            self.harmed = True
            self.speed_dash = False
            self.speed_dash_activated = False
            gem_equipped = False
            self.mid_air_jump = False
            self.screen_shake_counter = 10
            self.vel_x_r = 0
            self.vel_x_l = 0
            self.vel_y = 0

        if not self.player_moved:
            self.health = 2

        if not harm:
            self.harmed = False

        # next level portal collisions ---------------------------------------------------------------------------------
        for tile in next_level_list:
            if tile[1].colliderect(self.sack_rect.x, self.sack_rect.y,
                                   self.sack_width, self.sack_height) and not self.dead:
                self.teleport_count += 1*fps_adjust
                if self.teleport_count >= 20:
                    if not self.transition:
                        self.circle_transition = CircleTransition(screen)
                    self.transition = True
                    # music loading
                    if self.world_count == 1 and level_count == 2:
                        self.fadeout = True
                    if self.world_count == 2:
                        if level_count == 8:
                            self.fadeout = True

                if self.teleport_count >= 50:
                    if self.mid_air_jump:
                        self.mid_air_jump_counter = 4
                    level_count += 1
                    self.new_level = True
                    self.new_level_cooldown = 0
                    self.teleport_count = 0
                    self.player_moved = False
                    self.first_collision = False
                    self.speed_dash = False
                    self.speed_dash_activated = False
                    # player direction
                    self.direction = 1
            else:
                self.teleport_count = 0

        # movement and animation ---------------------------------------------------------------------------------------
        if self.new_level_cooldown >= 30 and not self.dead and self.teleport_count < 20\
                and not (self.col_types['right'] or self.col_types['left']) and move:
            # player control
            self.transition = False
            if self.player_jump and not self.jumped:
                self.teleport_count = 0
                if self.speed_dash_activated:
                    self.speed_dash_activated = False
                    if not gem_equipped:
                        self.speed_dash = False
                    self.vel_y = -7.5
                self.player_moved = True
                if not self.jumped and \
                        ((self.on_ground_counter > 0 and not self.airborn) or (self.dy > 5 and self.mid_air_jump)):
                    if self.mid_air_jump and not (self.on_ground_counter > 0 and not self.airborn):
                        self.mid_air_jump_counter += 1
                        self.screen_shake_counter = 10
                        sounds['mid_air_jump'] = True
                    if self.mid_air_jump:
                        self.vel_y = -11
                    else:
                        self.vel_y = -7.5
                    sounds['jump'] = True
                    self.jump_adder = 0
                    self.jumped = True
                    self.animate_walk = False
                    self.airborn = True
            if not self.mid_air_jump:
                if self.player_jump and self.jumped and self.jump_adder < 1.5:
                    self.jump_adder += 0.16 * fps_adjust
                    self.vel_y -= 0.35 * fps_adjust
                if self.jump_adder >= 1.5:
                    self.player_jump = False

            if not self.player_jump:
                self.jumped = False

            walking_left = False
            walking_right = False

            if not self.speed_dash_activated:
                if self.sack_rect.height != 28:
                    self.sack_rect.height = 28
                # walking left
                if key[self.controls['left']] or self.joystick_left or hat_value[0] == -1:
                    self.player_moved = True
                    if self.speed_dash and not self.speed_dash_activated:
                        self.speed_dash_activated = True
                        gem_equipped = False
                        self.screen_shake_counter = 10
                        self.vel_y = 0
                        self.sack_offset = 0
                        self.speed_dash_direction = -1
                    walking_left = True
                    self.speed_adder += 0.1 * fps_adjust
                    self.speed += self.speed_adder
                    if self.speed > self.player_speed:
                        self.speed = self.player_speed
                    dx -= self.speed
                    self.vel_x_l = dx
                    self.vel_x_r = 0
                    self.direction = -1
                    self.teleport_count = 0

                # walking right
                if key[self.controls['right']] or self.joystick_right or hat_value[0] == 1 or self.bridge_cutscene_walk:
                    self.player_moved = True
                    if self.speed_dash and not self.speed_dash_activated:
                        self.speed_dash_activated = True
                        gem_equipped = False
                        self.screen_shake_counter = 10
                        self.vel_y = 0
                        self.sack_offset = 0
                        self.speed_dash_direction = 1
                    walking_right = True
                    self.speed_adder += 0.1 * fps_adjust
                    self.speed += self.speed_adder
                    if self.speed > self.player_speed:
                        self.speed = self.player_speed
                    dx += self.speed
                    self.vel_x_r = dx
                    self.vel_x_l = 0
                    self.teleport_count = 0
                    self.direction = 1

                if not walking_right and not walking_left:
                    self.speed = 0
                    self.speed_adder = 0

                if walking_right and walking_left:
                    self.speed = 0
                    self.speed_adder = 0
                    self.walk_counter = 0

                if walking_left or walking_right:
                    self.walking = True
                else:
                    self.walking = False

                # sack walking animation
                if (walking_right or walking_left) and self.animate_walk and not self.airborn and self.vel_x != 0:
                    if self.animation_counter > self.walk_animation_speed:
                        self.walk_counter += 1
                        if self.walk_counter in [4, 8]:
                            sounds[f'step_{self.surface_type}'] = True
                        self.animation_counter = 0
                    if self.walk_counter > len(self.sack_walk):
                        self.walk_counter = 1
                    if self.walk_counter == 0:
                        self.sack_img = self.sack
                    else:
                        self.sack_img = self.sack_walk[self.walk_counter]
                    if self.direction == -1:
                        self.sack_img = pygame.transform.flip(self.sack_img, True, False)

            elif self.speed_dash_activated:
                self.sack_rect.height = 20
                self.sack_offset = 0
                self.speed_dash_landed = False
                if self.speed_dash_direction == -1:
                    if self.vel_x_l > -self.speed_dash_speed:
                        self.vel_x_l -= 1 * fps_adjust
                    else:
                        self.vel_x_l = self.speed_dash_speed * self.speed_dash_direction
                    self.direction = -1
                elif self.speed_dash_direction == 1:
                    self.direction = 1
                    if self.vel_x_r < self.speed_dash_speed:
                        self.vel_x_r += 1 * fps_adjust
                    else:
                        self.vel_x_r = self.speed_dash_speed * self.speed_dash_direction

        # jumping and idle animations
        if self.airborn and not self.speed_dash_activated:
            self.sack_offset = 0
            if self.vel_y < -9:
                self.sack_img = self.sack_jump[1]
            elif self.vel_y < -6.5:
                self.sack_img = self.sack_jump[2]
            elif self.vel_y < -5:
                self.sack_img = self.sack_jump[3]
            elif -5 < self.vel_y < 3:
                self.sack_img = self.sack_jump[4]
            elif self.vel_y < 5:
                self.sack_img = self.sack_jump[5]
            else:
                self.sack_img = self.sack_jump[6]
            if self.direction == -1:
                self.sack_img = pygame.transform.flip(self.sack_img, True, False)
        if not self.airborn and not self.walking:
            # idle animation
            self.sack_offset = 0
            if self.animation_counter > self.idle_animation_speed:
                self.idle_counter += 1
                self.animation_counter = 0
            if self.idle_counter <= self.idle_animation_lengths[self.idle_animation]:
                if self.idle_animation == 1:
                    self.sack_img = self.sack_idle1[self.idle_counter]
                else:
                    self.sack_img = self.sack_idle2[self.idle_counter]
            else:
                self.sack_img = self.sack
            if self.idle_counter > 15:
                self.idle_animation = random.randint(1, 2)
                self.idle_counter = 1
            if self.direction == -1:
                self.sack_img = pygame.transform.flip(self.sack_img, True, False)

        # respawn at the beginning of the level and transition
        if (self.player_jump and self.dead and self.dead_counter >= 36 and not self.restart_trigger)\
                or restart_level_procedure:
            self.restart_trigger = True
            self.single_fadeout = True
            self.teleport_count = 0
            self.circle_transition = CircleTransition(screen)
            self.init_flash = False
            self.mid_air_jump = False
            self.speed_dash = False
            self.speed_dash_activated = False

            counter = 0
            for letter in self.respawn_text:
                letter[1] = counter
                counter -= 2

        if self.restart_trigger:
            self.restart_counter += 1 * fps_adjust

        if self.restart_counter > 20:
            self.transition = True

        if self.restart_counter > 50 and self.single_restart:
            self.restart_level = True
            self.player_moved = False
            self.first_collision = False
            self.play_music = True
            self.single_restart = False

        if self.restart_counter > 80:
            self.restart_trigger = False
            self.restart_counter = 0
            self.single_restart = True

        self.col_types = {'left': False, 'right': False, 'top': False, 'bottom': False}

        # gravity ------------------------------------------------------------------------------------------------------
        if not self.speed_dash_activated:
            if self.dead:
                self.vel_y = dy
            else:
                if not move and self.world_count == 1 and level_count == 1:
                    self.lowering_cooldown -= 1 * fps_adjust
                    if self.lowering_cooldown <= 0:
                        grav_speed = 0.3
                    else:
                        grav_speed = 0
                else:
                    grav_speed = 0.65
                self.vel_y += grav_speed * fps_adjust
                if self.vel_y > 8:
                    self.vel_y = 8
            dy = self.vel_y*fps_adjust
        if dy > 3:
            self.airborn = True

        # collision detection and position -----------------------------------------------------------------------------
        self.vel_x = self.vel_x_l + self.vel_x_r
        temp_rect = self.sack_rect
        temp_rect.x += (self.vel_x + 0.5)

        bridge_cutscene_trigger = False

        if self.sack_rect.x + 20 > self.right_border:
            if self.vel_x > 0:
                self.vel_x_r = 0
                self.vel_x = 0
                self.sack_rect.x = self.right_border - 20
                self.col_types['right'] = True
        if self.sack_rect.x < self.left_border:
            if self.vel_x < 0:
                self.vel_x_l = 0
                self.vel_x = 0
                self.sack_rect.x = self.left_border
                self.col_types['left'] = True

        col_counter = 0
        col_y_tile_list = []
        append = col_y_tile_list.append
        for tile in tile_list:
            if tile[1].colliderect(temp_rect.x + self.vel_x, temp_rect.y, self.sack_width, self.sack_height):
                if tile[0] == self.bridge_section:
                    bridge_cutscene_trigger = True
                if self.vel_x > 0:
                    self.sack_rect.right = tile[1].left
                    self.vel_x = 0
                    self.vel_x_r = 0
                    self.col_types['right'] = True
                if self.vel_x < 0:
                    self.sack_rect.left = tile[1].right
                    self.vel_x = 0
                    self.vel_x_l = 0
                    self.col_types['left'] = True
            if tile[1][0] + tile_size > self.sack_rect.x > tile[1][0] - tile_size:
                append(tile)
            col_counter += 1

        if (self.col_types['left'] or self.col_types['right']) and self.speed_dash_activated:
            self.speed_dash_activated = False
            if not gem_equipped:
                self.speed_dash = False
            self.vel_y = -10

        col_counter = 0
        for tile in col_y_tile_list:
            if tile[1].colliderect(self.sack_rect.x, self.sack_rect.y + dy, self.sack_width, self.sack_height):
                if tile[0] == self.bridge_section:
                    self.bridge_cutscene_walk = True
                    if tile[-1] == 'none':
                        self.bridge_cutscene_walk = False
                        bridge_cutscene_trigger = True
                if dy > 0:
                    self.sack_rect.bottom = tile[1].top
                    self.surface_type = tile[2]
                    if (self.airborn or dy > 10) and self.player_moved and self.squash_counter_y > 4:
                        self.squash_counter_y = -3
                        sounds[f'step_{self.surface_type}'] = True
                        sounds['land'] = True
                        self.walk_counter = 0
                    dy = 0
                    self.vel_y = 0
                    self.col_types['bottom'] = True
                    self.airborn = False
                    self.camera_falling_assist = False
                    self.first_collision = True
                    self.on_ground_counter = self.default_on_ground_counter
                    self.animate_walk = True
                    self.speed_dash_landed = True
                if dy < 0:
                    self.sack_rect.top = tile[1].bottom
                    dy = 0
                    self.vel_y = 0
                    self.col_types['top'] = True
            col_counter += 1

        self.on_ground_counter -= 1

        # mushroom collisions
        for mushroom in shockwave_mush_list:
            y_movement = dy / 2
            if mushroom[1].colliderect(self.sack_rect.x + 7,
                                       self.sack_rect.y + y_movement, 6, self.sack_height)\
                    and not self.dead and dy > 1 and self.sack_rect.y < mushroom[1][1] and mushroom[3] == 0:
                mushroom[2] = 12
                mushroom[3] = 60
                dy = 0
                self.vel_y = -7.5
                sounds['mushroom'] = True

        # next level position
        if self.new_level:
            self.sack_rect.y = sheight / 2 - self.sack_width / 2
            self.direction = 1
            self.new_level = False

        # ensuring the player sprite is always in the middle level of the screen
        self.sack_rect.x = swidth / 2 - self.sack_width / 2
        if not self.first_collision:
            self.sack_rect.y = sheight / 2 - self.sack_width / 2

        # preventing the player from falling out of the world
        if self.sack_rect.bottom > sheight:
            self.sack_rect.bottom = sheight
            dy = 0
        if self.sack_rect.top + dy < 0:
            self.sack_rect.top = 0
            dy = 0

        # updating player coordinates ----------------------------------------------------------------------------------
        self.camera_movement_x = round(-self.vel_x * fps_adjust)
        dx = 0
        if self.sack_rect.y > (180 / 270 * sheight) and dy * fps_adjust > 0:
            self.camera_falling_assist = True
        if self.sack_rect.y < sheight / 2:
            self.camera_falling_assist = False
        if self.camera_falling_assist:
            self.camera_movement_y = round(-(dy + 1 / 10 * dy))
            self.sack_rect.y -= dy / 10
        elif self.sack_rect.y < top_border and dy * fps_adjust < 0:
            self.camera_movement_y = round(-dy)
        elif not self.first_collision:
            self.camera_movement_y = round(-dy)
        else:
            self.camera_movement_y = round(-dy / 2)
            self.sack_rect.y += round(dy / 2)

        self.dx = dx
        self.dy = dy

        # resetting player health --------------------------------------------------------------------------------------
        if self.restart_level:
            self.dead = False
            self.health = 2
            self.dead_counter = 0

        # returns ------------------------------------------------------------------------------------------------------
        return level_count, self.sack_rect, self.direction, self.health,\
               self.camera_movement_x, self.camera_movement_y,\
               self.fadeout, self.restart_level, self.player_moved, self.new_level_cooldown, shockwave_mush_list,\
               gem_equipped, screen_shake, sounds, bridge_cutscene_trigger

# BLITTING PLAYER SPRITE ONTO THE SCREEN ===============================================================================
    def blit_player(self, screen, draw_hitbox, fps_adjust):
        particle_x = self.sack_rect.x - 7
        self.init_flash = False

        # player flickering when taking damage (not in use because it doesn't look that good)
        if self.init_flash and self.health > 0:
            self.harm_counter -= 1
            self.harm_flash_counter += 1
            if self.harm_flash_counter >= 6:
                self.blit_plr = not self.blit_plr
                self.harm_flash_counter = 0
            if self.harm_counter <= 0:
                self.init_flash = False
                self.harm_counter = 60
                self.harm_flash_counter = 0
        else:
            self.blit_plr = True

        # power particles
        self.power_particle_surface.fill((0, 0, 0))

        for particle in self.power_particle_list:
            particle[2] -= 0.3
            particle[0] += self.camera_movement_x
            particle[1] += self.camera_movement_y
            pygame.draw.circle(self.power_particle_surface, particle[3], (particle[0], particle[1]), particle[2])

        self.power_particle_surface.set_colorkey((0, 0, 0))
        screen.blit(self.power_particle_surface, (0, 0))

        # landing squash
        if -3 <= self.squash_counter_y <= 3:
            width = self.sack.get_width()
            height = self.sack.get_height()
            self.sack_img = pygame.transform.scale(self.sack_img,
                                                   (width,
                                                    height - (3 - abs(round(self.squash_counter_y)))))
            squash_offset = 3 - abs(self.squash_counter_y)
        else:
            squash_offset = 0

        # speed dash visual effects
        if self.speed_dash_activated:
            sack_speed_dash_img = self.sack_speed_dash_transition[1]
            if self.speed_dash_sine_counter > 10:
                if self.animation_counter > self.speed_dash_animation_speed:
                    self.speed_dash_counter += 1
                    self.animation_counter = 0
                if self.speed_dash_counter > len(self.sack_speed_dash):
                    self.speed_dash_counter = 1
                sack_speed_dash_img = self.sack_speed_dash[self.speed_dash_counter]
            elif self.speed_dash_sine_counter > 7:
                sack_speed_dash_img = self.sack_speed_dash_transition[4]
            elif self.speed_dash_sine_counter > 5:
                sack_speed_dash_img = self.sack_speed_dash_transition[3]
            elif self.speed_dash_sine_counter > 2:
                sack_speed_dash_img = self.sack_speed_dash_transition[2]
            if self.direction == -1:
                sack_speed_dash_img = pygame.transform.flip(sack_speed_dash_img, True, False)

            self.speed_dash_sine_counter += 1 * fps_adjust
            self.speed_dash_animation_surface.fill((0, 0, 0))

            radius = 9
            offset = 5
            x = self.speed_dash_animation_surface.get_width()

            if self.speed_dash_sine_counter > 8:
                self.speed_dash_sine_offset_counter -= 0.7
                if self.speed_dash_sine_offset_counter < 0:
                    self.speed_dash_sine_offset_counter = 0

            for i in range(3):
                y = -math.sin((1/4) * (self.speed_dash_sine_counter + offset)) * (offset/5)
                x -= 5 - self.speed_dash_sine_offset_counter
                pygame.draw.circle(self.speed_dash_animation_surface, (234, 212, 170), (x, y + 10), radius, 0)
                offset += 5
                radius -= 2

            speed_dash_animation_mask = pygame.mask.from_surface(self.speed_dash_animation_surface)
            outline = speed_dash_animation_mask.outline()

            for pixel in outline:
                self.speed_dash_animation_surface.set_at((pixel[0], pixel[1]), (232, 183, 150))

            if self.speed_dash_direction == 1:
                screen.blit(self.speed_dash_animation_surface,
                            (self.sack_rect.x - self.speed_dash_animation_surface.get_width() + 10 - self.sack_offset,
                             self.sack_rect.y - 1))

            elif self.speed_dash_direction == -1:
                screen.blit(pygame.transform.flip(self.speed_dash_animation_surface, True, False),
                            (self.sack_rect.x + 10 - self.sack_offset,
                             self.sack_rect.y - 1))

            self.sack_img = sack_speed_dash_img

        if self.dead:
            self.blit_plr = death_animation_counter(self, fps_adjust)
            self.sack_img = self.sack_silhouette

        # drawing player onto the screen
        if self.blit_plr:
            screen.blit(self.sack_img, (self.sack_rect.x - 1 - self.sack_offset, self.sack_rect.y - 4 + squash_offset))

        if draw_hitbox and not self.dead:
            pygame.draw.rect(screen, (255, 255, 255), self.sack_rect, 1)

        # drawing teleportation particles onto the screen
        if not self.dead and self.teleport_count > 0:
            magic_animation(self, screen, self.teleport_count, particle_x)

# inter-level transition -----------------------------------------------------------------------------------------------
    def draw_transition(self, fps_adjust):
        if self.transition:
            self.circle_transition.draw_circle_transition(self.sack_rect, fps_adjust)

# respawn instructions -------------------------------------------------------------------------------------------------
    def blit_respawn_instructions(self, screen, fps_adjust, joystick_connected, settings_counters):
        if self.health == 0 and self.dead_counter >= 36 and self.restart_counter == 0:
            x = swidth / 2 - 3 * 8
            press = False
            self.respawn_press_counter += 1 * fps_adjust

            if self.controls['configuration'][4] == 1:
                controller_btn = self.a_button
            else:
                controller_btn = self.cross_button

            for letter in self.respawn_text:
                x += 6
                y_letter_offset = 0
                img = letter[0]
                if 10 > letter[1] > 0:
                    y_letter_offset = -abs(5 - abs(-5 + (letter[1])))
                if 100 > letter[1] > 90:
                    y_letter_offset = -abs(5 - abs(-5 + (letter[1] - 90)))
                if letter[1] >= 100:
                    letter[1] = 10
                if letter[1] > 0:
                    screen.blit(img, (x - img.get_width() / 2, sheight / 3 + y_letter_offset))
                letter[1] += 1 * fps_adjust

            if self.respawn_press_counter > 65:
                press = True
                if self.respawn_press_counter > 80:
                    self.respawn_press_counter = 10
            if joystick_connected:
                screen.blit(controller_btn, (swidth / 2 - tile_size / 4, sheight / 3 + 16))
            else:
                key_img = self.respawn_keys[str(settings_counters['jumping'])]
                if press:
                    key_img = self.respawn_keys[f'{settings_counters["jumping"]}_press']
                if self.respawn_press_counter > 8:
                    screen.blit(key_img, (swidth / 2 - key_img.get_width() / 2, sheight / 3 + 16))
