import pygame._sdl2

tile_size = 32
sack_width = 20
sack_height = 32


class BearTrap:
    def __init__(self):

        # images -------------------------------------------------------------------------------------------------------
        bear_trap_open = pygame.image.load('data/images/bear_trap_open.PNG').convert()
        bear_trap_shut = pygame.image.load('data/images/bear_trap_shut.PNG').convert()
        self.bear_trap_open_img = pygame.transform.scale(bear_trap_open, (tile_size, tile_size / 2))
        self.bear_trap_open_img.set_colorkey((0, 0, 0))
        self.bear_trap_shut_img = pygame.transform.scale(bear_trap_shut, (tile_size, tile_size / 2))
        self.bear_trap_shut_img.set_colorkey((0, 0, 0))
        self.img = self.bear_trap_open_img

        # variables ----------------------------------------------------------------------------------------------------
        self.bear_trap_shut = False
        self.harm = False

    def bear_trap_update(self, camera_move_x, camera_move_y, bear_trap_rect_list):
        for num in range(len(bear_trap_rect_list)):
            rect = bear_trap_rect_list[num]
            rect[1][0] += camera_move_x
            rect[1][1] += camera_move_y

    def bear_trap_blit(self, screen, sack_rect, shut_trap_list, bear_trap_rect_list):
        self.harm = False
        play_bear_trap_cling = False
        for num in range(len(bear_trap_rect_list)):
            rect = bear_trap_rect_list[num]
            shut = shut_trap_list[num]
            if rect[1].colliderect(sack_rect.x, sack_rect.y, sack_rect.width, sack_rect.height) and not shut:
                self.bear_trap_shut = True
                shut = True
                self.harm = True
            if self.bear_trap_shut or shut:
                self.img = self.bear_trap_shut_img
                self.bear_trap_shut = False
            else:
                self.img = self.bear_trap_open_img

            shut_trap_list[num] = shut

            screen.blit(self.img, (rect[1][0] - 12, rect[1][1] - 8))

        if self.harm:
            play_bear_trap_cling = True

        return self.harm, play_bear_trap_cling




