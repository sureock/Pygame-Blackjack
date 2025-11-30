import pygame

width, height = 1000, 750
fps = 24
white = (255,255,255)
black = (0,0,0)

def start():
    global running
    global setup
    global play
    button_surface = pygame.Surface((250,50))
    screen = pygame.display.set_mode((width,height))
    pygame.font.match_font('font.otf')
    font_name = pygame.font.Font('font.otf',32)
    font_setup = pygame.font.Font('font.otf',20)
    clock = pygame.time.Clock()

    text = font_name.render("SETUP",True,white)
    text_rect = text.get_rect()
    text_rect.topleft = (50,50)

    text_1 = font_setup.render("Sound Volume",True,white)
    text_1_rect = text_1.get_rect()
    text_1_rect.topleft =(100,400)
    button_1_rect = pygame.Rect(90,400,120,50)

    text_2 = font_setup.render("Deck Back View",True,white)
    text_2_rect = text_2.get_rect()
    text_2_rect.topleft =(100,465)
    button_2_rect = pygame.Rect(90,465,120,50)

    text_3 = font_setup.render("BACK",True,white)
    text_3_rect = text_3.get_rect()
    text_3_rect.topleft =((width-90)//2,685)
    button_3_rect = pygame.Rect(
        (width - 120)//2,675,120,50)

    setup = True
    while setup:
        dt = clock.tick(fps)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setup = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_3_rect.collidepoint(event.pos):
                    setup = False
                    running = True
                    play = False

        screen.blit(text, text_rect)
        screen.blit(button_surface,(button_1_rect.x, button_1_rect.y))
        screen.blit(button_surface,(button_2_rect.x, button_2_rect.y))
        screen.blit(button_surface,(button_3_rect.x, button_3_rect.y))
        screen.blit(text_1,text_1_rect)
        screen.blit(text_2,text_2_rect)
        screen.blit(text_3,text_3_rect)
        pygame.display.update()
    return(running,setup,play)