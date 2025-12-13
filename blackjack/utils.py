import pygame
import math
import os


# здесь будет подгрузка карт из папок
def card_load():
    """Создание словаря{(масть, достоинство)->путь к изображению}

    Returns:
        dict
    Raises:

    """

    cwd = os.getcwd()
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cards_suits = {}
    for i in suits:
        for j in cards:
            path = os.path.join(cwd, 'blackjack', i, j + '.png')
            cards_suits[(i, j)] = path
    return cards_suits


# Класс для анимации карты
class CardAnimation:
    def __init__(self, card_data, target_pos, start_pos=None, speed=9000):
        self.suit = card_data[0]
        self.rank = card_data[1]
        self.value = card_data[2]
        self.target_pos = target_pos
        self.start_pos = start_pos if start_pos else [0, 0]
        self.current_pos = list(self.start_pos)
        self.speed = speed
        self.reached = False
        self.card_text = f"{self.rank} {self.suit}"

    def update(self, dt):
        if not self.reached:
            self.current_pos, self.reached = move_image(
                self.current_pos,
                self.target_pos,
                self.speed * dt
            )
        return self.reached


def move_image(start_pos, target_pos, speed, current_pos=None):
    """
    Линейное движение к цели
    Возвращает новую позицию и флаг достижения цели

    :param start_pos: начальная позиция (x, y)
    :param target_pos: целевая позиция (x, y)
    :param speed: скорость перемещения (пикселей за кадр)
    :param current_pos: текущая позиция (для продолжения движения)
    :return: (новая позиция, достигнута ли цель)
    """
    if current_pos is None:
        current_pos = list(start_pos)

    # Вычисляем вектор к цели
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]

    # Расстояние до цели
    distance = math.sqrt(dx**2 + dy**2)

    # Если достигли цели
    if distance <= speed:
        return target_pos, True

    # Нормализуем вектор и двигаемся
    if distance > 0:
        dx_normalized = dx / distance
        dy_normalized = dy / distance

        current_pos[0] += dx_normalized * speed
        current_pos[1] += dy_normalized * speed

    return current_pos, False


# расчет хрен знает чего
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


class Text:
    def __init__(self, text, screen_size, topleft_param, logo=False):

        def get_relative_width(x, y):
            return x * y

        def get_relative_height(x, y):
            return x * y

        def scale(x, y):
            return pygame.transform.scale(x, y)

        self.width = screen_size[0]
        self.height = screen_size[1]

        self.width_relative = self.width / 1000
        self.height_relative = self.height / 750

        self.text = text
        self.text_width = text.get_size()[0]
        self.text_height = text.get_size()[1]

        if logo:
            self.text_width = self.text_width // 2
            self.text_height = self.text_height // 2

        self.text_scale = scale(text,
                                (get_relative_width(self.text_width,
                                                    self.width_relative),
                                 get_relative_height(self.text_height,
                                                     self.height_relative)
                                 ))
        self.text_rect = self.text_scale.get_rect()
        self.text_rect.topleft = topleft_param

        self.button_rect = pygame.Rect(topleft_param[0],
                                       topleft_param[1],
                                       get_relative_width(
                                            self.text_width,
                                            self.width_relative),
                                       get_relative_height(
                                            self.text_height,
                                            self.height_relative))


class Slider:
    def __init__(self,
                 pos: tuple,
                 size: tuple,
                 initial_val: float,
                 min: int,
                 max: int):
        self.pos = pos
        self.size = size

        self.left_pos = self.pos[0] - (size[0] // 2)
        self.right_pos = self.pos[0] + (size[0] // 2)
        self.top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_value = (self.right_pos - self.left_pos) * initial_val

        self.container_rect = pygame.Rect(self.left_pos,
                                          self.top_pos,
                                          self.size[0],
                                          self.size[1])
        self.button_rect = pygame.Rect(self.left_pos + self.initial_value - 5,
                                       self.top_pos,
                                       10,
                                       self.size[1])

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self, screen):
        pygame.draw.rect(screen, 'darkgray', self.container_rect)
        pygame.draw.rect(screen, 'blue', self.button_rect)

    def get_value(self):
        val_range = self.right_pos - self.left_pos - 1
        button_val = self.button_rect.centerx - self.left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min
