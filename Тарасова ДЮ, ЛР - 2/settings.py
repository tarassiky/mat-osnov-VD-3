class Settings:
    def __init__(self):
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 50)  # Темно-синий космический фон
        
        # Настройки корабля
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        # Параметры снаряда
        self.bullet_speed = 2.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 255, 0)  # Желтый для снарядов
        self.bullets_allowed = 3
        
        # Настройки пришельцев
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 - вправо, -1 - влево
        
        # Очки за пришельца
        self.alien_points = 50
        
        # Темп ускорения игры
        self.speedup_scale = 1.1
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 1.0
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
