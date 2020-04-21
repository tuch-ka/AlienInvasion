"""
Основной модуль. Запуск игры.
# TODO: реализовать изменение скорости стрелками вверх/вниз
# TODO: настройки в json
# TODO: добавть autofire на capslock
"""
import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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

        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )

        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Обновляет позиции снарядов."""
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.background_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.max_bullets:
            self.bullets.add(
                Bullet(self)
            )

    def _create_alien(self, alien_number, row_numer):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_numer
        self.aliens.add(alien)

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание одного пришельца, не включенного во флот,
        # для расчета максимального количествыа пришельцев в ряду
        # TODO: оптипизировать
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = (
                self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        )
        number_of_rows_y = available_space_y // (2 * alien_height)

        # Создание флота пришельцев.
        for row_number in range(number_of_rows_y):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()

            self._update_screen()


if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()

