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
#   traditional loading time: 0.0003 (traditional is way faster)
#   img_loader time: 0.001

# surface with particles vs individual particles:
#   surface with particles: 0.00025
#   individual particles: 0.0001 <-- FASTER

pygame.init()
screen = pygame.display.set_mode((500, 500))
img = img_loader('data/images/menu_background.PNG', 150, 120)
tm = time.time()
for i in range(100):
    screen.set_at((0, 0), (255, 255, 0))
tm = time.time() - tm
print(tm)
pygame.quit()
