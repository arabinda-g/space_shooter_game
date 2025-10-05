import pygame
import random
import math
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.shoot_cooldown = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # Keep player on screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 10
            return Bullet(self.x + self.width // 2, self.y, -10, CYAN)
        return None
    
    def draw(self, screen):
        # Draw player ship
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 4, self.y + self.height - 10),
            (self.x + 3 * self.width // 4, self.y + self.height - 10),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, CYAN, points)
        
        # Draw health bar
        bar_width = 60
        bar_height = 8
        bar_x = self.x + self.width // 2 - bar_width // 2
        bar_y = self.y - 15
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Enemy:
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        if enemy_type == 1:
            self.width = 30
            self.height = 30
            self.speed = 2
            self.health = 30
            self.color = RED
            self.points = 10
        elif enemy_type == 2:
            self.width = 40
            self.height = 40
            self.speed = 1.5
            self.health = 60
            self.color = PURPLE
            self.points = 25
        else:  # Boss
            self.width = 80
            self.height = 60
            self.speed = 1
            self.health = 200
            self.color = ORANGE
            self.points = 100
            
        self.max_health = self.health
        self.shoot_cooldown = 0
        
    def update(self):
        self.y += self.speed
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self):
        if self.enemy_type >= 2 and self.shoot_cooldown <= 0:
            self.shoot_cooldown = 60 if self.enemy_type == 2 else 30
            return Bullet(self.x + self.width // 2, self.y + self.height, 5, self.color)
        return None
    
    def draw(self, screen):
        # Draw enemy
        if self.enemy_type == 1:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.enemy_type == 2:
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        else:  # Boss
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, YELLOW, (self.x + 10, self.y + 10, self.width - 20, self.height - 20))
        
        # Draw health bar for stronger enemies
        if self.enemy_type >= 2:
            bar_width = self.width
            bar_height = 6
            bar_x = self.x
            bar_y = self.y - 10
            
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Bullet:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 4
        self.height = 10
        
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y, self.width, self.height))

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 30
        self.color = random.choice([RED, ORANGE, YELLOW, WHITE])
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 30))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type  # 'health', 'rapid_fire', 'shield'
        self.width = 20
        self.height = 20
        self.speed = 2
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        if self.power_type == 'health':
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x + 8, self.y + 4, 4, 12))
            pygame.draw.rect(screen, WHITE, (self.x + 4, self.y + 8, 12, 4))
        elif self.power_type == 'rapid_fire':
            pygame.draw.circle(screen, YELLOW, (self.x + 10, self.y + 10), 10)
            pygame.draw.circle(screen, RED, (self.x + 10, self.y + 10), 6)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.particles = []
        self.power_ups = []
        
        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 10
        self.spawn_timer = 0
        
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.game_state = "playing"  # "playing", "game_over", "paused"
        
        # Star field background
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]
        
    def spawn_enemy(self):
        if self.enemies_spawned < self.enemies_per_wave:
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(-100, -50)
            
            # Determine enemy type based on wave
            if self.wave >= 5 and random.random() < 0.1:  # Boss
                enemy_type = 3
            elif self.wave >= 3 and random.random() < 0.3:  # Purple enemy
                enemy_type = 2
            else:  # Regular enemy
                enemy_type = 1
                
            self.enemies.append(Enemy(x, y, enemy_type))
            self.enemies_spawned += 1
    
    def handle_collisions(self):
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    # Create explosion particles
                    for _ in range(10):
                        self.particles.append(Particle(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                    
                    enemy.health -= 25
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    if enemy.health <= 0:
                        self.score += enemy.points
                        if random.random() < 0.1:  # 10% chance for power-up
                            power_type = random.choice(['health', 'rapid_fire'])
                            self.power_ups.append(PowerUp(enemy.x, enemy.y, power_type))
                        self.enemies.remove(enemy)
        
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if (bullet.x < self.player.x + self.player.width and
                bullet.x + bullet.width > self.player.x and
                bullet.y < self.player.y + self.player.height and
                bullet.y + bullet.height > self.player.y):
                
                self.player.health -= 20
                self.enemy_bullets.remove(bullet)
                
                # Create damage particles
                for _ in range(5):
                    self.particles.append(Particle(self.player.x + self.player.width // 2, self.player.y + self.player.height // 2))
        
        # Enemies vs player
        for enemy in self.enemies[:]:
            if (enemy.x < self.player.x + self.player.width and
                enemy.x + enemy.width > self.player.x and
                enemy.y < self.player.y + self.player.height and
                enemy.y + enemy.height > self.player.y):
                
                self.player.health -= 30
                self.enemies.remove(enemy)
                
                # Create collision particles
                for _ in range(15):
                    self.particles.append(Particle(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
        
        # Power-ups vs player
        for power_up in self.power_ups[:]:
            if (power_up.x < self.player.x + self.player.width and
                power_up.x + power_up.width > self.player.x and
                power_up.y < self.player.y + self.player.height and
                power_up.y + power_up.height > self.player.y):
                
                if power_up.power_type == 'health':
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                elif power_up.power_type == 'rapid_fire':
                    self.player.shoot_cooldown = max(0, self.player.shoot_cooldown - 5)
                
                self.power_ups.remove(power_up)
    
    def update(self):
        if self.game_state != "playing":
            return
            
        # Update player
        self.player.update()
        
        # Handle shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.append(bullet)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)
        
        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer >= 60:  # Spawn every second
            self.spawn_enemy()
            self.spawn_timer = 0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
            else:
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_bullets.append(bullet)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.y > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)
        
        # Check for wave completion
        if self.enemies_spawned >= self.enemies_per_wave and len(self.enemies) == 0:
            self.wave += 1
            self.enemies_spawned = 0
            self.enemies_per_wave += 5
        
        # Handle collisions
        self.handle_collisions()
        
        # Check game over
        if self.player.health <= 0:
            self.game_state = "game_over"
        
        # Update stars
        self.stars = [(x, (y + 1) % SCREEN_HEIGHT) for x, y in self.stars]
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars
        for x, y in self.stars:
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        if self.game_state == "playing":
            # Draw game objects
            self.player.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            for bullet in self.enemy_bullets:
                bullet.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            for particle in self.particles:
                particle.draw(self.screen)
            
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            
            # Draw UI
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
            health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
            
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(wave_text, (10, 50))
            self.screen.blit(health_text, (10, 90))
            
            # Draw instructions
            instructions = [
                "WASD/Arrow Keys: Move",
                "SPACE: Shoot",
                "ESC: Pause"
            ]
            for i, instruction in enumerate(instructions):
                text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))
        
        elif self.game_state == "game_over":
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        elif self.game_state == "paused":
            pause_text = self.big_font.render("PAUSED", True, YELLOW)
            continue_text = self.font.render("Press ESC to Continue", True, WHITE)
            
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                
                if self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.__init__()  # Restart game
                    elif event.key == pygame.K_q:
                        return False
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
