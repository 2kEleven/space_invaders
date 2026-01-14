import pygame
from bullets import Bullet, bullet_original_pos

# Initialize fonts
pygame.font.init()
gui_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def draw_coords(screen, screen_width, player, enemies):
    # Draw Player Coordinates at the top left
    player_text = gui_font.render(f"Player: ({player.rect.x}, {player.rect.y})", True, (0, 255, 0))
    screen.blit(player_text, (player.rect.x + 10, player.rect.y - 20))

    # Draw Enemy Coordinates
    for enemy in enemies:
        enemy_text = small_font.render(f"({enemy.rect.x}, {enemy.rect.y})", True, (255, 0, 0))
        screen.blit(enemy_text, (enemy.rect.x, enemy.rect.y - 20))
    for enemy in enemies:
        # Calculate the horizontal distance
        distance_x = abs(player.rect.centerx - enemy.rect.centerx)
        distance_y = abs(player.rect.centery - enemy.rect.centery)
        x_line_text = small_font.render(f"{distance_x}", True, (255, 165, 0))
        y_line_text = small_font.render(f"{distance_y}", True, (255, 165, 0))

        # calculate the middle coordinates of the lines
        mid_x = (player.rect.centerx + enemy.rect.centerx) // 2
        line_y = player.rect.centery
        mid_y = (player.rect.centery + enemy.rect.centery) // 2
        line_x = enemy.rect.centerx

        
        # Center the text surface at the middle of the lines
        text_rect_x = x_line_text.get_rect(center=(mid_x, line_y - 15))
        text_rect_y = y_line_text.get_rect(center=(line_x - 15, mid_y))

        screen.blit(x_line_text, text_rect_x)

        screen.blit(y_line_text, text_rect_y)

        hypotenuse = (distance_x ** 2 + distance_y ** 2) ** (1/2)
        hypotenuse_text = small_font.render(f"{hypotenuse:.2f}", True, (255, 165, 0))
        screen.blit(hypotenuse_text, (mid_x, mid_y))

def draw_line_giant_enemy(screen, player, giant_enemies):
    for giant_enemy in giant_enemies:
        pygame.draw.line(screen, (0, 0, 250), (player.rect.x, player.rect.y), (giant_enemy.rect.x, giant_enemy.rect.y))

def draw_line_bullet(screen, player, bullets):
    for bullet in bullets:
        pygame.draw.line(screen, (255, 255, 255), (player.rect.x, player.rect.y), bullet_original_pos)

def draw_line_bomb(screen, player, bombs):
    for bomb in bombs:
        pygame.draw.line(screen, (250, 250, 250), (player.rect.x, player.rect.y), (bomb.rect.x, bomb.rect.y))

def draw_line_x(screen, player, enemies):
    for enemy in enemies:
        pygame.draw.line(screen, (255, 0, 0), (player.rect.x, player.rect.y), (enemy.rect.x, player.rect.y), 2)
def draw_line_y(screen, player, enemies):
    for enemy in enemies:
        pygame.draw.line(screen, (255, 0, 0), (enemy.rect.x, enemy.rect.y), (enemy.rect.x, player.rect.y), 2)
def draw_hypotenuse(screen, player, enemies):
    for enemy in enemies:
        pygame.draw.line(screen, (255, 0, 0), (player.rect.x, player.rect.y), (enemy.rect.x, enemy.rect.y), 2)