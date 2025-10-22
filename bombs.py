bombs = []
import pygame
class Bomb:
    def __init__(self, x, y):
        self.original_image = pygame.transform.scale(pygame.image.load("assets/bomb (1).png"), (30, 30))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 10
        self.time = 0

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)