import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game, row, col):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Создаем пришельца сложной формы
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.x = 50 + col * 60
        self.rect.y = 50 + row * 50
        
        self.x = float(self.rect.x)
        self.row = row
        self.col = col
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
    def update(self):
        # Движение вправо-влево с опусканием
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def draw(self):
        # Светло-зеленый цвет для тела (не кислотный)
        body_color = (100, 200, 100)
        # Темно-зеленый для деталей
        dark_green = (50, 150, 50)
        # Желтые глаза
        eye_color = (255, 255, 0)
        
        # Тело - овал
        pygame.draw.ellipse(self.screen, body_color, self.rect)
        
        # Голова - немного уже тела
        head_rect = pygame.Rect(self.rect.left + 5, self.rect.top + 5, self.rect.width - 10, 20)
        pygame.draw.ellipse(self.screen, dark_green, head_rect)
        
        # Глаза - желтые
        left_eye = pygame.Rect(self.rect.left + 10, self.rect.top + 12, 6, 6)
        right_eye = pygame.Rect(self.rect.right - 16, self.rect.top + 12, 6, 6)
        pygame.draw.ellipse(self.screen, eye_color, left_eye)
        pygame.draw.ellipse(self.screen, eye_color, right_eye)
        
        # Рот
        mouth_rect = pygame.Rect(self.rect.left + 15, self.rect.top + 22, 10, 3)
        pygame.draw.rect(self.screen, (50, 50, 50), mouth_rect)
        
        # Щупальца/антенны
        left_antenna = pygame.Rect(self.rect.left + 8, self.rect.top - 5, 3, 8)
        right_antenna = pygame.Rect(self.rect.right - 11, self.rect.top - 5, 3, 8)
        pygame.draw.rect(self.screen, dark_green, left_antenna)
        pygame.draw.rect(self.screen, dark_green, right_antenna)
        
        # Ноги
        for i in range(3):
            leg_x = self.rect.left + 5 + i * 12
            leg_rect = pygame.Rect(leg_x, self.rect.bottom - 8, 6, 8)
            pygame.draw.rect(self.screen, dark_green, leg_rect)
