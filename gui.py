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


def draw_start_screen(screen, screen_width, screen_height):
    # Create semi-transparent background
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Draw "Press SPACE to start"
    start_font = pygame.font.Font(None, 72)
    start_text = start_font.render("Press SPACE to start", True, (255, 255, 255))
    start_rect = start_text.get_rect()
    start_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(start_text, start_rect)

    # Draw game title above
    title_font = pygame.font.Font(None, 96)
    title_text = title_font.render("SPACE INVADERS", True, (0, 255, 0))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_width // 2, screen_height // 2 - 100)
    screen.blit(title_text, title_rect)


def draw_game_over(screen, screen_width, screen_height, high_score, score):
    # Create semi-transparent background with gradient effect
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(220)
    overlay.fill((10, 10, 30))
    screen.blit(overlay, (0, 0))

    # Draw decorative frame
    frame_padding = 80
    frame_rect = pygame.Rect(
        frame_padding,
        screen_height // 4,
        screen_width - (frame_padding * 2),
        screen_height // 2
    )

    # Draw frame border with glow effect
    pygame.draw.rect(screen, (150, 0, 0), frame_rect, 4, border_radius=15)
    pygame.draw.rect(screen, (255, 50, 50), frame_rect.inflate(8, 8), 2, border_radius=18)

    # Fill frame with darker background
    frame_bg = pygame.Surface((frame_rect.width, frame_rect.height))
    frame_bg.set_alpha(180)
    frame_bg.fill((20, 0, 0))
    screen.blit(frame_bg, frame_rect.topleft)

    # Draw "GAME OVER" with shadow effect
    title_font = pygame.font.Font(None, 110)

    # Shadow
    shadow_text = title_font.render("GAME OVER", True, (80, 0, 0))
    shadow_rect = shadow_text.get_rect()
    shadow_rect.center = (screen_width // 2 + 4, screen_height // 2 - 96)
    screen.blit(shadow_text, shadow_rect)

    # Main text with gradient effect (simulated)
    title_text = title_font.render("GAME OVER", True, (255, 50, 50))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_width // 2, screen_height // 2 - 100)
    screen.blit(title_text, title_rect)

    # Draw score panel with background
    panel_width = 400
    panel_height = 110
    panel_x = (screen_width - panel_width) // 2
    panel_y = screen_height // 2 - 10

    score_panel = pygame.Surface((panel_width, panel_height))
    score_panel.set_alpha(150)
    score_panel.fill((40, 40, 60))
    screen.blit(score_panel, (panel_x, panel_y))

    # Draw panel border
    pygame.draw.rect(screen, (100, 100, 150),
                    (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)

    # Draw scores with better formatting
    score_font = pygame.font.Font(None, 42)

    # Your score
    your_score_label = ability_font.render("Your Score:", True, (200, 200, 200))
    your_score_value = score_font.render(f"{score}", True, (255, 215, 0))

    label_rect = your_score_label.get_rect()
    label_rect.left = panel_x + 30
    label_rect.centery = panel_y + 30
    screen.blit(your_score_label, label_rect)

    value_rect = your_score_value.get_rect()
    value_rect.right = panel_x + panel_width - 30
    value_rect.centery = panel_y + 30
    screen.blit(your_score_value, value_rect)

    # Divider line
    pygame.draw.line(screen, (100, 100, 150),
                    (panel_x + 20, panel_y + 55),
                    (panel_x + panel_width - 20, panel_y + 55), 2)

    # High score
    high_score_label = ability_font.render("High Score:", True, (200, 200, 200))
    high_score_value = score_font.render(f"{high_score}", True, (255, 215, 0))

    label_rect = high_score_label.get_rect()
    label_rect.left = panel_x + 30
    label_rect.centery = panel_y + 80
    screen.blit(high_score_label, label_rect)

    value_rect = high_score_value.get_rect()
    value_rect.right = panel_x + panel_width - 30
    value_rect.centery = panel_y + 80
    screen.blit(high_score_value, value_rect)

    # New high score indicator
    if score >= high_score and score > 0:
        new_record_font = pygame.font.Font(None, 32)
        new_record_text = new_record_font.render("★ NEW RECORD ★", True, (255, 215, 0))
        new_record_rect = new_record_text.get_rect()
        new_record_rect.center = (screen_width // 2, panel_y + panel_height + 30)
        screen.blit(new_record_text, new_record_rect)

    # Draw restart button with hover effect
    button_font = pygame.font.Font(None, 50)
    button_text = "Press SPACE to Restart"

    # Button shadow
    shadow_button = button_font.render(button_text, True, (60, 60, 60))
    shadow_button_rect = shadow_button.get_rect()
    shadow_button_rect.center = (screen_width // 2 + 3, screen_height // 2 + 153)
    screen.blit(shadow_button, shadow_button_rect)

    # Animated text (pulsing effect with time)
    pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
    color_value = int(200 + (55 * pulse))

    restart_text = button_font.render(button_text, True, (color_value, color_value, 255))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (screen_width // 2, screen_height // 2 + 150)
    screen.blit(restart_text, restart_rect)

    # Draw decorative corners
    corner_size = 20
    corner_color = (255, 50, 50)

    # Top-left
    pygame.draw.line(screen, corner_color,
                    (frame_padding - 10, frame_rect.top - 10),
                    (frame_padding - 10 + corner_size, frame_rect.top - 10), 3)
    pygame.draw.line(screen, corner_color,
                    (frame_padding - 10, frame_rect.top - 10),
                    (frame_padding - 10, frame_rect.top - 10 + corner_size), 3)

    # Top-right
    pygame.draw.line(screen, corner_color,
                    (screen_width - frame_padding + 10, frame_rect.top - 10),
                    (screen_width - frame_padding + 10 - corner_size, frame_rect.top - 10), 3)
    pygame.draw.line(screen, corner_color,
                    (screen_width - frame_padding + 10, frame_rect.top - 10),
                    (screen_width - frame_padding + 10, frame_rect.top - 10 + corner_size), 3)

    # Bottom-left
    pygame.draw.line(screen, corner_color,
                    (frame_padding - 10, frame_rect.bottom + 10),
                    (frame_padding - 10 + corner_size, frame_rect.bottom + 10), 3)
    pygame.draw.line(screen, corner_color,
                    (frame_padding - 10, frame_rect.bottom + 10),
                    (frame_padding - 10, frame_rect.bottom + 10 - corner_size), 3)

    # Bottom-right
    pygame.draw.line(screen, corner_color,
                    (screen_width - frame_padding + 10, frame_rect.bottom + 10),
                    (screen_width - frame_padding + 10 - corner_size, frame_rect.bottom + 10), 3)
    pygame.draw.line(screen, corner_color,
                    (screen_width - frame_padding + 10, frame_rect.bottom + 10),
                    (screen_width - frame_padding + 10, frame_rect.bottom + 10 - corner_size), 3)

def draw_start_screen(screen, screen_width, screen_height):
    # Create semi-transparent background with gradient effect
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(220)
    overlay.fill((10, 10, 30))
    screen.blit(overlay, (0, 0))

    # Draw decorative frame
    frame_padding = 80
    frame_rect = pygame.Rect(
        frame_padding,
        screen_height // 4,
        screen_width - (frame_padding * 2),
        screen_height // 2
    )

    # Draw frame border with glow effect
    pygame.draw.rect(screen, (0, 150, 0), frame_rect, 4, border_radius=15)
    pygame.draw.rect(screen, (50, 255, 50), frame_rect.inflate(8, 8), 2, border_radius=18)

    # Fill frame with darker background
    frame_bg = pygame.Surface((frame_rect.width, frame_rect.height))
    frame_bg.set_alpha(180)
    frame_bg.fill((0, 20, 0))
    screen.blit(frame_bg, frame_rect.topleft)

    # Draw "SPACE INVADERS" with shadow effect
    title_font = pygame.font.Font(None, 100)

    # Shadow
    shadow_text = title_font.render("SPACE INVADERS", True, (0, 80, 0))
    shadow_rect = shadow_text.get_rect()
    shadow_rect.center = (screen_width // 2 + 4, screen_height // 2 - 96)
    screen.blit(shadow_text, shadow_rect)

    # Main text
    title_text = title_font.render("SPACE INVADERS", True, (50, 255, 50))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_width // 2, screen_height // 2 - 100)
    screen.blit(title_text, title_rect)

    # Draw subtitle
    subtitle_font = pygame.font.Font(None, 32)
    subtitle_text = subtitle_font.render("Defend Earth from the Invasion!", True, (150, 255, 150))
    subtitle_rect = subtitle_text.get_rect()
    subtitle_rect.center = (screen_width // 2, screen_height // 2 - 40)
    screen.blit(subtitle_text, subtitle_rect)

    # Draw instructions panel
    panel_width = 450
    panel_height = 140
    panel_x = (screen_width - panel_width) // 2
    panel_y = screen_height // 2 + 10

    instructions_panel = pygame.Surface((panel_width, panel_height))
    instructions_panel.set_alpha(150)
    instructions_panel.fill((40, 60, 40))
    screen.blit(instructions_panel, (panel_x, panel_y))

    # Draw panel border
    pygame.draw.rect(screen, (100, 150, 100),
                     (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)

    # Draw controls instructions
    controls_font = pygame.font.Font(None, 28)
    controls = [
        "arrow (left, right)  Move",
        "SPACE  Shoot",
        "T/D/S/B  Abilities"
    ]

    y_offset = panel_y + 25
    for i, control in enumerate(controls):
        control_text = controls_font.render(control, True, (200, 255, 200))
        control_rect = control_text.get_rect()
        control_rect.centerx = screen_width // 2
        control_rect.top = y_offset + (i * 35)
        screen.blit(control_text, control_rect)

    # Draw start button with pulsing effect
    button_font = pygame.font.Font(None, 60)
    button_text = "Press SPACE to Start"

    # Button shadow
    shadow_button = button_font.render(button_text, True, (60, 60, 60))
    shadow_button_rect = shadow_button.get_rect()
    shadow_button_rect.center = (screen_width // 2 + 3, screen_height // 2 + 183)
    screen.blit(shadow_button, shadow_button_rect)

    # Animated text (pulsing effect with time)
    pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
    color_value = int(150 + (105 * pulse))

    start_text = button_font.render(button_text, True, (color_value, 255, color_value))
    start_rect = start_text.get_rect()
    start_rect.center = (screen_width // 2, screen_height // 2 + 180)
    screen.blit(start_text, start_rect)

    # Draw decorative corners
    corner_size = 20
    corner_color = (50, 255, 50)

    # Top-left
    pygame.draw.line(screen, corner_color,
                     (frame_padding - 10, frame_rect.top - 10),
                     (frame_padding - 10 + corner_size, frame_rect.top - 10), 3)
    pygame.draw.line(screen, corner_color,
                     (frame_padding - 10, frame_rect.top - 10),
                     (frame_padding - 10, frame_rect.top - 10 + corner_size), 3)

    # Top-right
    pygame.draw.line(screen, corner_color,
                     (screen_width - frame_padding + 10, frame_rect.top - 10),
                     (screen_width - frame_padding + 10 - corner_size, frame_rect.top - 10), 3)
    pygame.draw.line(screen, corner_color,
                     (screen_width - frame_padding + 10, frame_rect.top - 10),
                     (screen_width - frame_padding + 10, frame_rect.top - 10 + corner_size), 3)

    # Bottom-left
    pygame.draw.line(screen, corner_color,
                     (frame_padding - 10, frame_rect.bottom + 10),
                     (frame_padding - 10 + corner_size, frame_rect.bottom + 10), 3)
    pygame.draw.line(screen, corner_color,
                     (frame_padding - 10, frame_rect.bottom + 10),
                     (frame_padding - 10, frame_rect.bottom + 10 - corner_size), 3)

    # Bottom-right
    pygame.draw.line(screen, corner_color,
                     (screen_width - frame_padding + 10, frame_rect.bottom + 10),
                     (screen_width - frame_padding + 10 - corner_size, frame_rect.bottom + 10), 3)
    pygame.draw.line(screen, corner_color,
                     (screen_width - frame_padding + 10, frame_rect.bottom + 10),
                     (screen_width - frame_padding + 10, frame_rect.bottom + 10 - corner_size), 3)

    # Draw small aliens/decorations (optional extra flair)
    deco_font = pygame.font.Font(None, 40)
    alien_symbols = ["👾", "🛸", "👾"]
    for i, symbol in enumerate(alien_symbols):
        try:
            alien_text = deco_font.render(symbol, True, (100, 255, 100))
            alien_rect = alien_text.get_rect()
            alien_rect.centerx = frame_padding + 30 + (i * (frame_rect.width - 60) // 2)
            alien_rect.centery = frame_rect.top + 20
            screen.blit(alien_text, alien_rect)
        except:
            # Fallback if emoji not supported
            pass