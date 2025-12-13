import pygame
from deck import deck52
from utils import CardAnimation, calculate_score, card_load

clock = pygame.time.Clock()
fps = 60
white = (255, 255, 255)
gray = (25, 25, 25)
razmer_def = (63, 89)
deck_image = pygame.image.load('deck1.jpg')
scaled_deck = pygame.transform.scale_by(deck_image, 2)
# загрузка карт
cards = card_load()


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

    # Списки для анимаций карт
    player_card_animations = []
    dealer_card_animations = []

    # Позиция колоды (стартовая позиция для всех карт)
    deck_pos = (WIDTH - 200, HEIGHT // 2)

    winner_text = ""  # текст победителя
    game_started = False
    game_over = False

    # Флаг, указывающий, что нужно начать анимацию раздачи
    animate_deal = False

    start_button = Button(50, HEIGHT - 120, 200, 60, "Начать игру")
    issue_a_card_button = Button(WIDTH // 2 - 100, HEIGHT - 160, 200, 60, "Взять карту")
    pass_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 60, "Пас",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    exit_button = Button(WIDTH - 250, HEIGHT - 120, 200, 60, "Выход",
                         color=(255, 100, 100), hover_color=(255, 150, 150))
    start_again_button = Button(50, HEIGHT - 120, 200, 60, "Начать заново")

    # Шрифты
    font = pygame.font.Font('font.otf', 30)
    card_font = pygame.font.Font('font.otf', 15)

    running = True
    while running:
        dt = clock.tick(fps) / 1000
        mouse_pos = pygame.mouse.get_pos()
        # mouse_pressed = pygame.mouse.get_pressed()[0]
        # current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # --- Начать игру / Начать заново ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked(mouse_pos, True) and not game_started:
                    game_started = True
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
                        suit, (rank, value) = deck.draw()
                        card_data = (suit, rank, value)
                        player_hand.append(card_data)

                        # Создаем анимацию для карты игрока
                        target_x = 50 + len(player_card_animations) * 150
                        target_y = 50
                        anim = CardAnimation(card_data, (target_x, target_y), deck_pos, speed=400)
                        player_card_animations.append(anim)

                        # Карта дилеру
                        suit, (rank, value) = deck.draw()
                        card_data = (suit, rank, value)
                        dealer_hand.append(card_data)

                        # Создаем анимацию для карты дилера (скрываем первую)
                        target_x = 50 + len(dealer_card_animations) * 200
                        target_y = 150
                        anim = CardAnimation(card_data, (target_x, target_y), deck_pos, speed=400)
                        dealer_card_animations.append(anim)

                    # Обновляем счет после добавления всех карт
                    PLAYER = calculate_score(player_hand)
                    DILER = calculate_score(dealer_hand)
                    animate_deal = True

                # --- Игрок берёт карту ---
                if game_started and not game_over and issue_a_card_button.is_clicked(mouse_pos, True):
                    suit, (rank, value) = deck.draw()
                    card_data = (suit, rank, value)
                    player_hand.append(card_data)

                    # Создаем анимацию для новой карты
                    target_x = 50 + (len(player_hand) - 1) * 150
                    target_y = 50
                    anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
                    player_card_animations.append(anim)

                    PLAYER = calculate_score(player_hand)

                    if PLAYER > 21:
                        winner_text = "Дилер выиграл!"
                        game_over = True

                # --- Игрок пасует ---
                if game_started and not game_over and pass_button.is_clicked(mouse_pos, True):
                    while DILER < 16:
                        suit, (rank, value) = deck.draw()
                        card_data = (suit, rank, value)
                        dealer_hand.append(card_data)

                        # Создаем анимацию для новой карты дилера
                        target_x = 50 + (len(dealer_hand) - 1) * 200
                        target_y = 150
                        anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
                        dealer_card_animations.append(anim)

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
                    player_card_animations.clear()
                    dealer_card_animations.clear()
                    winner_text = ""
                    game_over = False
                    PLAYER = 0
                    DILER = 0
                    deck.shuffle()

                    for i in range(2):
                        # Карта игроку
                        suit, (rank, value) = deck.draw()
                        card_data = (suit, rank, value)
                        player_hand.append(card_data)

                        # Создаем анимацию для карты игрока
                        target_x = 50 + len(player_card_animations) * 150
                        target_y = 50
                        anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
                        player_card_animations.append(anim)

                        # Карта дилеру
                        suit, (rank, value) = deck.draw()
                        card_data = (suit, rank, value)
                        dealer_hand.append(card_data)

                        # Создаем анимацию для карты дилера
                        target_x = 50 + len(dealer_card_animations) * 200
                        target_y = 150
                        anim = CardAnimation(card_data, (target_x, target_y), deck_pos)
                        dealer_card_animations.append(anim)

                    PLAYER = calculate_score(player_hand)
                    DILER = calculate_score(dealer_hand)
                    animate_deal = True

                # --- Выход ---
                if exit_button.is_clicked(mouse_pos, True):
                    running = False
                    return True, False, False

        screen.fill(gray)

        # Рисуем колоду
        screen.blit(scaled_deck, deck_pos)

        # Обновляем анимации карт
        all_animations_done = True

        # Анимации карт игрока
        for anim in player_card_animations:
            if not anim.reached:
                anim.update(dt)
                all_animations_done = False

        # Анимации карт дилера
        for anim in dealer_card_animations:
            if not anim.reached:
                anim.update(dt)
                all_animations_done = False

        # Если все анимации завершены, сбрасываем флаг
        if animate_deal and all_animations_done:
            animate_deal = False

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
        score_text = font.render(f"Очки игрока: {PLAYER}", True, (255, 255, 255))
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
        dealer_score_text = font.render(f"Очки дилера: {DILER if game_over or PLAYER > 21 else '??'}", True, (255, 255, 255))
        screen.blit(dealer_score_text, (50, 450))

        if winner_text:
            winner_render = font.render(winner_text, True, (255, 255, 0))
            screen.blit(winner_render, (WIDTH // 2 - winner_render.get_width() // 2, HEIGHT // 2))

        # --- Кнопки ---
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
        if game_started == True and game_over == False:
            issue_a_card_button.draw(screen)
            pass_button.draw(screen)
        if game_started == True and game_over == True:
            start_again_button.draw(screen)

        pygame.display.flip()

    return True, False, False
