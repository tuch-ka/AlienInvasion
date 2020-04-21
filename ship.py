import pygame


class Ship(object):
    """Класс управления кораблём."""
    def __init__(self, game):
        self.settings = game.settings

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.moving_right = False
        self.moving_left = False

        self.center_ship()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Обновляет позицию корабля с учетом флага."""
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.x += self.settings.ship_speed
        if self.moving_left and (self.rect.left > self.screen_rect.left):
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
