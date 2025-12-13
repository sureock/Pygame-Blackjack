import pygame


class Text:

    def __init__(self, text, screen_size, logo=False):

        def get_relative_width(x, y):
            return x * y

        def get_relative_height(x, y):
            return x * y

        def scale(x, y):
            return pygame.transform.scale(x, y)

        self.width = screen_size[0]
        self.height = screen_size[1]

        self.width_relative = self.width / 1000
        self.height_relative = self.height / 750

        self.text = text
        self.text_width = text.get_size()[0]
        self.text_height = text.get_size()[1]

        if logo:
            self.text_width = self.text_width // 2
            self.text_height = self.text_height // 2

        self.text_scale = scale(text,
                                (get_relative_width(self.text_width,
                                                    self.width_relative),
                                 get_relative_height(self.text_height,
                                                     self.height_relative)
                                 ))
        self.text_rect = self.text_scale.get_rect()
        self.topleft_param = ((
            self.width - get_relative_width(self.text_width,
                                            self.width_relative)) // 2,
                              20)
        self.text_rect.topleft = self.topleft_param

        self.button_rect = pygame.Rect(self.topleft_param[0],
                                       self.topleft_param[1],
                                       get_relative_width(
                                            self.text_width,
                                            self.width_relative),
                                       get_relative_height(
                                            self.text_height,
                                            self.height_relative))

    def resize(self, new_param):

        def get_relative_width(x, y):
            return x * y

        def get_relative_height(x, y):
            return x * y

        self.resize_param = new_param

        self.topleft_param = ((self.width - get_relative_width(self.text_width,
                                                               self.width_relative)) // 2,
                              self.height - get_relative_height(new_param,
                                                                self.height_relative))

        self.text_rect.topleft = self.topleft_param

        self.button_rect = pygame.Rect(self.topleft_param[0],
                                       self.topleft_param[1],
                                       get_relative_width(
                                            self.text_width,
                                            self.width_relative),
                                       get_relative_height(
                                            self.text_height,
                                            self.height_relative))
