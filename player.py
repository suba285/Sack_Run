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
        self.sack_rect = pygame.Rect(0, 0, 18, 23)
        self.sack_rect.x = swidth / 2 - self.sack_rect.width / 2
        self.sack_rect.y = sheight / 2 - self.sack_rect.height / 2

        self.player_speed = 2
        self.slide = 0.4
        self.default_on_ground_counter = 7
        self.on_ground_counter = self.default_on_ground_counter
        self.max_jump_press_counter = 7
        self.jump_press_counter = 0
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
        self.freeze = False
        self.freeze_type = ''
        self.block_control = False

        self.sack_silhouette = pygame.mask.Mask.to_surface(pygame.mask.from_surface(self.sack),
                                                           setcolor=(255, 255, 255), unsetcolor=(0, 0, 0)).convert()
        self.sack_silhouette.set_colorkey((0, 0, 0))

        self.controls = controls
        self.settings_counters = settings_counters
        self.world_count = world_count

        self.hat_value = [0, 0]

        # PARTICLE ANIMATIONS ------------------------------------------------------------------------------------------
        self.walking_particles_left = []
        self.walking_particles_right = []
        for frame in range(9):
            img = img_loader(f'data/images/particle_animation/walking_particles/walking_particles{frame + 1}.PNG',
                             16, 16)
            self.walking_particles_right.append(img)
            img = pygame.transform.flip(img, True, False)
            self.walking_particles_left.append(img)
        self.jumping_particles_right = []
        self.jumping_particles_left = []
        self.jumping_particles_up = []
        for frame in range(8):
            img = img_loader(f'data/images/particle_animation/jumping_particles/jumping_particles{frame + 1}.PNG',
                             16, 28)
            self.jumping_particles_up.append(img)
            img_l = pygame.transform.rotate(img, 30)
            img_r = pygame.transform.rotate(img, -30)
            self.jumping_particles_left.append(img_l)
            self.jumping_particles_right.append(img_r)
        self.landing_particles = []
        for frame in range(9):
            img = img_loader(f'data/images/particle_animation/landing_particles/landing_particles{frame + 1}.PNG',
                             40, 12)
            self.landing_particles.append(img)
        # particle animation lists
        self.walking_part_animations = []
        self.jumping_part_animations = []  # one cell -> [pos, counter, direction]
        self.landing_part_animations = []
        self.particle_frame_counter = 0
        self.particle_frame_duration = 3

        # teleportation particles frames -------------------------------------------------------------------------------
        self.particles1 = img_loader('data/images/particles1.PNG', tile_size, tile_size)
        self.particles2 = img_loader('data/images/particles2.PNG', tile_size, tile_size)
        self.particles3 = img_loader('data/images/particles3.PNG', tile_size, tile_size)
        self.particles4 = img_loader('data/images/particles4.PNG', tile_size, tile_size)

        # bridge
        self.bridge_section = img_loader('data/images/bridge_section.PNG', tile_size, 7)

        # mid-air jump shockwave
        jump_shock_template = img_loader('data/images/jump_shockwave.PNG', 64, 16)
        jump_shock_template.set_colorkey((0, 0, 0))
        self.jump_shock_frames = {}
        for frame in range(1, 9):
            surf = pygame.transform.scale(jump_shock_template, (8 * frame, 2 * frame))
            surf.set_alpha(40 * (9 - frame))
            self.jump_shock_frames[frame] = surf

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
        self.jump_keys = {
            '1': img_loader('data/images/buttons/key_space.PNG', tile_size, tile_size / 2),
            '1_press': img_loader('data/images/buttons/key_space_press.PNG', tile_size, tile_size / 2),
            '2': img_loader('data/images/buttons/key_w.PNG', tile_size / 2, tile_size / 2),
            '2_press': img_loader('data/images/buttons/key_w_press.PNG', tile_size / 2, tile_size / 2),
            '3': img_loader('data/images/buttons/key_up.PNG', tile_size / 2, tile_size / 2),
            '3_press': img_loader('data/images/buttons/key_up_press.PNG', tile_size / 2, tile_size / 2),
        }
        arrow = img_loader('data/images/white_arrow.PNG', 16, 16)
        self.right_arrow = pygame.transform.rotate(arrow, -90)
        self.icn_bob_counter = 0

        self.button_press_counter = 0

        self.restart_level = False
        self.restart_trigger = False
        self.restart_counter = 0
        self.single_restart = True

        # extra card powers and their counters -------------------------------------------------------------------------
        self.mid_air_jump = False
        self.mid_air_jump_counter = 0
        self.mid_air_jumps_num = 3
        self.speed_dash = False
        self.speed_dash_stopped = False
        self.speed_dash_activated = False
        self.speed_dash_landed = True
        self.speed_dash_direction = 1
        self.speed_dash_speed = 4.5

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
        self.jump_shock_counter = 100
        self.jump_shock_pos = [0, 0]
        self.speed_dash_tutorial1 = False
        self.speed_dash_tutorial1_pos = [0, 0]

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

    def update_pos_animation(self, screen, tile_list, next_level_list, level_count, world_count, harm_in, fps_adjust,
                             mid_air_jump_trigger, speed_dash_trigger,
                             left_border, right_border,
                             move, shockwave_mush_list, events, gem_equipped, joysticks, restart_level_procedure,
                             controls, freeze_tiles):

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
            'bubbles': 0
        }

        self.controls = controls

        self.animation_counter += 1 * fps_adjust

        self.screen_shake_counter -= 1 * fps_adjust

        self.squash_counter_y += 0.5 * fps_adjust

        self.jump_shock_counter += 1 * fps_adjust

        self.jump_press_counter -= 1 * fps_adjust

        self.particle_frame_counter += 1 * fps_adjust
        if self.particle_frame_counter > self.particle_frame_duration:
            self.particle_frame_counter = 0

        if self.airborn:
            self.slide = 0.4
        else:
            self.slide = 0.3

        if not self.freeze:
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
        bottom_border = 180 / 270 * sheight
        if [level_count, world_count] == [6, 4]:
            top_border = 100 / 270 * sheight
        if [level_count, world_count] == [1, 5]:
            top_border = 130 / 270 * sheight
        if [level_count, world_count] in [[6, 3], [6, 4], [5, 4]]:
            bottom_border = 150 / 270 * sheight

        harm = False

        jump_press = False

        if world_count == 1 and level_count == 1 and self.lowering_cooldown == 15:
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

        # joystick and keyboard input management
        if events['keydown']:
            if events['keydown'].key == self.controls['jump']:
                self.player_jump = True
                if self.freeze_type == 'sd1' and self.freeze:
                    self.freeze = False
                    self.block_control = True
        if events['keyup']:
            if events['keyup'].key == self.controls['jump']:
                self.player_jump = False
        if events['joybuttondown']:
            if events['joybuttondown'].button == controls['configuration'][5]:
                self.player_jump = True
                jump_press = True
                if self.freeze_type == 'sd1' and self.freeze:
                    self.freeze = False
                    self.block_control = True
        if events['joyhatdown']:
            event = events['joyhatdown']
            if controls['configuration'][0]:
                if event.button == controls['configuration'][0][0]:  # right
                    self.hat_value[0] = 1
                if event.button == controls['configuration'][0][2]:  # left
                    self.hat_value[0] = -1
        if events['joybuttonup']:
            if events['joybuttonup'].button == controls['configuration'][5]:
                self.player_jump = False
        if events['joyhatup']:
            event = events['joyhatup']
            if event.button in [controls['configuration'][0][0], controls['configuration'][0][2]]:
                self.hat_value[0] = 0
        if events['joyaxismotion_x']:
            event = events['joyaxismotion_x']
            if event.value > 0.6:
                self.joystick_right = True
                if self.freeze_type == 'sd2' and self.freeze:
                    self.freeze = False
                    sounds['bubbles'] = 1
                    self.block_control = False
            else:
                self.joystick_right = False
            if event.value < -0.6:
                self.joystick_left = True
            else:
                self.joystick_left = False
        if events['joydeviceremoved']:
            self.joystick_left = False
            self.joystick_right = False
            self.player_jump = False

        if key[self.controls['right']]:
            if self.freeze_type == 'sd2' and self.freeze:
                self.freeze = False
                self.block_control = False
                sounds['bubbles'] = 1

        # D-pad input
        if joysticks and joysticks[0].get_numhats() > 0:
            self.hat_value = joysticks[0].get_hat(0)

        if self.freeze and self.hat_value[0] == 1:
            if self.freeze_type == 'sd2' and self.freeze:
                self.freeze = False
                sounds['bubbles'] = 1
                self.block_control = False

        # special power cards effects ----------------------------------------------------------------------------------
        if mid_air_jump_trigger and not self.mid_air_jump:
            self.mid_air_jump = True
            self.power_indicator_list.append('jump_boost')
            self.mid_air_jump_counter = 0
        if speed_dash_trigger and not self.speed_dash:
            self.speed_dash = True
            if [world_count, level_count] == [3, 2]:
                self.speed_dash_tutorial1 = True
                self.speed_dash_tutorial1_pos = [swidth / 2 + tile_size, self.sack_rect.y + 2]
            self.speed_dash_sine_counter = 0
            self.speed_dash_sine_offset_counter = 9

        # updating special power cards counters ------------------------------------------------------------------------
        append = self.power_particle_list.append
        if len(self.power_particle_list) < 50:
            if self.mid_air_jump:
                if self.mid_air_jump_counter == 0:
                    self.particle_colour = (0, 98, 10)
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
                       random.randrange(y_value - 2, y_value + 16),
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
            self.button_press_counter = 0  # respawn instructions
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

        # speed dash tutorial lock
        if self.freeze_type == 'sd0':
            self.player_jump = False

        # jump counter
        if jump_press:
            self.jump_press_counter = self.max_jump_press_counter

        # movement and animation ---------------------------------------------------------------------------------------
        if self.new_level_cooldown >= 30 and not self.dead and self.teleport_count < 20\
                and not (self.col_types['right'] or self.col_types['left']) and move and not self.transition\
                and not self.freeze:
            # player control
            if self.jump_press_counter > 0 and not self.jumped:
                self.teleport_count = 0
                if self.speed_dash_activated and self.player_jump:
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
                        self.jump_shock_counter = 5
                        self.jump_shock_pos = [self.sack_rect.x + 10, self.sack_rect.y + 20]
                    if self.mid_air_jump and self.player_jump:
                        self.vel_y = -11
                    else:
                        self.vel_y = -7.5
                        if self.vel_x_r > 1.2:
                            jump_part_direction = 1
                        elif self.vel_x_l < -1.2:
                            jump_part_direction = -1
                        else:
                            jump_part_direction = 0
                        self.jumping_part_animations.append([[self.sack_rect.x + 9, self.sack_rect.y + 11],
                                                             0, jump_part_direction])
                    sounds['jump'] = True
                    self.jump_adder = 0
                    self.jumped = True
                    self.animate_walk = False
                    self.airborn = True
                    self.jump_press_counter = 0
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
                if self.sack_rect.height != 23:
                    self.sack_rect.height = 23
                # walking left
                if (key[self.controls['left']] or self.joystick_left or self.hat_value[0] == -1)\
                        and not self.col_types['left']:
                    self.player_moved = True
                    if self.speed_dash and not self.speed_dash_activated and not self.block_control:
                        self.speed_dash_activated = True
                        sounds['bubbles'] = 1
                        self.speed_dash_stopped = False
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
                if (key[self.controls['right']] or self.joystick_right or self.hat_value[0] == 1 or
                        self.bridge_cutscene_walk) and not self.col_types['right']:
                    self.player_moved = True
                    if self.speed_dash and not self.speed_dash_activated and not self.block_control:
                        self.speed_dash_activated = True
                        sounds['bubbles'] = 1
                        self.speed_dash_stopped = False
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
                        if self.walk_counter in [2, 6]:
                            part = [[self.sack_rect.x, self.sack_rect.y + 7], 0, self.direction]
                            self.walking_part_animations.append(part)
                    if self.walk_counter > len(self.sack_walk):
                        self.walk_counter = 1
                    if self.walk_counter == 0:
                        self.sack_img = self.sack
                    else:
                        self.sack_img = self.sack_walk[self.walk_counter]
                    if self.direction == -1:
                        self.sack_img = pygame.transform.flip(self.sack_img, True, False)

            elif self.speed_dash_activated:
                self.speed_dash_tutorial1 = False
                self.sack_rect.height = 10
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
            if self.idle_counter > 10:
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
        if not self.speed_dash_activated and not self.freeze:
            if self.dead:
                self.vel_y = dy
            else:
                if not move and world_count == 1 and level_count == 1:
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
        temp_x = self.sack_rect.x + round(self.vel_x)
        adjustment = 0

        if self.vel_x != 0:
            print(self.vel_x)

        border_col = 0

        if self.sack_rect.x + self.sack_width > self.right_border:
            if self.vel_x > 0:
                self.vel_x_r = 0
                self.vel_x = 0
                self.sack_rect.x = self.right_border - self.sack_width
                self.col_types['right'] = True
            border_col = 1
        if self.sack_rect.x < self.left_border:
            if self.vel_x < 0:
                self.vel_x_l = 0
                self.vel_x = 0
                self.sack_rect.x = self.left_border
                self.col_types['left'] = True
            border_col = -1

        # freeze tile collisions
        removal_list = []
        for tile in freeze_tiles:
            if self.sack_rect.colliderect(tile[0][0], tile[0][1], tile_size, tile_size * 2):
                self.freeze_type = tile[1]
                if self.freeze_type != 'sd0':
                    self.freeze = True
                    sounds['bubbles'] = -1
                removal_list.append(tile[1])
        for tile in freeze_tiles:
            if tile[1] in removal_list:
                freeze_tiles.remove(tile)

        col_counter = 0
        col_y_tile_list = []
        append = col_y_tile_list.append
        for tile in tile_list:
            if tile[1].colliderect(temp_x, self.sack_rect.y, self.sack_width, self.sack_height):
                if self.vel_x > 0:
                    adjustment = tile[1].left - self.sack_rect.right
                    self.vel_x_r = 0
                    self.vel_x = 0
                    self.col_types['right'] = True
                if self.vel_x < 0:
                    adjustment = tile[1].right - self.sack_rect.left
                    print(adjustment)
                    self.vel_x_l = 0
                    self.vel_x = 0
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
                    self.jump_press_counter = 0
                    self.airborn = False
                    self.camera_falling_assist = False
                    self.first_collision = True
                    if self.on_ground_counter < 0:
                        self.landing_part_animations.append([[self.sack_rect.x - 11, self.sack_rect.y + 11], 0])
                    self.on_ground_counter = self.default_on_ground_counter
                    self.animate_walk = True
                    self.speed_dash_landed = True
                if dy < 0:
                    self.sack_rect.top = tile[1].bottom
                    dy = 0
                    self.vel_y = 0
                    self.col_types['top'] = True
            col_counter += 1

        self.on_ground_counter -= 1 * fps_adjust

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

        # speed dash sound stop
        if not self.speed_dash_stopped and not self.speed_dash_activated:
            self.speed_dash_stopped = True
            sounds['bubbles'] = -1

        # updating player coordinates ----------------------------------------------------------------------------------
        if not self.freeze:
            self.camera_movement_x = round(-(self.vel_x + adjustment) * fps_adjust)
            if self.col_types['right'] and self.camera_movement_x < 0:
                self.camera_movement_x = 0
            if self.col_types['left'] and self.camera_movement_x > 0:
                self.camera_movement_y = 0
            dx = 0
            if self.sack_rect.y > (bottom_border / 270 * sheight) and dy * fps_adjust > 0:
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
        else:
            dx = 0
            dy = 0
            self.camera_movement_x = 0
            self.camera_movement_y = 0

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
               self.restart_level, self.player_moved, shockwave_mush_list,\
               gem_equipped, screen_shake, sounds, border_col, freeze_tiles

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
            if self.freeze:
                particle[2] -= 0.07
            else:
                particle[2] -= 0.3
            if particle[2] < 0:
                self.power_particle_list.remove(particle)
            particle[0] += self.camera_movement_x
            particle[1] += self.camera_movement_y
            pygame.draw.circle(self.power_particle_surface, particle[3], (particle[0], particle[1]), particle[2])

        self.power_particle_surface.set_colorkey((0, 0, 0))
        screen.blit(self.power_particle_surface, (0, 0))

        # mid-air jump shockwave
        self.jump_shock_pos[0] += self.camera_movement_x
        self.jump_shock_pos[1] += self.camera_movement_y
        frame_count = round(self.jump_shock_counter / 3)
        if 0 < frame_count < 9:
            frame = self.jump_shock_frames[frame_count]
            screen.blit(frame, (self.jump_shock_pos[0] - frame.get_width() / 2,
                                self.jump_shock_pos[1] - frame.get_height() / 2))

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

            if not self.freeze:
                self.speed_dash_sine_counter += 1 * fps_adjust
            else:
                self.speed_dash_sine_counter += 0.18 * fps_adjust
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
                             self.sack_rect.y - 6))

            elif self.speed_dash_direction == -1:
                screen.blit(pygame.transform.flip(self.speed_dash_animation_surface, True, False),
                            (self.sack_rect.x + 10 - self.sack_offset,
                             self.sack_rect.y - 6))

            self.sack_img = sack_speed_dash_img

        if self.dead:
            self.blit_plr = death_animation_counter(self, fps_adjust)
            self.sack_img = self.sack_silhouette

        # drawing player onto the screen
        if self.blit_plr:
            screen.blit(self.sack_img, (self.sack_rect.x - 1 - self.sack_offset, self.sack_rect.y - 9 + squash_offset))

        if draw_hitbox and not self.dead:
            pygame.draw.rect(screen, (255, 255, 255), self.sack_rect, 1)

        # drawing teleportation particles onto the screen
        if not self.dead and self.teleport_count > 0:
            magic_animation(self, screen, self.teleport_count, particle_x)

# inter-level transition -----------------------------------------------------------------------------------------------
    def draw_transition(self, fps_adjust, long_trans):
        if self.transition:
            transition = self.circle_transition.draw_circle_transition(self.sack_rect, fps_adjust, long_trans)
            if not transition:
                self.transition = False

# draw sack particles --------------------------------------------------------------------------------------------------
    def draw_sack_particles(self, screen):
        # walking
        for particles in self.walking_part_animations:
            if self.particle_frame_counter == 0:
                particles[1] += 1
            particles[0][0] += self.camera_movement_x
            particles[0][1] += self.camera_movement_y
            if particles[2] == 1:
                img = self.walking_particles_right[particles[1]]
            else:
                img = self.walking_particles_left[particles[1]]
            screen.blit(img, particles[0])
            if particles[1] == 8:
                self.walking_part_animations.remove(particles)
        # jumping
        for particles in self.jumping_part_animations:
            if self.particle_frame_counter == 0:
                particles[1] += 1
            particles[0][0] += self.camera_movement_x
            particles[0][1] += self.camera_movement_y
            if particles[2] == 1:
                img = self.jumping_particles_right[particles[1]]
            elif particles[2] == -1:
                img = self.jumping_particles_left[particles[1]]
            else:
                img = self.jumping_particles_up[particles[1]]
            screen.blit(img, (particles[0][0] - img.get_width() / 2, particles[0][1] - img.get_height() / 2))
            if particles[1] == 7:
                self.jumping_part_animations.remove(particles)
        # landing
        for particles in self.landing_part_animations:
            if self.particle_frame_counter == 0:
                particles[1] += 1
            particles[0][0] += self.camera_movement_x
            particles[0][1] += self.camera_movement_y
            img = self.landing_particles[particles[1]]
            screen.blit(img, particles[0])
            if particles[1] == 8:
                self.landing_part_animations.remove(particles)

# instructions ---------------------------------------------------------------------------------------------------------
    def blit_button_instructions(self, screen, fps_adjust, joystick_connected, settings_counters):
        press = False
        if self.button_press_counter > 65:
            press = True
            if self.button_press_counter > 80:
                self.button_press_counter = 10
        self.icn_bob_counter += 1 * fps_adjust
        self.button_press_counter += 1 * fps_adjust
        speedrun = False
        if settings_counters['speedrun'] == 2:
            speedrun = True

        if self.health == 0 and self.dead_counter >= 36 and self.restart_counter == 0:
            x = swidth / 2 - 3 * 8

            if self.controls['configuration'][7] == 1:
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

            if joystick_connected:
                screen.blit(controller_btn, (swidth / 2 - tile_size / 4, sheight / 3 + 16))
            else:
                key_img = self.jump_keys[str(settings_counters['jumping'])]
                if press:
                    key_img = self.jump_keys[f'{settings_counters["jumping"]}_press']
                if self.button_press_counter > 8:
                    screen.blit(key_img, (swidth / 2 - key_img.get_width() / 2, sheight / 3 + 16))

        if self.freeze:
            if self.freeze_type == 'sd1':
                if self.controls['configuration'][7] == 1:
                    controller_btn = self.a_button
                else:
                    controller_btn = self.cross_button
                if joystick_connected:
                    screen.blit(controller_btn, (swidth / 2 + 3 * tile_size / 4, sheight / 3 + 16))
                else:
                    key_img = self.jump_keys[str(settings_counters['jumping'])]
                    if press:
                        key_img = self.jump_keys[f'{settings_counters["jumping"]}_press']
                    screen.blit(key_img, (swidth / 2 + tile_size, sheight / 3 + 16))
            if self.freeze_type == 'sd2':
                offset = math.sin(self.icn_bob_counter / 15) * 2
                screen.blit(self.right_arrow, (swidth / 2 + tile_size + offset, self.sack_rect.y + 2))

        if self.speed_dash_tutorial1 and not speedrun:
            self.speed_dash_tutorial1_pos[1] += self.camera_movement_y
            offset = math.sin(self.icn_bob_counter / 15) * 3
            screen.blit(self.right_arrow, (self.speed_dash_tutorial1_pos[0] + offset, self.speed_dash_tutorial1_pos[1]))


