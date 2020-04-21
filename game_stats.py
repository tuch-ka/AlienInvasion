class GameStats(object):
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
