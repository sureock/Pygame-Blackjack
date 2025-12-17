"""Модуль для работы с командной строкой"""
import argparse


def get_args():
    """Функция получения аргументов из командной строки.

    Returns:
        tuple: имя игрока, пароль.
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
        '-p', '--password',
        type=str,
        action='store',
        default='12345',
        help='Пароль'
    )
    args = parser.parse_args()
    return (args.user, args.password)
