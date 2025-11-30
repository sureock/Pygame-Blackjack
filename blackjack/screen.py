import menu
import setups
import pygame

pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

pygame.init()

running = True
setup = False
play = False
while running or setup or play:
    if running:
        running, setup, play = menu.start()
    elif setup:
        running, setup, play = setups.start()




