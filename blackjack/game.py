import pygame

width, height = 1000, 750
fps = 24

white = (255,255,255)
blue = (50,150,255)
black = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

text_rect = pygame.Rect(
    (width - 750)//2,
    20, 750, 150)

button_1_rect = pygame.Rect(
    (width - 500)//2,
    525,500,50)

button_2_rect = pygame.Rect(
    (width - 500)//2,
    600,500,50)

button_3_rect = pygame.Rect(
    (width - 500)//2,
    675,500,50)

running = True
while running:
    dt = clock.tick(fps)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    pygame.draw.rect(screen, white, text_rect)
    pygame.draw.rect(screen, blue, button_1_rect)
    pygame.draw.rect(screen, blue, button_2_rect)
    pygame.draw.rect(screen, blue, button_3_rect)
    pygame.display.flip()
pygame.quit()
