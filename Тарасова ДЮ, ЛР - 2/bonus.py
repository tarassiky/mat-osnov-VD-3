import pygame
import random
from pygame.sprite import Sprite

class Bonus(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Типы бонусов: 'life', 'shield', 'power'
        self.bonus_types = ['life', 'shield', 'power']
        self.type = random.choice(self.bonus_types)
        
        # Создаем бонус как прямоугольник
        size = 30
        self.rect = pygame.Rect(0, 0, size, size)
        
        # Случайная позиция по X
        self.rect.x = random.randint(0, self.settings.screen_width - size)
        self.rect.y = 0
        
        # Цвет в зависимости от типа
        if self.type == 'life':
            self.color = (0, 255, 0)  # Зеленый - дополнительная жизнь
        elif self.type == 'shield':
            self.color = (0, 0, 255)  # Синий - щит
        else:
            self.color = (255, 0, 0)  # Красный - усиление
        
        self.speed = 2.0
        
    def update(self):
        self.rect.y += self.speed
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def apply_effect(self, ai_game):
        if self.type == 'life':
            ai_game.stats.ships_left += 1
            ai_game.sb.prep_ships()
            print("Bonus: Extra life!")
        elif self.type == 'shield':
            # Активируем щит на 5 секунд
            ai_game.ship.shield_active = True
            ai_game.ship.shield_timer = pygame.time.get_ticks()
            print("Bonus: Shield activated!")
        elif self.type == 'power':
            # Усиленные снаряды на 10 секунд
            ai_game.settings.bullets_allowed = 10
            ai_game.power_timer = pygame.time.get_ticks()
            print("Bonus: Power shots activated!")
