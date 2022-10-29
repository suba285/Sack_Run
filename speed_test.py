import pygame
from image_loader import img_loader
import time
# drawing circle vs blitting circle:
#   pygame.draw.circle time = 0.00015
#   screen.blit_time = 0.0015 (10 times longer than pygame.draw.circle)
# blitting one big surface vs many small ones:
#   one big time: 0.00012
#   small ones time: 5 (conclusion: better to blit one big than many small ones)
# img_loader vs traditional loading:
#   traditional loading time: 0.0003 (tranditional is way faster
#   img_loader time: 0.001


def hello(hello, yes, no, go, hi, he, now, many, frick):
    print(hello)
    return hello


pygame.init()
screen = pygame.display.set_mode((100, 100))
tm = time.time()
hello('hello', 1, 2, 3, 3, 4, 5, 2, 3)
tm = time.time() - tm
print(tm)
pygame.quit()
