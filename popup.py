from screen_info import swidth
import pygame._sdl2
import math


# popup function
def draw_popup(screen, popup, element, popup_counter, bob=False, fps_adjust=1):
    popup_scale = 1
    if popup_counter <= 10:
        popup_scale = popup_counter / 10
    if 270 > popup_counter > 10:
        popup_scale = 1
    if 280 > popup_counter >= 270:
        popup_scale = (10 - (popup_counter - 270)) / 10
    if popup_scale > 0 and popup_counter < 280:
        if popup_scale != 1:
            final_popup = pygame.transform.scale(popup, (popup.get_width() * popup_scale, popup.get_height()))
        else:
            final_popup = popup
        x = swidth / 2 - final_popup.get_width() / 2
        y = 10
        offset = math.sin((1 / 15) * popup_counter) * 2
        screen.blit(final_popup, (x, y))
        if element:
            if popup_scale != 1:
                img = pygame.transform.scale(element[0], (element[0].get_width() * popup_scale, element[0].get_height()))
            else:
                img = element[0]
            screen.blit(img, (x + element[1][0] * popup_scale, y + element[1][1] + offset))
