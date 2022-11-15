import pygame
from image_loader import img_loader


class Text:
    def __init__(self):
        self.characters = []
        self.ready_characters = []
        self.char_dimentions = (5, 9)
        num_of_charachters = 75
        num_tiles = num_of_charachters
        for num in range(num_tiles):
            self.characters.append(img_loader(f"data/font/letter{num}.PNG",
                                               self.char_dimentions[0], self.char_dimentions[1]))

        self.num_of_lines = 0
        self.num_of_chars = 0
        self.char_x = 0
        self.char_y = 0
        self.line_spacing = 11
        self.space = 5
        self.char_spacing = 1
        self.longest_line = 0

        self.thin_characters = ['l', 't', 'i', 'f', '.', ',', "'"]

        self.char_to_num = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8,
            'i': 9,
            'j': 10,
            'k': 11,
            'l': 12,
            'm': 13,
            'n': 14,
            'o': 15,
            'p': 16,
            'q': 17,
            'r': 18,
            's': 19,
            't': 20,
            'u': 21,
            'v': 22,
            'w': 23,
            'x': 24,
            'y': 25,
            'z': 26,
            '.': 27,
            ',': 28,
            "'": 29,
            ':': 30,
            'A': 31,
            'B': 32,
            'C': 33,
            'D': 34,
            'E': 35,
            'F': 36,
            'G': 37,
            'H': 38,
            'I': 39,
            'J': 40,
            'K': 41,
            'L': 42,
            'M': 43,
            'N': 44,
            'O': 45,
            'P': 46,
            'Q': 47,
            'R': 48,
            'S': 49,
            'T': 50,
            'U': 51,
            'V': 52,
            'W': 53,
            'X': 54,
            'Y': 55,
            'Z': 56,
            '1': 57,
            '2': 58,
            '3': 59,
            '4': 60,
            '5': 61,
            '6': 62,
            '7': 63,
            '8': 64,
            '9': 65,
            '0': 66,
            '?': 67,
            '#': 68,
            '[': 69,
            ']': 70,
            '(': 71,
            ')': 72,
            '!': 73,
            '-': 74,
            '+': 75
        }

    def make_text(self, text):
        for line in text:
            chars = list(line)
            self.num_of_chars = 0
            self.num_of_lines += 1
            self.char_x = 0
            for char in chars:
                self.num_of_chars += 1
                if char != ' ':
                    char_num = self.char_to_num[char]
                    char_img = self.characters[char_num - 1]
                    if char in self.thin_characters:
                        char_len = 3
                    else:
                        char_len = 5

                    character = [char_img, self.char_x, self.char_y]
                    self.ready_characters.append(character)

                    self.char_x += (char_len + self.char_spacing)

                else:
                    self.char_x += self.space

            self.char_y += 11

            if self.char_x > self.longest_line:
                self.longest_line = self.char_x

        surface_dimentions = (self.longest_line, self.char_y)
        text_surface = pygame.Surface(surface_dimentions).convert()
        for char in self.ready_characters:
            img = char[0]
            x = char[1]
            y = char[2]
            text_surface.blit(img, (x, y))

        text_surface.set_colorkey((0, 0, 0))

        return text_surface


