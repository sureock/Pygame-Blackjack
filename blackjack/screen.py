import menu
import pygame

pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

pygame.init()

music = pygame.mixer.music
music.load("Play Roulette.mp3")
music.play(loops=-1)

menu.start()
