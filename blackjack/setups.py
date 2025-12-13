import pygame
import utils
import menu
# import pygame_scrollbar

fps = 24
white = (255, 255, 255)
gray = (25, 25, 25)


def start():

    button_surface = pygame.Surface((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    width_relative = width/1000
    height_relative = height/750
    pygame.font.match_font('font.otf')
    font_name = pygame.font.Font('font.otf', 32)
    font_setup = pygame.font.Font('font.otf', 18)
    # clock = pygame.time.Clock()

    tname = font_name.render("SETUP", True, white)
    text_name = utils.Text(tname,
                           screen.get_size(),
                           (20 * width_relative, 20 * height_relative))
    tname_height = tname.get_size()[1]

    t1 = font_setup.render("Sound Volume", True, white)
    add_height = tname_height + 200
    text_1 = utils.Text(t1,
                        screen.get_size(),
                        (25 * width_relative, add_height * height_relative))

    t2 = font_setup.render("Deck Back View", True, white)
    add_height_1 = add_height + t1.get_size()[1] + 25
    text_2 = utils.Text(t2,
                        screen.get_size(),
                        (25 * width_relative, add_height_1 * height_relative))

    t3 = font_setup.render("BACK", True, white)
    t3_width, t3_height = t3.get_size()
    text_3 = utils.Text(t3,
                        screen.get_size(),
                        ((width - t3_width * width_relative) // 2,
                         (height - (t3_height + 10) * height_relative)))
    button_3_rect = pygame.Rect((width - t3_width * width_relative) // 2,
                                (height - (t3_height + 10) * height_relative),
                                t3_width * width_relative,
                                t3_height * height_relative)

    setup = True
    while setup:
        # dt = clock.tick(fps)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setup = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_3_rect.collidepoint(event.pos):
                    menu.start()

        screen.fill(gray)
        screen.blit(text_name.text_scale, text_name.text_rect)
        # screen.blit(button_surface,(button_1_rect.x, button_1_rect.y))
        # screen.blit(button_surface,(button_2_rect.x, button_2_rect.y))
        screen.blit(button_surface, (button_3_rect.x, button_3_rect.y))
        screen.blit(text_1.text_scale, text_1.text_rect)
        screen.blit(text_2.text_scale, text_2.text_rect)
        screen.blit(text_3.text_scale, text_3.text_rect)
        pygame.display.update()
