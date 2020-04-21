import pygame


class Bullet(pygame.sprite.Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда
        self.rect = pygame.Rect(
            *game.ship.rect.midtop,
            self.settings.bullet_width,
            self.settings.bullet_height
        )

        # Хранение позиции снаряда в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """отображение снаряда на экране."""
        pygame.draw.rect(
            self.screen,
            self.color,
            self.rect
        )


class MegaBullet(Bullet):
    """Мощный читерский снаряд."""
    def __init__(self, game):
        super().__init__(game)
        self.color = (255, 0, 0)

        self.rect = pygame.Rect(
            *game.ship.rect.midtop,
            50,
            50,
        )
