class Settings(object):
    """Настройки игры."""

    def __init__(self):
        # Настройки экрана
        self.fullscreen = False
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)

        # Настройки корабля
        self.ship_speed = 1.5

        # Настройки снаряда
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_bullets = 3
