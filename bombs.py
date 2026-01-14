bombs = []

import pygame
class Bomb:
    def __init__(self, x, y, speed, is_giant):
        self.original_image = pygame.transform.scale(pygame.image.load("assets/bomb (1).png"), (30, 30))
        self.giant_image = pygame.transform.scale(pygame.image.load("assets/giant_enemy_bomb.png"), (60, 60))
        self.giant_image = pygame.transform.rotate(self.giant_image, 90)

        if is_giant:
            self.image = self.giant_image
        else:
            self.image = self.original_image

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        if not self.rect.y > 1000:
            screen.blit(self.image, self.rect)
        else:
            bombs.remove(self)