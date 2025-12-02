import pygame
from deck import deck52
import sys
import menu
fps = 24
white = (255,255,255)
gray = (25,25,25)


class Button:
    def __init__(self, x, y, width, height, text,
                 color=(200, 200, 200), hover_color=(170, 170, 170), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 36)
        self.active = True

    def draw(self, surface):
        if not self.active:
            return
        mouse_pos = pygame.mouse.get_pos()

        # меняем цвет при наведении
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # рисуем текст
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, clicked):
        return self.rect.collidepoint(mouse_pos) and clicked

def calculate_score(hand):
    total = 0
    aces = 0

    for suit, rank, value in hand:
        if rank == "Ace":
            aces += 1
            total += 1
        else:
            total += value


    if aces > 0 and total + 10 <= 21:
        total += 10

    return total



def start():

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption('blackjack')
    clock = pygame.time.Clock()

    # Создаём объект колоды
    deck = deck52()
    deck.shuffle()

    DILER = 0
    PLAYER = 0

    player_hand = []
    dealer_hand = []

    winner_text = ""  # текст победителя
    game_started = False
    game_over = False

    start_button = Button(50, HEIGHT - 120, 200, 60, "Начать игру")
    issue_a_card_button = Button(WIDTH // 2 - 100, HEIGHT - 160, 200, 60, "Взять карту")
    pass_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 60, "Пас",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    exit_button = Button(WIDTH - 250, HEIGHT - 120, 200, 60, "Выход",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    start_again_button = Button(50, HEIGHT - 120, 200, 60, "Начать заново")
    running = True
    while running:
            dt = clock.tick(fps) / 1000
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # --- Начать игру / Начать заново ---
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.is_clicked(mouse_pos, True):
                        game_started  = True
                        winner_text = ""
                        player_hand.clear()
                        dealer_hand.clear()
                        PLAYER = 0
                        DILER = 0
                        deck.shuffle()

                        for  i in range(2):
                            suit, (rank, value) = deck.draw()
                            player_hand.append((suit, rank, value))
                            PLAYER = calculate_score(player_hand)
                            suit, (rank, value) = deck.draw()
                            dealer_hand.append((suit, rank, value))
                            DILER = calculate_score(dealer_hand)

                    # --- Игрок берёт карту ---
                    if game_started and not game_over and issue_a_card_button.is_clicked(mouse_pos, True):
                        suit, (rank, value) = deck.draw()
                        player_hand.append((suit, rank, value))
                        PLAYER = calculate_score(player_hand)

                    if PLAYER > 21:
                        winner_text = "Дилер выиграл!"
                        game_over  = True




                    # --- Игрок пасует ---
                    if game_started and not game_over and pass_button.is_clicked(mouse_pos, True):
                        while DILER < 16:
                            suit, (rank, value) = deck.draw()
                            dealer_hand.append((suit, rank, value))
                            DILER = calculate_score(dealer_hand)
                        game_over = True


                    if DILER > 21:
                        winner_text = "Игрок выиграл!"


                    if DILER > PLAYER and game_over == True and pass_button.is_clicked(mouse_pos, True):
                        winner_text = "Дилер выиграл!"


                    elif DILER > PLAYER and game_over == False and pass_button.is_clicked(mouse_pos, False):
                        winner_text = ""

                    if DILER == PLAYER and game_over == True and pass_button.is_clicked(mouse_pos, True):
                        winner_text = "Ничья!"


                    elif DILER == PLAYER and game_over == False and pass_button.is_clicked(mouse_pos, False):
                        winner_text = ""

                    if DILER < PLAYER and game_over == True and pass_button.is_clicked(mouse_pos, True):
                        winner_text = "Игрок победил!"


                    elif DILER < PLAYER and game_over == False and pass_button.is_clicked(mouse_pos, False):
                        winner_text = ""





                    if start_again_button.is_clicked(mouse_pos, True) and game_started == True:
                            player_hand.clear()
                            dealer_hand.clear()
                            game_over = False
                            PLAYER = 0
                            DILER = 0
                            deck.shuffle()

                            for i in range(2):
                                suit, (rank, value) = deck.draw()
                                player_hand.append((suit, rank, value))
                                PLAYER = calculate_score(player_hand)
                                suit, (rank, value) = deck.draw()
                                dealer_hand.append((suit, rank, value))
                                DILER = calculate_score(dealer_hand)

                    # --- Выход ---
                    if exit_button.is_clicked(mouse_pos, True):

                        running = False
                        return True, False, False


            screen.fill(gray)

            font = pygame.font.SysFont(None, 48)


            # Карты игрока
            x = 50
            y = 50
            for suit, rank, value in player_hand:
                card_text = f"{rank} {suit}"
                text = font.render(card_text, True, (0, 0, 0))
                screen.blit(text, (x, y))
                x += 150

            # Очки игрока
            score_text = font.render(f"Очки игрока: {PLAYER}", True, (255, 255, 255))
            screen.blit(score_text, (50, 120))

            # Карты дилера
            x = 50
            y = 150
            for suit, rank, value in dealer_hand:
                card_text = f"{rank} {suit}"
                text = font.render(card_text, True, (0, 0, 0))
                screen.blit(text, (x, y))
                x += 200

                # Очки дилера
                dealer_score_text = font.render(f"Очки дилера: {DILER}", True, (255, 255, 255))
                screen.blit(dealer_score_text, (50, 220))

            if winner_text:
                winner_render = font.render(winner_text, True, (255, 255, 0))
                screen.blit(winner_render, (WIDTH // 2 - winner_render.get_width() // 2, HEIGHT // 2))



            # --- Кнопки ---
            # Кнопка "Начать игру" показывается только если игра не началась или закончилась
            # управление доступностью
            start_button.active = not game_started
            if game_started == True and game_over == False:
                issue_a_card_button.active = True
                pass_button.active = True
            if game_started == True and game_over == True:
                start_again_button.active = True
            exit_button.active = True

            exit_button.draw(screen)
            if game_started == False:
                    start_button.draw(screen)


                # Кнопки "Взять карту" и "Пас" активны только во время игры
            if game_started== True and game_over == False:
                    issue_a_card_button.draw(screen)
                    pass_button.draw(screen)
            if game_started == True and game_over == True:
                    start_again_button.draw(screen)

            pygame.display.flip()
    return True, False, False
