import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Создаем корабль как прямоугольник для коллизии
        self.rect = pygame.Rect(0, 0, 60, 50)
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        
        # Щит
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 5000  # 5 секунд в миллисекундах
        
    def update(self):
        # Проверка времени действия щита
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > self.shield_duration:
            self.shield_active = False
            
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
        
    def blitme(self):
        # Основной цвет корабля - синий
        main_color = (0, 100, 200)
        accent_color = (50, 150, 255)
        window_color = (200, 230, 255)
        
        # Корпус корабля - трапеция
        points = [
            (self.rect.left, self.rect.bottom),  # левый низ
            (self.rect.right, self.rect.bottom), # правый низ
            (self.rect.right - 15, self.rect.top + 10), # правый верх
            (self.rect.left + 15, self.rect.top + 10)   # левый верх
        ]
        pygame.draw.polygon(self.screen, main_color, points)
        
        # Кабина
        cabin_rect = pygame.Rect(
            self.rect.left + 20, self.rect.top + 5,
            self.rect.width - 40, 15
        )
        pygame.draw.ellipse(self.screen, accent_color, cabin_rect)
        
        # Окно кабины
        window_rect = pygame.Rect(
            self.rect.left + 25, self.rect.top + 8,
            self.rect.width - 50, 8
        )
        pygame.draw.ellipse(self.screen, window_color, window_rect)
        
        # Двигатели
        for i in range(2):
            engine_x = self.rect.left + 15 + i * 30
            engine_rect = pygame.Rect(engine_x, self.rect.bottom - 10, 10, 10)
            pygame.draw.rect(self.screen, (255, 100, 0), engine_rect)
        
        # Рисуем щит если активен
        if self.shield_active:
            shield_rect = pygame.Rect(
                self.rect.x - 8, self.rect.y - 8,
                self.rect.width + 16, self.rect.height + 16
            )
            pygame.draw.ellipse(self.screen, (0, 255, 255), shield_rect, 3)
        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.shield_active = False
