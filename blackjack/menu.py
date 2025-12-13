import pygame
import game
import setups
import utils

fps = 24
white = (255, 255, 255)
gray = (25, 25, 25)


def start():

    pygame.mixer.music.load("Play Roulette.mp3")
    pygame.mixer.music.play()

    button_surface = pygame.Surface((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.font.match_font('font.otf')
    font = pygame.font.Font('font.otf', 20)

    tname = pygame.image.load('logo.png').convert_alpha()
    text_name = utils.Text(tname,
                           screen.get_size(),
                           ((width - (tname.get_size()[0] // 2) * (width / 1000)) // 2,
                            40),
                           True)

    t3 = font.render("EXIT", True, white)
    t3_param = t3.get_size()[1] + 10
    text_3 = utils.Text(t3,
                        screen.get_size(),
                        ((width - t3.get_size()[0] * (width / 1000)) // 2,
                         height - t3_param * height / 750))

    t2 = font.render("SETUP", True, white)
    t2_param = t3_param + t2.get_size()[1] + 5
    text_2 = utils.Text(t2,
                        screen.get_size(),
                        ((width - t2.get_size()[0] * width / 1000) // 2,
                         height - t2_param * height / 750))

    t1 = font.render("PLAY", True, white)
    t1_param = t2_param + t1.get_size()[1] + 5
    text_1 = utils.Text(t1,
                        screen.get_size(),
                        ((width - t1.get_size()[0] * width / 1000) // 2,
                         height - t1_param * height / 750))

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
