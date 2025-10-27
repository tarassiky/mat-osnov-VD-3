import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # Создаем снаряд
        self.rect = pygame.Rect(0, 0, 5, 15)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        self.y = float(self.rect.y)
        
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        # Основной цвет снаряда
        main_color = (255, 255, 0)  # желтый
        glow_color = (255, 200, 0)   # оранжевое свечение
        
        # Рисуем свечение
        glow_rect = pygame.Rect(
            self.rect.x - 2, self.rect.y - 2,
            self.rect.width + 4, self.rect.height + 4
        )
        pygame.draw.rect(self.screen, glow_color, glow_rect)
        
        # Рисуем основной снаряд
        pygame.draw.rect(self.screen, main_color, self.rect)
        
        # Яркое ядро
        core_rect = pygame.Rect(
            self.rect.x + 1, self.rect.y + 1,
            self.rect.width - 2, self.rect.height - 2
        )
        pygame.draw.rect(self.screen, (255, 255, 200), core_rect)
