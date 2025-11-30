"""Модуль для работы с командной строкой"""
import argparse


def get_args():
    """Функция получения аргументов из командной строки

    Returns:
        tuple: имя игрока, размер окна
    """

    parser = argparse.ArgumentParser(
        description="Игра Blackjack"
    )
    parser.add_argument(
        'user',
        type=str,
        help='Имя игрока'
    )
    parser.add_argument(
        '-s', '--size',
        type=str,
        choices=['fullscreen', 'windowed'],
        default='windowed',
        help='Размер окна'
    )
    args = parser.parse_args()
    return (args.user, args.size)
