
from image_loader import img_loader
from font_manager import Text
from button import Button

swidth = 360
sheight = 264
tile_size = 32


class PauseScreen:
    def __init__(self, pause_screen):
        self.pause_screen = pause_screen

        self.background = img_loader('data/images/menu_background.PNG', swidth, sheight)

        self.resume_button = img_loader('data/images/button_resume.PNG', tile_size * 1.5, tile_size * 0.75)
        self.resume_button_press = img_loader('data/images/button_resume_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.resume_button_down = img_loader('data/images/button_resume_down.PNG', tile_size * 1.5, tile_size * 0.75)

        self.menu_button = img_loader('data/images/button_menu.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_press = img_loader('data/images/button_menu_press.PNG', tile_size * 1.5, tile_size * 0.75)
        self.menu_button_down = img_loader('data/images/button_menu_down.PNG', tile_size * 1.5, tile_size * 0.75)

        paused_text = Text()
        self.paused_txt = paused_text.make_text(['paused'])

        self.resume_btn = Button(swidth / 2 - self.resume_button.get_width() / 2, 64,
                                 self.resume_button, self.resume_button_press, self.resume_button_down)
        self.menu_btn = Button(swidth / 2 - self.menu_button.get_width() / 2, 98,
                               self.menu_button, self.menu_button_press, self.menu_button_down)

    def draw_pause_screen(self, mouse_adjustment, events):

        self.pause_screen.blit(self.background, (0, 0))

        self.pause_screen.blit(self.paused_txt, (swidth / 2 - self.paused_txt.get_width() / 2, 40))

        resume = False
        menu = False
        prev_level = False

        over1 = False
        over2 = False
        over3 = False
        final_over1 = False
        final_over2 = False

        resume, over1 = self.resume_btn.draw_button(self.pause_screen, False, mouse_adjustment, events)
        menu, over2 = self.menu_btn.draw_button(self.pause_screen, False, mouse_adjustment, events)

        if over1 or over2:
            final_over1 = True

        return self.pause_screen, final_over1, resume, menu



