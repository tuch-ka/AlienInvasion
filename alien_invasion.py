"""
Основной модуль. Запуск игры.
# TODO: реализовать изменение скорости стрелками вверх/вниз
# TODO: настройки в json
# TODO: добавть autofire на capslock
"""
import sys
import time

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet, MegaBullet
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

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.mega_bullets = pygame.sprite.Group()
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

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_z:
            self._fire_mega_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_bullet_alien_collisions(self):

        # Проверка попаданий в пришельцев.
        collisions = pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True,
        )

        self._using_mega_bullets()

        if not self.aliens:
            self.bullets.empty()
            self.mega_bullets.empty()
            self._create_fleet()

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_bullets(self):
        """Обновляет позиции снарядов."""
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(
            self.ship,
            self.aliens
        ):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.background_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for mega_bullet in self.mega_bullets.sprites():
            mega_bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.max_bullets:
            self.bullets.add(
                Bullet(self)
            )

    def _fire_mega_bullet(self):
        self.mega_bullets.add(
            MegaBullet(self)
        )

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
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

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_speed
        self.settings.fleet_direction *= -1

    def _using_mega_bullets(self):
        # Обработка читерских пуль
        self.mega_bullets.update()

        for mega_bullet in self.mega_bullets.copy():
            if mega_bullet.rect.bottom <= 0:
                self.mega_bullets.remove(mega_bullet)

        pygame.sprite.groupcollide(
            self.mega_bullets,
            self.aliens,
            False,
            True,
        )

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            time.sleep(2)

        else:
            self.stats.game_active = False

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()

