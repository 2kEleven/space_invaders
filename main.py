from giant_enemy import *
from player import *
from bullets import *
from enemy import *
from bombs import *
from gui import *
import os
import random

# formula for the bullet:
# f(x) = ax + b
# f(x) = 46.6x - 98.969

#clock
clock = pygame.time.Clock()
# screen/background
screen_width, screen_height = 750, 750
screen = pygame.display.set_mode((screen_width, screen_height))
image_sky = pygame.image.load("assets/space_background.png")
pygame.display.set_caption("Space Invader")
# import high_score
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Initialize font for GUI
pygame.font.init()
gui_font = pygame.font.Font(None, 36)

def background_sky():
    bg = pygame.transform.scale(image_sky, (screen_width, screen_height))
    screen.blit(bg, (0, 0))

# abilities
abilities = {"time_warp": 5,
             "double_fire": 10,
             "shield": 5,
             "bomb": 0.1} # ability : seconds
availible_abilities = []
active_abilities = {}
bomb_triggered = {}
double_fire = False
shield = False

# player
player = Player(screen_width / 2, 550)
score = 0
level = 1
# enemies
spawn_enemies()
# giant enemy
giant_enemies = []
# running
Running = True
while Running:
    # screen/background
    screen.fill((0, 0, 0))
    background_sky()
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not bullets:
                    if double_fire:
                        bullets.append(Bullet(player.rect.centerx - 30, player.rect.top + 30, -player.rotation_angle))
                        bullets.append(Bullet(player.rect.centerx + 30, player.rect.top + 30, -player.rotation_angle))
                    else:
                        bullets.append(Bullet(player.rect.centerx, player.rect.top, -player.rotation_angle))
                else:
                    if all(bullet.time >= 35 for bullet in bullets):
                        if double_fire:
                            bullets.append(Bullet(player.rect.centerx - 30, player.rect.top + 30, -player.rotation_angle))
                            bullets.append(Bullet(player.rect.centerx + 30, player.rect.top + 30, -player.rotation_angle))
                        else:
                            bullets.append(Bullet(player.rect.centerx, player.rect.top, -player.rotation_angle))
            
            # Ability activation keys
            if event.key == pygame.K_t:  # Time warp
                if "time_warp" in availible_abilities:
                    availible_abilities.remove("time_warp")
                    active_abilities["time_warp"] = abilities["time_warp"]
            
            elif event.key == pygame.K_d:  # Double fire
                if "double_fire" in availible_abilities:
                    availible_abilities.remove("double_fire")
                    active_abilities["double_fire"] = abilities["double_fire"]
            
            elif event.key == pygame.K_s:  # Shield
                if "shield" in availible_abilities:
                    availible_abilities.remove("shield")
                    active_abilities["shield"] = abilities["shield"]
            
            elif event.key == pygame.K_b:  # Bomb
                if "bomb" in availible_abilities:
                    availible_abilities.remove("bomb")
                    active_abilities["bomb"] = abilities["bomb"]
                    bomb_triggered["bomb"] = False  # Initialize bomb trigger


    # KeyDown
    Key = pygame.key.get_pressed()
    if Key[pygame.K_RIGHT]:
        player.move("right")
    elif Key[pygame.K_LEFT]:
        player.move("left")
    else:
        player.move("stop")
    # bullet
    for bullet in bullets:
        bullet.move()
        if bullet.rect.y + 20 < 0:
            bullets.remove(bullet)
        else:
            screen.blit(bullet.image, bullet.rect)
    # bombs
    for enemy in enemies:
        drop_bomb = random.randint(1, 1000)
        if drop_bomb == 1:
            bomb = Bomb(enemy.rect.x, enemy.rect.y)
            bombs.append(bomb)
    for bomb in bombs:
        bomb.move()
        if bomb.rect.y + 20 < 0:
            bombs.remove(bomb)
        else:
            bomb.draw(screen)
    # bomb ---- player collision
    for bomb in bombs:
        offset = (bomb.rect.x - player.rect.x, bomb.rect.y - player.rect.y)
        if player.mask.overlap(bomb.mask, offset):
            if not shield:
                player.health -= 20
            bombs.remove(bomb)

    # player
    player.draw(screen)
    # player --- enemy collision
    for enemy in enemies[:]:
        offset = (player.rect.x - enemy.rect.x, player.rect.y - enemy.rect.y)
        if enemy.mask.overlap(player.mask, offset):
            if not shield:
                player.health -= 30
            enemy.rect.y += player.rect.height + 10
    # health bar
    player.draw_health_bar(screen)
    if player.health <= 0:
        Running = False
        game_over = True

    # enemy --- bullet collision
    for bullet in bullets:
        for enemy in enemies:
            offset = (bullet.rect.x - enemy.rect.x, bullet.rect.y - enemy.rect.y)
            if enemy.mask.overlap(bullet.mask, offset):
                if not enemy.is_falling:
                    enemy.start_shot()
                    score += 20
                bullets.remove(bullet)
                break

    # enemies - update and draw
    for enemy in enemies[:]:
        if enemy.is_shot:
            enemy.move()
            enemy.update_shot()
        elif enemy.is_falling:
            enemy.update_falling()
            enemy.move()
        else:
            enemy.move()
        enemy.draw(screen)
    # if enemy offscreen
    for enemy in enemies[:]:
        if enemy.rect.y > screen_height + enemy.rect.height:
            enemies.remove(enemy)

    # giant enemy spawn
    i = random.randint(1, 700)
    if i == 1 :
        giant_enemy = Giant_Enemy(50, 100)
        giant_enemies.append(giant_enemy)
    # giant enemy move
    for giant_enemy in giant_enemies:
        if giant_enemy.is_off_screen_x(screen_width):
            giant_enemies.remove(giant_enemy)
        else:
            giant_enemy.move()
            giant_enemy.draw(screen)
    # giant enemy --- bullet collision
    for giant_enemy in giant_enemies:
        for bullet in bullets:
            offset = (bullet.rect.x - giant_enemy.rect.x, bullet.rect.y - giant_enemy.rect.y)
            if giant_enemy.mask.overlap(bullet.mask, offset):
                if not giant_enemy.is_falling:
                    giant_enemy.start_shot()
                    score += random.randint(50, 350)
                bullets.remove(bullet)
                break
    # giant enemy ---- player collision
    for giant_enemy in giant_enemies:
        offset = (player.rect.x - giant_enemy.rect.x, player.rect.y - giant_enemy.rect.y)
        if giant_enemy.mask.overlap(player.mask, offset):
            if not shield:
                player.health -= 60
            giant_enemy.rect.y += player.rect.height + 10 + giant_enemy.rect.height
    # draw and update giant enemy
    for giant_enemy in giant_enemies:
        if giant_enemy.is_shot:
            giant_enemy.move()
            giant_enemy.update_shot()
        elif giant_enemy.is_falling:
            giant_enemy.update_falling()
            giant_enemy.move()
        else:
            giant_enemy.move()
    # if giant enemy offscreen
    for giant_enemy in giant_enemies:
        if giant_enemy.is_off_screen(screen_height):
            giant_enemies.remove(giant_enemy)
    # checks for win
    if not enemies and not giant_enemies:
        player.health += 50
        level += 1
        spawn_enemies()
        chosen_ability = random.choice(list(abilities.keys()))
        availible_abilities.append(chosen_ability)  # Add to available abilities list

    # Draw GUI (points and level)
    draw_top_gui(screen, score, level, high_score, screen_width)
    draw_available_abilities(screen, availible_abilities, screen_height)

    # highscore
    if score > high_score:
        high_score = int(score)
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
    # abilities
    if active_abilities:
        for ability in list(active_abilities.keys()):  # Iterate over a copy of keys
            if active_abilities[ability] <= 0:
                del active_abilities[ability]  # Remove from dictionary
                if ability == "shield":
                    shield = False
                elif ability == "double_fire":
                    double_fire = False
                elif ability == "time_warp":
                    for enemy in enemies:
                        enemy.speed = 2.5
                    for giant_enemy in giant_enemies:
                        giant_enemy.speed = 2.5
                elif ability == "bomb":
                    if ability in bomb_triggered:
                        del bomb_triggered[ability]

            else:
                active_abilities[ability] -= 1 / 60
                if ability == "time_warp":
                    for enemy in enemies:
                        enemy.speed = 0
                    for giant_enemy in giant_enemies:
                        giant_enemy.speed = 0
                elif ability == "double_fire":
                    double_fire = True
                elif ability == "bomb":
                    # Only trigger bomb once
                    if ability not in bomb_triggered or not bomb_triggered[ability]:
                        for enemy in enemies:
                            if not enemy.is_falling:
                                enemy.start_shot()
                        for giant_enemy in giant_enemies:
                            if not giant_enemy.is_falling:
                                giant_enemy.start_shot()
                        bomb_triggered[ability] = True
                elif ability == "shield":
                    shield = True

    # screen
    pygame.display.update()
    clock.tick(60)