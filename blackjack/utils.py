import pygame
import math


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
