"""
Основной модуль. Запуск игры.
"""
import sys

import pygame

from settings import Settings


class AlienInvasion(object):
    """
    Класс для управления ресурсами и поведением игры.
    """
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        pygame.display.set_caption('Alien Invasion')

        self.settings = Settings()

        self.background_color = self.settings.background_color
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.background_color)
            pygame.display.flip()


if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()

