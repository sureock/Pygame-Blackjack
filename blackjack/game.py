import pygame

width, height = 1000, 750
fps = 24

white = (255,255,255)
black = (0,0,0)

pygame.init()

button_surface = pygame.Surface((250,50))

screen = pygame.display.set_mode((width,height))
pygame.font.match_font('font.otf')
font = pygame.font.Font('font.otf',24)
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

text = pygame.image.load('2(900x270).png').convert_alpha()
text_rect = text.get_rect()
text_rect.topleft = ((width - 900)//2,20)

text_1 = font.render("PLAY",True,white)
text_1_rect = text_1.get_rect()
text_1_rect.topleft =((width-90)//2,535)
button_1_rect = pygame.Rect(
    (width - 120)//2,525,120,50)

text_2 = font.render("SETUP",True,white)
text_2_rect = text_2.get_rect()
text_2_rect.topleft =((width-120)//2,610)
button_2_rect = pygame.Rect(
    (width - 120)//2,600,120,50)

text_3 = font.render("EXIT",True,white)
text_3_rect = text_3.get_rect()
text_3_rect.topleft =((width-90)//2,685)
button_3_rect = pygame.Rect(
    (width - 120)//2,675,120,50)

running = True
while running:
    dt = clock.tick(fps)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_1_rect.collidepoint(event.pos):
                ...
            if button_2_rect.collidepoint(event.pos):
                ...
            if button_3_rect.collidepoint(event.pos):
                running = False

    screen.blit(text, text_rect)
    screen.blit(button_surface,(button_1_rect.x, button_1_rect.y))
    screen.blit(button_surface,(button_2_rect.x, button_2_rect.y))
    screen.blit(button_surface,(button_3_rect.x, button_3_rect.y))
    screen.blit(text_1,text_1_rect)
    screen.blit(text_2,text_2_rect)
    screen.blit(text_3,text_3_rect)
    pygame.display.update()
pygame.quit()
