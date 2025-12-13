import pygame
import game
import setups

fps = 24
white = (255, 255, 255)
gray = (25, 25, 25)


def start():

    button_surface = pygame.Surface((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    width_relative = width / 1000
    height_relative = height / 750
    pygame.font.match_font('font.otf')
    font = pygame.font.Font('font.otf', 20)

    def get_relative_width(x):
        return x * width_relative

    def get_relative_height(x):
        return x * height_relative

    def scale(x, y):
        return pygame.transform.scale(x, y)

    class Text:
        def __init__(self, text, logo=False):
            self.text = text
            self.text_width = text.get_size()[0]
            self.text_height = text.get_size()[1]

            if logo:
                self.text_width = self.text_width // 2
                self.text_height = self.text_height // 2

            self.text_scale = scale(text,
                                    (get_relative_width(self.text_width),
                                     get_relative_height(self.text_height)
                                     ))
            self.text_rect = self.text_scale.get_rect()
            self.topleft_param = ((
                width - get_relative_width(self.text_width)) // 2,
                                  20)
            self.text_rect.topleft = self.topleft_param

            self.button_rect = pygame.Rect(self.topleft_param[0],
                                           self.topleft_param[1],
                                           get_relative_width(
                                               self.text_width),
                                           get_relative_height(
                                               self.text_height))

        def resize(self, new_param):
            self.resize_param = new_param

            self.topleft_param = ((
                width - get_relative_width(self.text_width)) // 2,
                                  height - get_relative_height(new_param))

            self.text_rect.topleft = self.topleft_param

            self.button_rect = pygame.Rect(self.topleft_param[0],
                                           self.topleft_param[1],
                                           get_relative_width(
                                               self.text_width),
                                           get_relative_height(
                                               self.text_height))

    text_name = Text(pygame.image.load('logo.png').convert_alpha(), True)

    text_3 = Text(font.render("EXIT", True, white))
    text_3.resize(text_3.text_height + 10)

    text_2 = Text(font.render("SETUP", True, white))
    text_2.resize(text_3.resize_param + text_2.text_height + 5)

    text_1 = Text(font.render("PLAY", True, white))
    text_1.resize(text_2.resize_param + text_1.text_height + 5)

    pygame.mixer.music.load("Play Roulette.mp3")
    pygame.mixer.music.play()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if text_1.button_rect.collidepoint(event.pos):
                    game.start()
                if text_2.button_rect.collidepoint(event.pos):
                    setups.start()
                if text_3.button_rect.collidepoint(event.pos):
                    pygame.quit()

        screen.fill(gray)
        screen.blit(text_name.text_scale, text_name.text_rect)
        screen.blit(button_surface,
                    (text_1.button_rect.x, text_1.button_rect.y))
        screen.blit(button_surface,
                    (text_2.button_rect.x, text_2.button_rect.y))
        screen.blit(button_surface,
                    (text_3.button_rect.x, text_3.button_rect.y))
        screen.blit(text_1.text_scale, text_1.text_rect)
        screen.blit(text_2.text_scale, text_2.text_rect)
        screen.blit(text_3.text_scale, text_3.text_rect)
        pygame.display.update()
