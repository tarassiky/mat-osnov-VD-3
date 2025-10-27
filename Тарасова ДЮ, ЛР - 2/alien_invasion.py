import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bonus import Bonus
from stars import Star
import random

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Инициализация звуков
        self._initialize_sounds()
        
        # Создаем экземпляры
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        self._create_fleet()
        self._create_stars()
        self.play_button = Button(self, "Play")
        
        # Таймер для усиленных снарядов
        self.power_timer = 0
        self.power_duration = 10000  # 10 секунд
        
    def _initialize_sounds(self):
        try:
            self.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
            self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
            self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
            self.life_lost_sound = pygame.mixer.Sound("sounds/life_lost.wav")
        except:
            print("Warning: Some sound files not found")
            # Создаем заглушки если файлы не найдены
            self.laser_sound = None
            self.explosion_sound = None
            self.game_over_sound = None
            self.life_lost_sound = None
        
    def run_game(self):
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bonuses()
                
            self._update_screen()
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            
            self.aliens.empty()
            self.bullets.empty()
            self.bonuses.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self._save_game()
        elif event.key == pygame.K_l:
            self._load_game()
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.laser_sound:
                self.laser_sound.play()
            
    def _update_bullets(self):
        self.bullets.update()
        
        # Проверка времени действия усиленных снарядов
        if self.settings.bullets_allowed > 3 and pygame.time.get_ticks() - self.power_timer > self.power_duration:
            self.settings.bullets_allowed = 3
        
        # Удаление снарядов за экраном
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        # Проверка попаданий в пришельцев
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            if self.explosion_sound:
                self.explosion_sound.play()
            self.stats.score += len(collisions) * self.settings.alien_points
            self.sb.prep_score()
            
            # Шанс выпадения бонуса при уничтожении пришельца
            if random.random() < 0.1:  # 10% шанс
                self._create_bonus(collisions)
            
        # Проверка уничтожения всего флота
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
                
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        # Проверка столкновений пришельцев с кораблем
        if pygame.sprite.spritecollideany(self.ship, self.aliens) and not self.ship.shield_active:
            self._ship_hit()
            
        # Проверка достижения пришельцами нижнего края
        self._check_aliens_bottom()
        
    def _update_bonuses(self):
        self.bonuses.update()
        
        # Удаление бонусов за экраном
        for bonus in self.bonuses.copy():
            if bonus.rect.top > self.settings.screen_height:
                self.bonuses.remove(bonus)
        
        # Проверка столкновений бонусов с кораблем
        bonus_collisions = pygame.sprite.spritecollide(self.ship, self.bonuses, True)
        for bonus in bonus_collisions:
            bonus.apply_effect(self)
        
    def _create_bonus(self, collisions):
        # Создаем бонус в позиции первого уничтоженного пришельца
        for aliens_list in collisions.values():
            if aliens_list:
                alien_pos = aliens_list[0].rect
                bonus = Bonus(self)
                bonus.rect.center = alien_pos.center
                self.bonuses.add(bonus)
                break
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _create_fleet(self):
        # Создаем несколько рядов пришельцев
        number_rows = 3
        number_cols = 8
        
        for row in range(number_rows):
            for col in range(number_cols):
                alien = Alien(self, row, col)
                self.aliens.add(alien)
                
    def _create_stars(self):
        # Создаем звездное небо
        for _ in range(100):  # 100 звезд
            star = Star(self)
            self.stars.add(star)
            
    def _ship_hit(self):
        if self.life_lost_sound:
            self.life_lost_sound.play()
            
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            self.aliens.empty()
            self.bullets.empty()
            self.bonuses.empty()
            
            self._create_fleet()
            self.ship.center_ship()
        else:
            if self.game_over_sound:
                self.game_over_sound.play()
            self.stats.game_active = False
            
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
            
    def _save_game(self):
        import pickle
        game_data = {
            "level": self.stats.level,
            "score": self.stats.score,
            "ships_left": self.stats.ships_left
        }
        with open("savegame.pkl", "wb") as f:
            pickle.dump(game_data, f)
        print("Game saved!")
            
    def _load_game(self):
        import pickle
        try:
            with open("savegame.pkl", "rb") as f:
                game_data = pickle.load(f)
                
            self.stats.level = game_data["level"]
            self.stats.score = game_data["score"]
            self.stats.ships_left = game_data["ships_left"]
            
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            self.aliens.empty()
            self.bullets.empty()
            self.bonuses.empty()
            self._create_fleet()
            self.ship.center_ship()
            
            print("Game loaded!")
        except FileNotFoundError:
            print("No saved game found!")
            
    def _update_screen(self):
        # Заполняем экран темно-синим цветом
        self.screen.fill(self.settings.bg_color)
        
        # Рисуем звезды
        for star in self.stars.sprites():
            star.draw()
        
        # Рисуем корабль, снаряды, пришельцев и бонусы
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        for alien in self.aliens.sprites():
            alien.draw()
            
        for bonus in self.bonuses.sprites():
            bonus.draw()
            
        # Вывод счета
        self.sb.show_score()
        
        # Кнопка Play, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
