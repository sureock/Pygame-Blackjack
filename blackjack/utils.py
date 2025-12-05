# import pygame
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
