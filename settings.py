class Settings(object):
    """Настройки игры."""

    def __init__(self):
        # Настройки экрана
        self.fullscreen = False
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)

        # Настройки корабля
        self.ship_limit = 3

        # Настройки снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_bullets = 3

        # Настройки пришельцев
        self.fleet_speed = 10

        # Темп ускорения игры
        self.speed_up = 1.1

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Инициализация динамических настроек."""

        # Настройки корабля
        self.ship_speed = 1.5
        # Настройки снаряда
        self.bullet_speed = 1
        # Настройки пришельцев
        self.alien_speed = 1.0
        #   1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скокрости."""
        self.ship_speed *= self.speed_up
        self.bullet_speed *= self.speed_up
        self.alien_speed *= self.speed_up
        self.alien_points += 25

