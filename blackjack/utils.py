"""Модуль классов, применяющихся в проекте."""

import pygame
import math
import os
from PIL import Image, ImageSequence


# здесь будет подгрузка карт из папок
def card_load():
    """Метод создания словаря карт.

    Returns:
        cards_suits: словарь путей {(масть, достоинство)->путь к изображению}.
    """

    cwd = os.getcwd()
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cards_suits = {}
    for i in suits:
        for j in cards:
            path = os.path.join(cwd, i, j + '.png')
            cards_suits[(i, j)] = path
    return cards_suits


# Класс для анимации карты
class CardAnimation:
    """Класс анимаций карт.
    """

    def __init__(self, card_data, target_pos, start_pos=None, speed=5000):
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
    """Метод линейного движения к цели.
    Возвращает новую позицию и флаг достижения цели.

    Args:
        start_pos: начальная позиция (x, y).
        target_pos: целевая позиция (x, y).
        speed: скорость перемещения (пикселей за кадр).
        current_pos: текущая позиция (для продолжения движения).

    Returns:
        tuple: новая позиция (list), достигнута ли цель (bool)
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


def calculate_score(hand):
    """Метод расчёта суммы очков в руке.

    Args:
        hand: текущая рука.

    Returns:
        int: сумма очков
    """

    total = 0
    aces = 0

    for suit, rank, value in hand:
        if rank == "A":
            aces += 1
            total += 1
        else:
            total += value

    if aces > 0 and total + 10 <= 21:
        total += 10

    return total


class Text:
    """Класс создания текста и получения параметров для его вывода в окне.
    """

    def __init__(self, text, screen_size, topleft_param, logo=False):
        """Метод инициации класса.

        Args:
            text: текст либо изображение.
            screen_size: размер экрана.
            topleft_param: точка отрисовки.
            logo: флаг для лого.
        """

        def get_relative_width(x, y):
            """Метод получения относительной ширины.

            Returns:
                float: относительная ширина
            """

            return x * y

        def get_relative_height(x, y):
            """Метод получения относительной высоты.

            Returns:
                float: относительная высоты.
            """

            return x * y

        def scale(x, y):
            """Метод изменения размера.

            Returns:
                float: текст, измененного размера.
            """

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
    """Класс слайдера.
    """

    def __init__(self,
                 pos: tuple,
                 size: tuple,
                 initial_val: float,
                 min: int,
                 max: int):
        """Метод инициации класса.

        Args:
            pos: местоположение.
            size: размер.
            initial_val: десятичная дробь.
            min: минимальное значение.
            max: максимальное значение.
        """

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
        """Метод движения слайдера.
        """

        self.button_rect.centerx = mouse_pos[0]

    def render(self, screen):
        """Метод рендера слайдера.
        """

        pygame.draw.rect(screen, 'darkgray', self.container_rect)
        pygame.draw.rect(screen, 'blue', self.button_rect)

    def get_value(self):
        """Метод получения значения от местоположения слайдера.

        Returns:
            float: значение от местоположения слайдера.
        """

        val_range = self.right_pos - self.left_pos - 1
        button_val = self.button_rect.centerx - self.left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min


class Button:
    """Класс кнопки.
    """

    def __init__(self, x, y, width, height, text,
                 color=(200, 200, 200),
                 hover_color=(170, 170, 170),
                 text_color=(0, 0, 0)):
        """Метод инициации класса.

        Args:
            x: координата по x.
            y: координата по y.
            width: ширина кнопки.
            height: высота кнопки.
            text: текст кнопки.
            color: цвет кнопки.
            hover_color: цвет кнопки при наведении мыши.
            text_color: цыет текста кнопки.
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 36)
        self.active = True

    def draw(self, surface):
        """Метод создания кнопки в окне.

        Args:
            surface: окно, на котором будет создана кнопка.

        Returns:
            None: если кнопка не активна.
        """

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
        """Метод считывания нажатия.

        Returns:
            bool: ЛКМ нажата и мышь находится на кнопке.
        """

        return self.rect.collidepoint(mouse_pos) and clicked


class AnimatedBackground:
    """Класс анимирования заднего фона
    """

    animations = {}

    def __init__(self, gif_path, screen_width, screen_height):
        """Метод инициации класса.

        Args:
            gif_path: направление к гифке.
            screen_width: ширина экрана.
            screen_height: высота экрана.
        """

        def load_gif_frames(path):
            """Загружает все кадры GIF"""
            frames = []
            durations = []
            with Image.open(path) as gif:
                for frame in ImageSequence.Iterator(gif):
                    # Конвертируем RGBA
                    frame = frame.convert("RGBA")

                    # Конвертируем PIL Image в PyGame Surface
                    frame_data = frame.tobytes()
                    frame_size = frame.size
                    pygame_frame = pygame.image.fromstring(frame_data,
                                                           frame_size,
                                                           "RGBA")

                    frames.append(pygame_frame)
                    durations.append(frame.info.get('duration', 100))

            return frames, durations

        if gif_path not in self.animations:
            self.frames, self.durations = load_gif_frames(gif_path)
            self.animations[gif_path] = (self.frames, self.durations)
        else:
            self.frames, self.durations = self.animations[gif_path]

        # self.frames, self.durations = load_gif_frames(gif_path)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_frame = 0
        self.animation_time = 0
        self.scaled_frames = []

        # Масштабируем кадры под размер экрана
        for frame in self.frames:
            scaled = pygame.transform.scale(frame,
                                            (screen_width,
                                             screen_height))
            self.scaled_frames.append(scaled)

    def update(self, dt):
        """Обновление анимации"""
        self.animation_time += dt

        # Переход к следующему кадру по времени
        if self.animation_time >= self.durations[self.current_frame]:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        """Отрисовка текущего кадра"""
        screen.blit(self.scaled_frames[self.current_frame], (0, 0))
