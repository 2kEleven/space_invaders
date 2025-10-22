bullets = []
import pygame, math
class Bullet:
    def __init__(self, x, y, angle_deg):
        self.original_image = pygame.transform.scale(pygame.image.load("assets/bullet.png"), (30, 30))
        self.rect = self.original_image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.original_image)
        self.speed = 10
        self.angle = angle_deg
        radians = math.radians(self.angle + 90)
        self.dx = -math.cos(radians) * self.speed
        self.dy = -math.sin(radians) * self.speed
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.time = 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.time += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)