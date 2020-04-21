import pygame


class ScoreBoard(object):
    """Класс для вывода игровой информации."""
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        self.level_image = self.font.render(
            str(self.stats.level),
            True,
            self.text_color,
            self.settings.background_color,
        )

        # Уровень выводится под текущим счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_color,
            self.settings.background_color,
        )

        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        self.high_score_image = self.font.render(
            str(self.stats.high_score),
            True,
            self.text_color,
            self.settings.background_color,
        )

        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Выводит счет на экран."""
        self.screen.blit(
            self.score_image,
            self.score_rect,
        )
        self.screen.blit(
            self.high_score_image,
            self.high_score_rect,
        )
        self.screen.blit(
            self.level_image,
            self.level_rect,
        )
