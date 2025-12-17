import menu
import pygame
import parse
import bdclass

def call_game(name):
    pygame.display.set_caption('Blackjack')
    clock = pygame.time.Clock()

    pygame.init()

    music = pygame.mixer.music
    music.load("Play Roulette.mp3")
    music.play(loops=-1)

    menu.start(name)

name, password = parse.get_args()
auth = bdclass.Auth(name, password)

text, result = auth.login()
print(text)
if not result:
    text, result = auth.regist()
    print(text)
    if result:
        call_game(name)
else:
    call_game(name)
