import pygame
from level_transition import CircleTransition
from image_loader import img_loader
import random
import math

sheight = 264
swidth = 352

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
def death_animation1(self, fps_adjust):
    self.dead_counter += 1 * fps_adjust
    if self.dead_counter > 36:
        self.sack_img = self.dead6
    elif self.dead_counter > 30:
        self.sack_img = self.dead5
    elif self.dead_counter > 24:
        self.sack_img = self.dead4
    elif self.dead_counter > 18:
        self.sack_img = self.dead3
    elif self.dead_counter > 12:
        self.sack_img = self.dead2
    elif self.dead_counter > 6:
        self.sack_img = self.dead1

    return self.sack_img


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
        screen.blit(img, (particle_x + 2, self.sack_rect.y))


# ======================================================================================================================

class Player:
    def __init__(self, screen, controls, settings_counters, world_count):
        # player sprite assets -----------------------------------------------------------------------------------------
        self.sack0f = img_loader('data/images/sack0.PNG', player_size_x, player_size_y)
        self.sack1f = img_loader('data/images/sack1.PNG', player_size_x, player_size_y)
        self.sack2f = img_loader('data/images/sack2.PNG', player_size_x, player_size_y)
        self.sack0b = pygame.transform.flip(self.sack0f, True, False)
        self.sack1b = pygame.transform.flip(self.sack1f, True, False)
        self.sack2b = pygame.transform.flip(self.sack2f, True, False)
        self.sack_blinkf = img_loader('data/images/sack_eyes_closed.PNG', player_size_x, player_size_y)
        self.sack_lookf = img_loader('data/images/sack_side_look.PNG', player_size_x, player_size_y)
        self.sack_jumpf = img_loader('data/images/sack_jumping.PNG', player_size_x, player_size_y)
        self.sack_jumpb = pygame.transform.flip(self.sack_jumpf, True, False)
        self.sack_jump1f = img_loader('data/images/sack_jumping1.PNG', tile_size, tile_size)
        self.sack_jump2f = img_loader('data/images/sack_jumping2.PNG', tile_size, tile_size)
        self.sack_jump3f = img_loader('data/images/sack_jumping3.PNG', tile_size, tile_size)
        self.sack_jump1b = pygame.transform.flip(self.sack_jump1f, True, False)
        self.sack_jump2b = pygame.transform.flip(self.sack_jump2f, True, False)
        self.sack_jump3b = pygame.transform.flip(self.sack_jump3f, True, False)
        self.sack_blinkb = pygame.transform.flip(self.sack_blinkf, True, False)
        self.sack_lookb = pygame.transform.flip(self.sack_lookf, True, False)
        self.sack_speed_dash1 = img_loader('data/images/sack_speed_dash1.PNG', player_size_x, 22)
        self.sack_speed_dash2 = img_loader('data/images/sack_speed_dash2.PNG', player_size_x, 22)
        self.sack_speed_dash3 = img_loader('data/images/sack_speed_dash3.PNG', player_size_x, 22)
        self.sack_speed_dash4 = img_loader('data/images/sack_speed_dash4.PNG', player_size_x, 22)
        self.sack_img = self.sack0f
        self.sack_rect = self.sack0f.get_rect()
        self.dead_rect = img_loader('data/images/sack0.PNG', 4, player_size_y).get_rect()
        self.sack_rect.x = swidth / 2 - self.sack_rect.width / 2
        self.sack_rect.y = sheight / 2 - self.sack_rect.height / 2
        self.player_speed = 2.42
        self.slide = 0.4
        self.default_on_ground_counter = 6
        self.on_ground_counter = self.default_on_ground_counter
        self.sack_width = self.sack0f.get_width()
        self.sack_height = self.sack0f.get_height()
        self.vel_y = 0
        self.vel_x_l = 0
        self.vel_x_r = 0
        self.vel_x = 0
        self.jumped = False
        self.sack_offset = 0
        self.squash_counter_x = 10
        self.squash_counter_y = 10

        damage_animation_colour = (180, 25, 25)

        self.sack0f_mask = pygame.mask.from_surface(self.sack0f)
        self.sack0f_damage = pygame.mask.Mask.to_surface(self.sack0f_mask, setcolor=damage_animation_colour)
        self.sack1f_mask = pygame.mask.from_surface(self.sack1f)
        self.sack1f_damage = pygame.mask.Mask.to_surface(self.sack1f_mask, setcolor=damage_animation_colour)
        self.sack2f_mask = pygame.mask.from_surface(self.sack2f)
        self.sack2f_damage = pygame.mask.Mask.to_surface(self.sack2f_mask, setcolor=damage_animation_colour)

        self.sack_jump1f_mask = pygame.mask.from_surface(self.sack_jump1f)
        self.sack_jump1f_damage = pygame.mask.Mask.to_surface(self.sack_jump1f_mask, setcolor=damage_animation_colour)
        self.sack_jump2f_mask = pygame.mask.from_surface(self.sack_jump2f)
        self.sack_jump2f_damage = pygame.mask.Mask.to_surface(self.sack_jump2f_mask, setcolor=damage_animation_colour)
        self.sack_jump3f_mask = pygame.mask.from_surface(self.sack_jump3f)
        self.sack_jump3f_damage = pygame.mask.Mask.to_surface(self.sack_jump3f_mask, setcolor=damage_animation_colour)

        self.sack0f_damage.set_colorkey((0, 0, 0))
        self.sack1f_damage.set_colorkey((0, 0, 0))
        self.sack2f_damage.set_colorkey((0, 0, 0))
        self.sack_jump3f_damage.set_colorkey((0, 0, 0))
        self.sack_jump1f_damage.set_colorkey((0, 0, 0))
        self.sack_jump2f_damage.set_colorkey((0, 0, 0))

        self.sack_damage_img = self.sack0f_damage

        self.controls = controls
        self.settings_counters = settings_counters
        self.world_count = world_count

        # player sprite death animation frames -------------------------------------------------------------------------
        self.dead1 = img_loader('data/images/dead_sack1.PNG', tile_size, tile_size)
        self.dead2 = img_loader('data/images/dead_sack2.PNG', tile_size, tile_size)
        self.dead3 = img_loader('data/images/dead_sack3.PNG', tile_size, tile_size)
        self.dead4 = img_loader('data/images/dead_sack4.PNG', tile_size, tile_size)
        self.dead5 = img_loader('data/images/dead_sack5.PNG', tile_size, tile_size)
        self.dead6 = img_loader('data/images/dead_sack6.PNG', tile_size, tile_size)

        # speed dash transition animation frames -----------------------------------------------------------------------
        self.dash_transition1 = img_loader('data/images/sack_speed_dash_transition1.PNG', player_size_x, player_size_y)
        self.dash_transition2 = img_loader('data/images/sack_speed_dash_transition2.PNG', player_size_x, player_size_y)
        self.dash_transition3 = img_loader('data/images/sack_speed_dash_transition3.PNG', player_size_x, player_size_y)
        self.dash_transition4 = img_loader('data/images/sack_speed_dash_transition4.PNG', player_size_x, player_size_y)

        # teleportation particles frames -------------------------------------------------------------------------------
        self.particles1 = img_loader('data/images/particles1.PNG', tile_size, tile_size)
        self.particles2 = img_loader('data/images/particles2.PNG', tile_size, tile_size)
        self.particles3 = img_loader('data/images/particles3.PNG', tile_size, tile_size)
        self.particles4 = img_loader('data/images/particles4.PNG', tile_size, tile_size)

        # card powers indicator images ---------------------------------------------------------------------------------
        self.jump_boost_indicator = img_loader('data/images/icon_jump_boost.PNG', tile_size, tile_size)
        self.no_gravity_indicator = img_loader('data/images/icon_no_gravity.PNG', tile_size, tile_size)
        self.no_harm_indicator = img_loader('data/images/icon_no_harm.PNG', tile_size, tile_size)

        self.jump_boost_surf = pygame.Surface((tile_size, tile_size))
        self.no_harm_surf = pygame.Surface((tile_size, tile_size))
        self.no_gravity_surf = pygame.Surface((tile_size, tile_size))

        self.progress_bar = pygame.Surface((tile_size, 18))
        self.progress_bar.set_alpha(128)
        self.progress_bar.fill((0, 0, 0))

        # respawn instruction images and variables ---------------------------------------------------------------------
        self.respawn_instr1 = img_loader('data/images/respawn_instructions1.PNG', tile_size * 2, tile_size)
        self.respawn_instr2 = img_loader('data/images/respawn_instructions2.PNG', tile_size * 2, tile_size)
        self.respawn_instructions_blit_counter = 0
        self.respawn_instructions_blit_counter = 0

        self.restart_level = False
        self.restart_trigger = False
        self.restart_counter = 0
        self.single_restart = True

        # extra card powers and their counters -------------------------------------------------------------------------
        self.mid_air_jump = False
        self.mid_air_jump_counter = 0
        self.mid_air_jump_duration = 450
        self.speed_dash = False
        self.speed_dash_activated = False
        self.speed_dash_direction = 1
        self.speed_dash_speed = 5
        self.regeneration = False
        self.regeneration_counter = 0
        self.no_gravity = False
        self.no_gravity_counter = 0
        self.no_gravity_duration = 180
        self.no_harm = False
        self.no_harm_counter = 0
        self.no_harm_duration = 300

        # other player variables ---------------------------------------------------------------------------------------
        self.walk_counter = 0
        self.blink_counter = 0
        self.direction = 1
        self.animate_walk = True
        self.new_level = False
        self.new_level_cooldown = 70
        self.teleport_count = 0
        self.health = 2
        self.harmed = False
        self.dead = False
        self.transition = False
        self.dead_counter = 0
        self.airborn = False
        self.break_transition = False
        self.transition_get_smaller = True
        self.lowest_tile = 0
        self.highest_tile = 264
        self.speed = 0
        self.speed_adder = 0
        self.player_moved = False
        self.blit_plr = True
        self.harm_counter = 40
        self.damage = False
        self.damage_counter = 0
        self.harm_flash_counter = 0
        self.init_flash = False
        self.first_power_jump = False

        self.speed_dash_sine_counter = 0
        self.speed_dash_animation_counter = 0
        self.speed_dash_sine_offset_counter = 9
        self.speed_dash_animation_surface = pygame.Surface((40, 40))
        self.speed_dash_animation_surface.set_colorkey((0, 0, 0))
        self.speed_dash_animation_surface.fill((0, 0, 0))

        # music and sounds ---------------------------------------------------------------------------------------------
        self.first_level_play_music = True
        self.play_music = False
        self.single_play = True
        self.fadeout = False
        self.single_fadeout = True
        self.music_faded = False
        self.play_once = False
        self.song = 'game_song1'

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
        self.power_particle_surface = pygame.Surface((swidth, sheight))
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
        self.hey_particle1 = HeyParticle(self.hey_part1, self.hey_part2, self.hey_part3, self.sack_rect)
        self.circle_transition = CircleTransition(screen)

    def update_pos_animation(self, screen, tile_list, next_level_list, level_count, harm_in, fps_adjust,
                             mid_air_jump_trigger, speed_dash_trigger,
                             left_border, right_border, game_counter,
                             move, shockwave_mush_list, events, over_card):

        dx = 0
        dy = 0

        self.damage_counter -= 1

        self.squash_counter_y += 0.5

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
        if level_count == 8:
            top_border = 80
        else:
            top_border = 50

        harm = False

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
        if harm_in and self.teleport_count <= 100:
            harm = True

        # joystick input management
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.controls['jump']:
                self.player_jump = True
            if event.type == pygame.KEYUP and event.key == self.controls['jump']:
                self.player_jump = False
            if event.type == pygame.JOYBUTTONDOWN and not over_card:
                if event.button == 0:
                    self.player_jump = True
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    self.player_jump = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > 0.2:
                        self.joystick_right = True
                    else:
                        self.joystick_right = False
                    if event.value < -0.2:
                        self.joystick_left = True
                    else:
                        self.joystick_left = False
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystick_left = False
                self.joystick_right = False
                self.player_jump = False

        # special power cards effects ----------------------------------------------------------------------------------
        if mid_air_jump_trigger and not self.mid_air_jump:
            self.mid_air_jump = True
            self.power_indicator_list.append('jump_boost')
        if speed_dash_trigger and not self.speed_dash:
            self.speed_dash = True
            self.speed_dash_sine_counter = 0
            self.speed_dash_sine_offset_counter = 9

        # updating special power cards counters ------------------------------------------------------------------------
        if self.mid_air_jump:
            self.mid_air_jump_counter += 1 * fps_adjust
            self.particle_colour = (67, 124, 94)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])
        if self.speed_dash:
            self.particle_colour = (70, 161, 193)
            x_value = int(self.sack_rect.x)
            y_value = int(self.sack_rect.y)
            self.power_particle_list.append([random.randrange(x_value, x_value + self.sack_width),
                                             random.randrange(y_value, y_value + self.sack_height),
                                             random.randrange(6, 14),
                                             self.particle_colour])

        # special power cards duration counters ------------------------------------------------------------------------
        if self.mid_air_jump_counter >= self.mid_air_jump_duration:
            self.mid_air_jump_counter = 0
            self.power_indicator_list.remove('jump_boost')
            self.mid_air_jump = False

        # subtracting health if player is being harmed
        if not self.harmed and harm and self.player_moved:
            self.health = 0
            self.dead = True
            self.harmed = True
            self.speed_dash = False
            self.speed_dash_activated = False

        if not self.player_moved:
            self.health = 2

        if not harm:
            self.harmed = False

        if self.dead:
            self.sack_img = death_animation1(self, fps_adjust)

        # next level portal collisions ---------------------------------------------------------------------------------
        for tile in next_level_list:
            song_loops = -1
            if tile[1].colliderect(self.sack_rect.x, self.sack_rect.y,
                                   self.sack_width, self.sack_height) and not self.dead:
                self.teleport_count += 1*fps_adjust
                if self.teleport_count >= 100:
                    if not self.transition:
                        self.circle_transition = CircleTransition(screen)
                    self.transition = True
                    # music loading
                    if self.world_count == 1 and level_count == 2:
                        self.fadeout = True
                    if self.world_count == 2:
                        if level_count == 8:
                            self.fadeout = True

                if self.teleport_count >= 130:
                    if self.mid_air_jump:
                        self.mid_air_jump_counter = 1000
                    if self.no_gravity:
                        self.no_gravity_counter = 1000
                    if self.no_harm:
                        self.no_harm_counter = 1000
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

        # movement and animation ---------------------------------------------------------------------------------------
        if self.new_level_cooldown >= 30 and not self.dead and self.teleport_count < 100\
                and not (self.col_types['right'] or self.col_types['left']) and game_counter >= 0 and move:
            # player control
            self.transition = False
            if self.player_jump and not self.jumped:
                self.teleport_count = 0
                if self.speed_dash_activated:
                    self.speed_dash_activated = False
                    self.speed_dash = False
                    self.vel_y = -8
                self.player_moved = True
                if not self.jumped and \
                        ((self.on_ground_counter > 0 and not self.airborn) or self.dy > 5 and self.mid_air_jump):
                    self.vel_y = -11
                    self.jumped = True
                    self.player_jump = False
                    self.animate_walk = False
                    self.airborn = True

            if not key[self.controls['jump']]:
                self.jumped = False
                if not self.airborn:
                    # standing animation
                    self.sack_offset = 0
                    if self.direction == 1:
                        self.blink_counter += 1*fps_adjust
                        if self.blink_counter > 150:
                            self.blink_counter = 0
                        if self.blink_counter > 75:
                            self.sack_img = self.sack0f
                            self.sack_damage_img = self.sack0f_damage
                        elif self.blink_counter > 60:
                            self.sack_img = self.sack_blinkf
                            self.sack_damage_img = self.sack0f_damage
                        elif self.blink_counter > 30:
                            self.sack_img = self.sack_lookf
                            self.sack_damage_img = self.sack0f_damage
                        elif self.blink_counter > 15:
                            self.sack_img = self.sack_blinkf
                            self.sack_damage_img = self.sack0f_damage
                        else:
                            self.sack_img = self.sack0f
                            self.sack_damage_img = self.sack0f_damage
                    elif self.direction == 0:
                        self.blink_counter += 1*fps_adjust
                        if self.blink_counter > 150:
                            self.blink_counter = 0
                        if self.blink_counter > 75:
                            self.sack_img = self.sack0b
                            self.sack_damage_img = pygame.transform.flip(self.sack0f_damage, True, False)
                        elif self.blink_counter > 60:
                            self.sack_img = self.sack_blinkb
                            self.sack_damage_img = pygame.transform.flip(self.sack0f_damage, True, False)
                        elif self.blink_counter > 30:
                            self.sack_img = self.sack_lookb
                            self.sack_damage_img = pygame.transform.flip(self.sack0f_damage, True, False)
                        elif self.blink_counter > 15:
                            self.sack_img = self.sack_blinkb
                            self.sack_damage_img = pygame.transform.flip(self.sack0f_damage, True, False)
                        else:
                            self.sack_img = self.sack0b
                            self.sack_damage_img = pygame.transform.flip(self.sack0f_damage, True, False)

            if self.airborn and not self.col_types['bottom'] and not self.speed_dash_activated:
                if self.direction == 1:
                    self.sack_offset = jump_offset_amount - 3
                    if self.vel_y < -5:
                        self.sack_img = self.sack_jump1f
                    elif -5 < self.vel_y < 3:
                        self.sack_img = self.sack_jump2f
                    else:
                        self.sack_img = self.sack_jump3f
                else:
                    self.sack_offset = jump_offset_amount + 4
                    if self.vel_y < -5:
                        self.sack_img = self.sack_jump1b
                    elif -5 < self.vel_y < 3:
                        self.sack_img = self.sack_jump2b
                    else:
                        self.sack_img = self.sack_jump3b

            walking_left = False
            walking_right = False

            if not self.speed_dash_activated:
                if self.sack_rect.height != 32:
                    self.sack_rect.height = 32
                # walking left
                if key[self.controls['left']] or self.joystick_left:
                    self.player_moved = True
                    if self.speed_dash:
                        self.speed_dash_activated = True
                        self.vel_y = 0
                        self.sack_offset = 0
                        self.speed_dash_direction = -1
                    walking_left = True
                    self.speed_adder += 0.1 * fps_adjust
                    self.speed += self.speed_adder
                    if self.speed > self.player_speed:
                        self.speed = self.player_speed * fps_adjust
                    dx -= self.speed
                    self.vel_x_l = dx
                    self.vel_x_r = 0
                    self.direction = 0
                    self.teleport_count = 0
                    if self.animate_walk:
                        self.walk_counter += 0.8 * fps_adjust
                        if self.walk_counter > 20:
                            self.walk_counter = 0
                        elif self.walk_counter > 15:
                            self.sack_img = self.sack2b
                        elif self.walk_counter > 10:
                            self.sack_img = self.sack0b
                        elif self.walk_counter > 5:
                            self.sack_img = self.sack1b
                        else:
                            self.sack_img = self.sack0b

                # walking right
                if key[self.controls['right']] or self.joystick_right:
                    self.player_moved = True
                    if self.speed_dash:
                        self.speed_dash_activated = True
                        self.vel_y = 0
                        self.sack_offset = 0
                        self.speed_dash_direction = 1
                    walking_right = True
                    self.speed_adder += 0.1 * fps_adjust
                    self.speed += self.speed_adder
                    if self.speed > self.player_speed:
                        self.speed = self.player_speed * fps_adjust
                    dx += self.speed
                    self.vel_x_r = dx
                    self.vel_x_l = 0
                    self.teleport_count = 0
                    self.direction = 1
                    if self.animate_walk:
                        self.walk_counter += 0.8 * fps_adjust
                        if self.walk_counter > 20:
                            self.walk_counter = 0
                        elif self.walk_counter > 15:
                            self.sack_img = self.sack2f
                        elif self.walk_counter > 10:
                            self.sack_img = self.sack0f
                        elif self.walk_counter > 5:
                            self.sack_img = self.sack1f
                        else:
                            self.sack_img = self.sack0f

                if not walking_right and not walking_left:
                    self.speed = 0
                    self.speed_adder = 0

                if walking_right and walking_left:
                    self.speed = 0
                    self.speed_adder = 0
                    self.walk_counter = 0

            elif self.speed_dash_activated:
                self.sack_rect.height = 20
                self.sack_offset = 0
                if self.speed_dash_direction == -1:
                    if self.vel_x_l > -self.speed_dash_speed:
                        self.vel_x_l -= 1 * fps_adjust
                    else:
                        self.vel_x_l = self.speed_dash_speed * fps_adjust * self.speed_dash_direction
                elif self.speed_dash_direction == 1:
                    if self.vel_x_r < self.speed_dash_speed:
                        self.vel_x_r += 1 * fps_adjust
                    else:
                        self.vel_x_r = self.speed_dash_speed * fps_adjust * self.speed_dash_direction

        # respawn at the beginning of the level and transition
        if (pygame.mouse.get_pressed()[0] or self.player_jump)\
                and self.dead and self.dead_counter >= 36 and not self.restart_trigger:
            self.restart_trigger = True
            self.single_fadeout = True
            self.teleport_count = 0
            self.circle_transition = CircleTransition(screen)
            self.init_flash = False

        if self.restart_trigger:
            self.restart_counter += 1 * fps_adjust

        if self.restart_counter > 20:
            self.transition = True
            if self.single_fadeout:
                self.fadeout = True
                self.single_fadeout = False

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
            if self.no_gravity:
                self.vel_y = dy
            else:
                self.vel_y += 0.6 * fps_adjust
                if self.vel_y > 8:
                    self.vel_y = 8
            dy = self.vel_y*fps_adjust

        # collision detection and position -----------------------------------------------------------------------------
        hit_list_x = []
        self.vel_x = self.vel_x_l + self.vel_x_r
        temp_rect = self.sack_rect
        temp_rect.x += (self.vel_x + 0.5)

        if self.dead:
            x_adjust = 15
            sack_width = 2
        else:
            x_adjust = 0
            sack_width = self.sack_width

        for tile in tile_list:
            if tile[1].colliderect(temp_rect.x + x_adjust + dx, temp_rect.y, sack_width, self.sack_height):
                hit_list_x.append(tile)

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

        for tile in hit_list_x:
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

        if (self.col_types['left'] or self.col_types['right']) and self.speed_dash_activated:
            self.speed_dash_activated = False
            self.speed_dash = False
            self.vel_y = -10

        hit_list_y = []
        for tile in tile_list:
            if tile[1].colliderect(self.sack_rect.x + x_adjust, self.sack_rect.y + dy, sack_width, self.sack_height):
                hit_list_y.append(tile)

        self.on_ground_counter -= 1

        for tile in hit_list_y:
            if dy > 0:
                self.sack_rect.bottom = tile[1].top
                if (self.airborn or dy > 8) and self.player_moved:
                    self.squash_counter_y = -2
                dy = 0
                self.vel_y = 0
                self.col_types['bottom'] = True
                self.airborn = False
                self.camera_falling_assist = False
                self.first_collision = True
                self.on_ground_counter = self.default_on_ground_counter
                self.animate_walk = True
            if dy < 0:
                self.sack_rect.top = tile[1].bottom
                dy = 0
                self.vel_y = 0
                self.col_types['top'] = True

        # mushroom collisions
        for mushroom in shockwave_mush_list:
            if fps_adjust >= 2:
                y_movement = dy
            else:
                y_movement = 0
            if mushroom[1].colliderect(self.sack_rect.x + 7,
                                       self.sack_rect.y + y_movement, 6, self.sack_height)\
                    and not self.dead and dy > 1 and self.sack_rect.y < mushroom[1][1] and mushroom[3] == 0:
                mushroom[2] = 12
                mushroom[3] = 60
                dy = 0
                self.vel_y = -7

        # next level position
        if self.new_level:
            self.sack_rect.y = 264 / 2 - 16
            self.direction = 1
            self.new_level = False

        # ensuring the player sprite is always in the middle level of the screen
        self.sack_rect.x = 164
        if not self.first_collision:
            self.sack_rect.y = 132

        # preventing the player from falling out of the world
        if self.sack_rect.bottom > sheight:
            self.sack_rect.bottom = sheight
            dy = 0
        if self.sack_rect.top + dy < 0:
            self.sack_rect.top = 0
            dy = 0

        # updating hey particles ---------------------------------------------------------------------------------------
        self.hey_particle1.update_particle(self.sack_rect, fps_adjust, self.new_level,
                                           self.camera_movement_x, self.camera_movement_y)

        # updating player coordinates ----------------------------------------------------------------------------------
        self.camera_movement_x = round(-self.vel_x)
        dx = 0
        if self.sack_rect.y > 180 and dy * fps_adjust > 0:
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
               self.fadeout, self.restart_level, self.player_moved, self.new_level_cooldown, shockwave_mush_list

# UPDATING PLAYER SPRITE HEALTH ========================================================================================
    def update_health(self):
        if self.dead:
            self.health = 0
            if self.mid_air_jump:
                self.mid_air_jump_counter = 1000

# displaying the currently used power icon -----------------------------------------------------------------------------
    def player_power_indicator(self, screen):
        spacer = 0
        for icon in self.power_indicator_list:
            if icon == 'jump_boost':
                percentage = self.mid_air_jump_duration / self.mid_air_jump_counter
                bar_y = int(18 / percentage)
                self.jump_boost_surf.blit(self.jump_boost_indicator, (0, 0))
                self.jump_boost_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.jump_boost_surf.set_colorkey((0, 0, 0))
                screen.blit(self.jump_boost_surf, (2*tile_size + spacer, 0))
            elif icon == 'no_gravity':
                percentage = self.no_gravity_duration / self.no_gravity_counter
                bar_y = int(18 / percentage)
                self.no_gravity_surf.blit(self.no_gravity_indicator, (0, 0))
                self.no_gravity_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.no_gravity_surf.set_colorkey((0, 0, 0))
                screen.blit(self.no_gravity_surf, (2*tile_size + spacer, 0))
            elif icon == 'no_harm':
                percentage = self.no_harm_duration / self.no_harm_counter
                bar_y = int(18 / percentage)
                self.no_harm_surf.blit(self.no_harm_indicator, (0, 0))
                self.no_harm_surf.blit(self.progress_bar, (0, bar_y + 8))
                self.no_harm_surf.set_colorkey((0, 0, 0))
                screen.blit(self.no_harm_surf, (2*tile_size + spacer, 0))
            spacer += 32

# BLITTING PLAYER SPRITE ONTO THE SCREEN ===============================================================================
    def blit_player(self, screen, draw_hitbox, fps_adjust):
        particle_x = self.sack_rect.x - 8
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
        if -2 <= self.squash_counter_y <= 2:
            width = self.sack_img.get_width()
            height = self.sack_img.get_height()
            self.sack_img = pygame.transform.scale(self.sack_img,
                                                   (width,
                                                    height - (2 - abs(self.squash_counter_y))))
            self.sack_damage_img = pygame.transform.scale(self.sack_damage_img,
                                                          (width,
                                                           height - (2 - abs(self.squash_counter_y))))
            squash_offset = 2 - abs(self.squash_counter_y)
        else:
            squash_offset = 0

        # speed dash visual effects
        if self.speed_dash_activated:
            if self.speed_dash_sine_counter > 10:
                sack_speed_dash_img = self.sack_speed_dash1
                if self.speed_dash_animation_counter >= 40:
                    self.speed_dash_animation_counter = 0
                    sack_speed_dash_img = self.sack_speed_dash1
                elif self.speed_dash_animation_counter >= 30:
                    sack_speed_dash_img = self.sack_speed_dash4
                elif self.speed_dash_animation_counter >= 20:
                    sack_speed_dash_img = self.sack_speed_dash3
                elif self.speed_dash_animation_counter >= 10:
                    sack_speed_dash_img = self.sack_speed_dash2
                elif self.speed_dash_animation_counter >= 0:
                    sack_speed_dash_img = self.sack_speed_dash1
            elif self.speed_dash_sine_counter > 7:
                sack_speed_dash_img = self.dash_transition4
            elif self.speed_dash_sine_counter > 5:
                sack_speed_dash_img = self.dash_transition3
            elif self.speed_dash_sine_counter > 2:
                sack_speed_dash_img = self.dash_transition2
            elif self.speed_dash_sine_counter >= 0:
                sack_speed_dash_img = self.dash_transition1
            else:
                sack_speed_dash_img = self.dash_transition1

            self.speed_dash_sine_counter += 1 * fps_adjust
            self.speed_dash_animation_counter += 1 * fps_adjust
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
                pygame.draw.circle(self.speed_dash_animation_surface, (234, 212, 170), (x, y + 15), radius, 0)
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

                self.sack_img = sack_speed_dash_img

            elif self.speed_dash_direction == -1:
                screen.blit(pygame.transform.flip(self.speed_dash_animation_surface, True, False),
                            (self.sack_rect.x + 10 - self.sack_offset,
                             self.sack_rect.y - 1))

                self.sack_img = pygame.transform.flip(sack_speed_dash_img, True, False)

        # drawing player onto the screen
        if self.blit_plr:
            screen.blit(self.sack_img, (self.sack_rect.x - self.sack_offset, self.sack_rect.y + squash_offset))

        if draw_hitbox:
            pygame.draw.rect(screen, (255, 255, 255), self.sack_rect, 1)

        # hey particles
        self.hey_particle1.blit_particle(screen)

        # drawing teleportation particles onto the screen
        if not self.dead and self.teleport_count > 20:
            magic_animation(self, screen, self.teleport_count, particle_x)

# inter-level transition -----------------------------------------------------------------------------------------------
    def draw_transition(self, fps_adjust):
        if self.transition:
            self.circle_transition.draw_circle_transition(self.sack_rect, fps_adjust)

# respawn instructions -------------------------------------------------------------------------------------------------
    def blit_respawn_instructions(self, screen, fps_adjust):
        if self.health == 0 and self.dead_counter >= 36 and self.restart_counter == 0:
            self.respawn_instructions_blit_counter += 1 * fps_adjust

            if self.respawn_instructions_blit_counter > 54:
                self.respawn_instructions_blit_counter = 0
                img = self.respawn_instr1
            elif self.respawn_instructions_blit_counter > 44:
                img = self.respawn_instr2
            else:
                img = self.respawn_instr1

            screen.blit(img, (swidth / 2 - tile_size, sheight / 3 - (tile_size / 2)))

