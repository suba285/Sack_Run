import pygame._sdl2
from image_loader import img_loader


def popup_bg_generator(dimensions):
    width = dimensions[0]
    height = dimensions[1]

    surface = pygame.Surface((width + 8, height + 8), pygame.HWACCEL).convert_alpha()

    corner1 = img_loader('data/images/popup_corner.PNG', 4, 4)
    corner2 = pygame.transform.rotate(corner1, 90)
    corner3 = pygame.transform.rotate(corner2, 90)
    corner4 = pygame.transform.rotate(corner3, 90)
    side1 = img_loader('data/images/popup_side.PNG', width, 4)
    side2 = pygame.transform.rotate(img_loader('data/images/popup_side.PNG', height, 4), 90)
    side3 = pygame.transform.flip(side1, False, True)
    side4 = pygame.transform.flip(side2, True, False)
    bg = img_loader('data/images/popup_bg.PNG', width, height)

    surface.blit(bg, (4, 4))
    surface.blit(side1, (4, 0))
    surface.blit(side3, (4, height + 4))
    surface.blit(side4, (width + 4, 4))
    surface.blit(side2, (0, 4))
    surface.blit(corner1, (0, 0))
    surface.blit(corner2, (0, height + 4))
    surface.blit(corner3, (width + 4, height + 4))
    surface.blit(corner4, (width + 4, 0))

    surface.set_colorkey((0, 0, 0))

    return surface


