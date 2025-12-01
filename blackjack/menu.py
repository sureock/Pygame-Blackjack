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
    font = pygame.font.Font('font.otf',20)
    clock = pygame.time.Clock()

    text_name = pygame.image.load('logo.png').convert_alpha()
    text_name_width, text_name_height = text_name.get_size()
    scale_text_name = pygame.transform.scale(text_name,(text_name_width*width_relative//2,text_name_height*height_relative//2))
    text_rect = scale_text_name.get_rect()
    text_rect.topleft = ((width - text_name_width*width_relative//2)//2,20)

    text_3 = font.render("EXIT",True,white)
    text_3_width, text_3_height = text_3.get_size()
    scale_text_3 = pygame.transform.scale(text_3,(text_3_width*width_relative,text_3_height*height_relative))
    text_3_rect = scale_text_3.get_rect()
    text_3_rect.topleft =((width-text_3_width*width_relative)//2,(height-(text_3_height+10)*height_relative))
    button_3_rect = pygame.Rect((width-text_3_width*width_relative)//2,(height-(text_3_height+10)*height_relative),
                                text_3_width*width_relative,text_3_height*height_relative)

    text_2 = font.render("SETUP",True,white)
    text_2_width, text_2_height = text_2.get_size()
    scale_text_2 = pygame.transform.scale(text_2,(text_2_width*width_relative,text_2_height*height_relative))
    text_2_rect = text_2.get_rect()
    text_2_rect.topleft =((width-text_2_width*width_relative)//2,(height-(text_3_height+10+text_2_height+5)*height_relative))
    button_2_rect = pygame.Rect((width-text_2_width*width_relative)//2,(height-(text_3_height+10+text_2_height+5)*height_relative),
                                text_2_width*width_relative,text_2_height*height_relative)

    text_1 = font.render("PLAY",True,white)
    text_1_width, text_1_height = text_1.get_size()
    scale_text_1 = pygame.transform.scale(text_1,(text_1_width*width_relative,text_1_height*height_relative))
    text_1_rect = scale_text_1.get_rect()
    text_1_rect.topleft =((width-text_1_width*width_relative)//2,(height-(text_3_height+10+text_2_height+5+text_1_height+5)*height_relative))
    button_1_rect = pygame.Rect((width-text_1_width*width_relative)//2,height-((text_3_height+10+text_2_height+5+text_1_height+5)*height_relative),
                                text_1_width*width_relative,text_1_height*height_relative)

    running = True
    while running:
        dt = clock.tick(fps)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_1_rect.collidepoint(event.pos):
                    play = True
                    running = False
                    setup = False
                if button_2_rect.collidepoint(event.pos):
                    setup = True
                    running = False
                    play = False
                if button_3_rect.collidepoint(event.pos):
                    running = False
                    setup = False
                    play = False

        screen.fill(gray)
        screen.blit(scale_text_name, text_rect)
        screen.blit(button_surface,(button_1_rect.x, button_1_rect.y))
        screen.blit(button_surface,(button_2_rect.x, button_2_rect.y))
        screen.blit(button_surface,(button_3_rect.x, button_3_rect.y))
        screen.blit(scale_text_1,text_1_rect)
        screen.blit(scale_text_2,text_2_rect)
        screen.blit(scale_text_3,text_3_rect)
        pygame.display.update()
    return(running,setup,play)
