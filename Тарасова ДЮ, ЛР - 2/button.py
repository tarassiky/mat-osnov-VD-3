import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Размеры и свойства кнопки - космический стиль
        self.width, self.height = 200, 50
        self.button_color = (0, 100, 200)  # Синий цвет кнопки
        self.text_color = (255, 255, 255)  # Белый текст
        self.font = pygame.font.SysFont(None, 48)
        
        # Построение кнопки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Сообщение кнопки
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Рисуем кнопку с обводкой
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)  # Белая обводка
        self.screen.blit(self.msg_image, self.msg_image_rect)
