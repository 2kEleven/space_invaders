import pygame

screen_width = 750

class Player:
    def __init__(self, x, y):
        self.original_image = pygame.transform.scale(pygame.image.load("assets/spaceship.png"), (75, 75))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.health = 100
        self.rotation_angle = 0
    def move(self, direction):
        self.rotation_angle = 0

        if direction == "right":
            if not self.rect.right >= screen_width:
                self.rotation_angle = -20
                self.rect.x += self.speed

        elif direction == "left":
            if not self.rect.left <= 0:
                self.rotation_angle = 20
                self.rect.x -= self.speed

        elif direction == "stop":
            self.rotation_angle = 0

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        empty_bar = 100 - self.health / 2
        x = self.rect.centerx - bar_width / 2
        y = self.rect.bottom + 5
        if self.health >= 100:
            self.health = 100

        pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (x - bar_width / 2 + empty_bar, y, self.health / 2, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (x + bar_width / 2 - 1, y, self.health / 2, bar_height))
