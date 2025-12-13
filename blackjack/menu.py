import pygame
import game
import setups
from utils import widgets

fps = 24
white = (255, 255, 255)
gray = (25, 25, 25)


def start():

    pygame.mixer.music.load("Play Roulette.mp3")
    pygame.mixer.music.play()

    button_surface = pygame.Surface((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.font.match_font('font.otf')
    font = pygame.font.Font('font.otf', 20)

    text_name = widgets.Text(pygame.image.load('logo.png').convert_alpha(),
                             screen.get_size(),
                             True)

    text_3 = widgets.Text(font.render("EXIT", True, white),
                          screen.get_size())
    text_3.resize(text_3.text_height + 10)

    text_2 = widgets.Text(font.render("SETUP", True, white),
                          screen.get_size())
    text_2.resize(text_3.resize_param + text_2.text_height + 5)

    text_1 = widgets.Text(font.render("PLAY", True, white),
                          screen.get_size())
    text_1.resize(text_2.resize_param + text_1.text_height + 5)

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
