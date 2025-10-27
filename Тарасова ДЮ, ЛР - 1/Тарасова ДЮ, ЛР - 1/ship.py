import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Создаем корабль как прямоугольник (вместо загрузки картинки)
        self.rect = pygame.Rect(0, 0, 60, 50)
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
        
    def blitme(self):
        pygame.draw.rect(self.screen, (0, 100, 200), self.rect)  # Синий корабль
        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)