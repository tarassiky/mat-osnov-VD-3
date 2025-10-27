import pygame
import random
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Создаем звезду как маленький круг
        self.size = random.randint(1, 3)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        
        # Случайная позиция на экране
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)
        
        # Яркость звезды
        self.brightness = random.randint(150, 255)
        
    def draw(self):
        # Рисуем звезду как белый круг с разной яркостью
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.ellipse(self.screen, color, self.rect)
