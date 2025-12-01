import pygame

fps = 24
white = (255,255,255)
gray = (25,25,25)

def start():
    button_surface = pygame.Surface((0,0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    width_relative = width/1000
    height_relative = height/750 
    pygame.font.match_font('font.otf')
    font_name = pygame.font.Font('font.otf',32)
    font_setup = pygame.font.Font('font.otf',18)
    clock = pygame.time.Clock()

    text_name = font_name.render("SETUP",True,white)
    text_name_width, text_name_height = text_name.get_size()
    scale_text_name = pygame.transform.scale(text_name,(text_name_width*width_relative,text_name_height*height_relative))
    text_name_rect = scale_text_name.get_rect()
    text_name_rect.topleft =(20*width_relative,20*height_relative)

    text_1 = font_setup.render("Sound Volume",True,white)
    text_1_width, text_1_height = text_1.get_size()
    scale_text_1 = pygame.transform.scale(text_1,(text_1_width*width_relative,text_1_height*height_relative))
    text_1_rect = scale_text_1.get_rect()
    text_1_rect.topleft =(25*width_relative,((text_name_height+200)*height_relative))

    text_2 = font_setup.render("Deck Back View",True,white)
    text_2_width, text_2_height = text_2.get_size()
    scale_text_2 = pygame.transform.scale(text_2,(text_2_width*width_relative,text_2_height*height_relative))
    text_2_rect = text_2.get_rect()
    text_2_rect.topleft =(25*width_relative,(text_name_height+200+text_1_height+25)*height_relative)
    # button_2_rect = pygame.Rect(90,465,120,50)

    text_3 = font_setup.render("BACK",True,white)
    text_3_width, text_3_height = text_3.get_size()
    scale_text_3 = pygame.transform.scale(text_3,(text_3_width*width_relative,text_3_height*height_relative))
    text_3_rect = scale_text_3.get_rect()
    text_3_rect.topleft =((width-text_3_width*width_relative)//2,(height-(text_3_height+10)*height_relative))
    button_3_rect = pygame.Rect((width-text_3_width*width_relative)//2,(height-(text_3_height+10)*height_relative),
                                text_3_width*width_relative,text_3_height*height_relative)

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

        screen.fill(gray)
        screen.blit(scale_text_name, text_name_rect)
        # screen.blit(button_surface,(button_1_rect.x, button_1_rect.y))
        # screen.blit(button_surface,(button_2_rect.x, button_2_rect.y))
        screen.blit(button_surface,(button_3_rect.x, button_3_rect.y))
        screen.blit(scale_text_1,text_1_rect)
        screen.blit(scale_text_2,text_2_rect)
        screen.blit(scale_text_3,text_3_rect)
        pygame.display.update()
    return(running,setup,play)
