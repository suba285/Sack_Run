import pygame

# this function is used to load images, adjust their size and turn the black background transparent


def img_loader(path, width, height):
    img_raw = pygame.image.load(path).convert()
    img = pygame.transform.scale(img_raw, (width, height))
    img.set_colorkey((0, 0, 0))
    return img
