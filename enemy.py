import pygame
screen_width = 750

class Enemy:
    def __init__(self, x, y):
        self.original_image = pygame.transform.scale(pygame.image.load("assets/enemy_green.png"), (75, 50))
        self.image = self.original_image
        self.original_dead_image = pygame.transform.scale(pygame.image.load("assets/dead_enemy.png"), (75, 50))
        self.image_explosion = pygame.transform.scale(pygame.image.load("assets/explosion.png"), (90, 90))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.rotation_angle = 0
        self.is_shot = False
        self.is_falling = False
        self.fall_speed = 5
        self.shot_timer = 0
        self.shot_duration = 15  # 1 second at 60 FPS
        
    def move(self):
        if self.rect.x > screen_width -50:
            self.rect.y += 30
            self.speed *= -1
        if self.rect.x < 0:
            self.rect.y += 30
            self.speed *= -1
        if not self.is_shot and not self.is_falling:
            self.rect.x += self.speed
    
    def start_shot(self):
        self.is_shot = True
        self.shot_timer = 0
    
    def update_shot(self):
        if self.is_shot:
            self.shot_timer += 1
            if self.shot_timer >= self.shot_duration:
                self.is_shot = False
                self.is_falling = True
                self.rotation_angle = 0
        
    def start_falling(self):
        self.is_falling = True
        
    def update_falling(self):
        if self.is_falling:
            self.rect.y += self.fall_speed
            self.rotation_angle += 10
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_dead_image, self.rotation_angle)
            self.rect = self.image.get_rect(center=old_center)
    
    def is_off_screen(self, screen_height):
        return self.rect.y > screen_height

    def draw(self, screen):
        if self.is_shot:
            screen.blit(self.image_explosion, self.rect)
        elif self.is_falling:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
enemies = []
for row in range(0, 3):
    for col in range(1, 10):
        enemy = Enemy(50 + col * 80, 50 + row * 60)
        enemies.append(enemy)