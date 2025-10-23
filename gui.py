import pygame

# Initialize fonts
pygame.font.init()
gui_font = pygame.font.Font(None, 36)
ability_font = pygame.font.Font(None, 24)
ability_small_font = pygame.font.Font(None, 18)

# Load ability images
ability_images = {}
ability_files = {
    "time_warp": "assets/ability_clock.png",
    "double_fire": "assets/ability_bullet.png",
    "shield": "assets/ability_shield.png",
    "bomb": "assets/ability_bomb.png",
    "double_points": "assets/ability_bullet.png"  # Added double_points ability
}

# Load images with error handling
for ability, filepath in ability_files.items():
    try:
        ability_images[ability] = pygame.transform.scale(pygame.image.load(filepath), (50, 50))
        print(f"Successfully loaded {filepath} for {ability}")
    except pygame.error as e:
        print(f"Warning: Could not load {filepath} for {ability}: {e}")

def draw_top_gui(screen, points, level, high_score, screen_width):
    """Draw the top GUI bar with points, level, and highscore"""
    gui_bg = pygame.Surface((screen_width, 50))
    gui_bg.set_alpha(128)
    gui_bg.fill((0, 0, 0))
    screen.blit(gui_bg, (0, 0))

    # Draw points text
    points_text = gui_font.render(f"Points: {points}", True, (255, 255, 255))
    screen.blit(points_text, (20, 10))

    # Draw level text
    level_text = gui_font.render(f"Level: {level}", True, (255, 255, 255))
    level_text_rect = level_text.get_rect()
    level_text_rect.topright = (screen_width - 20, 10)
    screen.blit(level_text, level_text_rect)

    # Draw the high score
    highscore_text = gui_font.render(f"Highscore: {high_score}", True, (255, 215, 0))
    highscore_rect = highscore_text.get_rect()
    highscore_rect.centerx = screen_width // 2
    highscore_rect.top = 10
    screen.blit(highscore_text, highscore_rect)


def draw_available_abilities(screen, availible_abilities, screen_height):
    if not availible_abilities:
        return

    # Count abilities
    ability_counts = {}
    unique_abilities = []
    for ability in availible_abilities:
        if ability not in ability_counts:
            ability_counts[ability] = 0
            unique_abilities.append(ability)
        ability_counts[ability] += 1

    # Draw semi-transparent background
    ability_bg = pygame.Surface((350, 200))
    ability_bg.set_alpha(128)
    ability_bg.fill((0, 0, 0))
    screen.blit(ability_bg, (10, screen_height - 150))

    # Draw abilities horizontally
    start_x = 20
    start_y = screen_height - 100

    for i, ability in enumerate(unique_abilities):
        if i < 4:  # Limit to 4 abilities displayed
            # Debug: print which ability is being drawn
            if ability not in ability_images:
                print(f"Warning: Ability '{ability}' not found in ability_images!")
            
            # Draw "To activate"
            activate_text = ability_small_font.render("Activate:", True, (200, 200, 200))
            activate_rect = activate_text.get_rect()
            activate_rect.centerx = start_x + (i * 75) + 25
            activate_rect.bottom = start_y - 35
            screen.blit(activate_text, activate_rect)
            
            # Draw first letter (to activate)
            key_text = ability_font.render(ability[0].upper(), True, (255, 255, 0))
            key_rect = key_text.get_rect()
            key_rect.centerx = start_x + (i * 75) + 25
            key_rect.bottom = start_y - 8
            screen.blit(key_text, key_rect)

            # Draw ability image
            if ability in ability_images:
                screen.blit(ability_images[ability], (start_x + (i * 75), start_y))
            
            # Draw amount below ability
            amount_text = ability_small_font.render(f"x{ability_counts[ability]}", True, (255, 255, 255))
            amount_rect = amount_text.get_rect()
            amount_rect.centerx = start_x + (i * 75) + 25
            amount_rect.top = start_y + 55
            screen.blit(amount_text, amount_rect)
