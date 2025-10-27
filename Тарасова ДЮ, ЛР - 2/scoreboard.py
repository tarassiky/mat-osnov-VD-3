import pygame.font

class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Настройки шрифта - светлый цвет для темного фона
        self.text_color = (255, 255, 255)  # Белый цвет
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        score_str = f"Score: {self.stats.score}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_level(self):
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 70
        
    def prep_ships(self):
        ships_str = f"Ships: {self.stats.ships_left}"
        self.ships_image = self.font.render(ships_str, True, self.text_color, self.settings.bg_color)
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.right = self.screen_rect.right - 20
        self.ships_rect.top = 120
        
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)
