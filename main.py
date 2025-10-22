from player import *
from bullets import *
from enemy import *
from bombs import *
import random

# dev note
# to make the bullet go oblique make the function:
# f(x) = ax + b
# formula for the bullet:
# f(x) = 46.6x - 98.969

#clock
clock = pygame.time.Clock()
# screen/background
screen_width, screen_height = 750, 750
screen = pygame.display.set_mode((screen_width, screen_height))
image_sky = pygame.image.load("assets/space_background.png")
pygame.display.set_caption("Space Invader")
def background_sky():
    bg = pygame.transform.scale(image_sky, (screen_width, screen_height))
    screen.blit(bg, (0, 0))
# player
player = Player(screen_width / 2, 600)
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
                    bullets.append(Bullet(player.rect.centerx, player.rect.top, -player.rotation_angle))
                else:
                    if all(bullet.time >= 35 for bullet in bullets):
                        bullets.append(Bullet(player.rect.centerx, player.rect.top, -player.rotation_angle))


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
        offset = (player.rect.x - bomb.rect.x, player.rect.y - bomb.rect.y)
        if player.mask.overlap(bomb.mask, offset):
            player.health -= 20
            bombs.remove(bomb)

    # player
    player.draw(screen)
    # player --- enemy collision
    for enemy in enemies[:]:
        offset = (player.rect.x - enemy.rect.x, player.rect.y - enemy.rect.y)
        if enemy.mask.overlap(player.mask, offset):
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
                enemy.start_shot()
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
        
    # screen
    pygame.display.update()
    # clock
    clock.tick(60)
