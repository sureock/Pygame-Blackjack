import pygame
import sys
import gc
from deck import deck52
from utils import CardAnimation, calculate_score, card_load, Button
import menu

clock = pygame.time.Clock()
fps = 60
white = (255, 255, 255)
gray = (25, 25, 25)
razmer_def = (63, 89)
deck_image = pygame.image.load('deck1.jpg')
scaled_deck = pygame.transform.scale_by(deck_image, 2)
# загрузка карт
cards = card_load()


def start():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption('blackjack')
    clock = pygame.time.Clock()

    # Создаём объект колоды
    deck = deck52()

    DILER = 0
    PLAYER = 0

    player_hand = []
    dealer_hand = []

    # Списки для анимаций карт
    player_card_animations = []
    dealer_card_animations = []

    # Позиция колоды (стартовая позиция для всех карт)
    deck_pos = (WIDTH - 200, HEIGHT // 2)

    winner_text = ""  # текст победителя
    game_started = False
    game_over = True

    start_button = Button(50, HEIGHT - 120, 200, 60, "Начать игру")
    card_button = Button(WIDTH // 2 - 100,
                                 HEIGHT - 160, 200, 60, "Взять карту")
    pass_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 60, "Пас",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    exit_button = Button(WIDTH - 250, HEIGHT - 120, 200, 60, "Выход",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    start_again_button = Button(50, HEIGHT - 120, 200, 60, "Начать заново")

    # Шрифты
    font = pygame.font.Font('font.otf', 30)
    # card_font = pygame.font.Font('font.otf', 15)

    def draw_player():
        suit, (rank, value) = deck.draw()
        card_data = (suit, rank, value)
        player_hand.append(card_data)

        # Создаем анимацию для новой карты
        target_x = 50 + (len(player_hand) - 1) * 150
        target_y = 50
        anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
        player_card_animations.append(anim)

    def draw_dealer():
        suit, (rank, value) = deck.draw()
        card_data = (suit, rank, value)
        dealer_hand.append(card_data)

        # Создаем анимацию для карты дилера (скрываем первую)
        target_x = 50 + len(dealer_card_animations) * 200
        target_y = 150
        anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
        dealer_card_animations.append(anim)

    

    running = True
    while running:
        dt = clock.tick(fps) / 1000
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            # --- Начать игру / Начать заново ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked(mouse_pos, True) and game_over:
                    game_started = True
                    game_over = False
                    winner_text = ""
                    player_hand.clear()
                    dealer_hand.clear()
                    player_card_animations.clear()
                    dealer_card_animations.clear()
                    PLAYER = 0
                    DILER = 0
                    deck.shuffle()

                    for i in range(2):
                        # Карта игроку
                        draw_player()

                        # Карта дилеру
                        draw_dealer()

                    # Обновляем счет после добавления всех карт
                    PLAYER = calculate_score(player_hand)
                    DILER = calculate_score(dealer_hand)

                # --- Игрок берёт карту ---
                if card_button.is_clicked(mouse_pos, True) and not game_over:
                    draw_player()

                    PLAYER = calculate_score(player_hand)

                    if PLAYER > 21:
                        winner_text = "Дилер выиграл!"
                        game_over = True

                # --- Игрок пасует ---
                if pass_button.is_clicked(mouse_pos, True) and not game_over:
                    while DILER < 16:
                        draw_dealer()

                        DILER = calculate_score(dealer_hand)
                    game_over = True

                    if DILER > 21:
                        winner_text = "Игрок выиграл!"

                    elif DILER > PLAYER and game_over:
                        winner_text = "Дилер выиграл!"

                    if DILER == PLAYER and game_over:
                        winner_text = "Ничья!"

                    if DILER < PLAYER and game_over:
                        winner_text = "Игрок победил!"

                # --- Выход ---
                if exit_button.is_clicked(mouse_pos, True):
                    running = False
                    return

        screen.fill(gray)

        # Рисуем колоду
        screen.blit(scaled_deck, deck_pos)

        # Анимации карт игрока
        for anim in player_card_animations:
            if not anim.reached:
                anim.update(dt)

        # Анимации карт дилера
        for anim in dealer_card_animations:
            if not anim.reached:
                anim.update(dt)

        # Карты игрока (отрисовываем с анимацией)
        for i, anim in enumerate(player_card_animations):
            # Создаем поверхность для карты
            card_surface = pygame.Surface(razmer_def)
            card_surface = pygame.transform.scale_by(card_surface, 2)
            pygame.draw.rect(card_surface, (0, 0, 0), (0, 0, 126, 178), 2)

            # изображение карты
            if i < len(player_hand):
                suit, rank, value = player_hand[i]
                image = pygame.image.load(cards[(suit, rank)])
                scaled_image = pygame.transform.scale_by(image, 2)
                card_surface.blit(scaled_image, (0, 0))

            # Рисуем карту в текущей позиции анимации
            screen.blit(card_surface, anim.current_pos)

        # Очки игрока
        score_text = font.render(f"Очки игрока: {PLAYER}", True, white)
        screen.blit(score_text, (50, 250))

        # Карты дилера (отрисовываем с анимацией)
        for i, anim in enumerate(dealer_card_animations):
            # Создаем поверхность для карты
            card_surface = pygame.Surface(razmer_def)
            card_surface = pygame.transform.scale_by(card_surface, 2)

            # Первая карта дилера скрыта до конца игры
            if i == 0 and not game_over and game_started:
                pygame.draw.rect(card_surface, (0, 0, 0), (0, 0, 126, 178), 2)
                card_surface.blit(scaled_deck, (0, 0))
            else:
                pygame.draw.rect(card_surface, (0, 0, 0), (0, 0, 126, 178), 2)

                if i < len(dealer_hand):
                    suit, rank, value = dealer_hand[i]
                    image = pygame.image.load(cards[(suit, rank)])
                    scaled_image = pygame.transform.scale_by(image, 2)
                    card_surface.blit(scaled_image, (0, 0))

            # Рисуем карту в текущей позиции анимации
            screen.blit(card_surface, anim.current_pos)

        # Очки дилера (показываем только после паса или если игрок проиграл)
        dealer_text = f"Очки дилера: {DILER if game_over else '??'}"
        dealer_score_text = font.render(dealer_text, True, white)
        screen.blit(dealer_score_text, (50, 450))

        if winner_text:
            winner_render = font.render(winner_text, True, (255, 255, 0))
            screen.blit(winner_render,
                        (WIDTH // 2 - winner_render.get_width() // 2,
                         HEIGHT // 2))

        exit_button.draw(screen)
        if not game_started:
            start_button.draw(screen)

        # Кнопки "Взять карту" и "Пас" активны только во время игры
        if game_started and not game_over:
            card_button.draw(screen)
            pass_button.draw(screen)
        if game_started and game_over:
            start_again_button.draw(screen)


        pygame.display.flip()
    pygame.quit()