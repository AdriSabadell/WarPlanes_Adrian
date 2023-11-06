import pygame
import pygame.freetype
import random

FPS = 60
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
PLAYER_VEL = 7
BULLET_SPEED = 15  
ENEMY_SPEED = 5
ENEMY_GENERATION_INTERVAL = 1500
CLOUD_SPEED = 1
CLOUD_GENERATOR_INTERVAL = 5000
POWER_UP_GENERATION_INTERVAL = 10000
POWER_SPEED = 3

# game states
GAME_STATE_MENU = 1
GAME_STATE_PLAYING = 2
GAME_STATE_RESULTS = 3
GAME_STATE_EXIT = 4

def move_player(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player['x'] > 0:
        player['x'] -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player['x'] < WINDOW_SIZE_X - 75:
        player['x'] += PLAYER_VEL

def draw_player(screen, player, bullets, enemy, cloud, power):
    screen.fill((0, 128, 255))
    sprite = player['right']
    square = sprite.get_rect().move(player['x'], player['y'])

    for obj in cloud:
        screen.blit(obj['image'], (obj['x'], obj['y']))

    screen.blit(sprite, square)

    for obj in bullets:
        screen.blit(obj['image'], (obj['x'], obj['y']))

    for obj in enemy:
        screen.blit(obj['image'], (obj['x'], obj['y']))

    for obj in power:
        screen.blit(obj['image'], (obj['x'], obj['y']))

def update_bullets(bullets):
    for obj in bullets:
        obj['y'] -= BULLET_SPEED

def update_enemy(enemy):
    for obj in enemy:
        obj['y'] += ENEMY_SPEED

def update_cloud(cloud):
    for obj in cloud:
        obj['y'] += CLOUD_SPEED
        
def update_power(power):
    for obj in power:
        obj['y'] += POWER_SPEED

def create_player():
    player = {
        'right': pygame.image.load('images/pig/USA_plane.png'),
        'x': 400 - 27,
        'y': 525 - 15,
        'points': 0
    }
    return player

def kill_enemy(bullets, enemies, player):
    bullets_to_remove = []
    enemies_to_remove = []
    for bullet in bullets:
        bullet_rect = bullet['image'].get_rect().move(bullet['x'], bullet['y'])
        for idx, enemy in enumerate(enemies):
            enemy_rect = enemy['image'].get_rect().move(enemy['x'], enemy['y'])
            if bullet_rect.colliderect(enemy_rect):
                bullets_to_remove.append(bullets.index(bullet))
                enemies_to_remove.append(idx)
                player['points'] += 1  # Aumenta la puntuación al eliminar un enemigo

    for index in sorted(bullets_to_remove, reverse=True):
        del bullets[index]

    for index in sorted(enemies_to_remove, reverse=True):
        del enemies[index]



def draw_overlay(screen, font, player):
    font.render_to(screen, (50, 550), 'Puntuación: ' + str(player['points']))

def main():
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_SIZE_X, WINDOW_SIZE_Y])
    game_icon = pygame.image.load('images/icon.png')
    player = create_player()

    overlay_font = pygame.freetype.Font("fonts/Lato-Black.ttf", 32)

    pygame.display.set_caption('Exemple 5')
    pygame.display.set_icon(game_icon)

    clock = pygame.time.Clock()
    going = True
    bullets = []
    enemy = []
    cloud = []
    power = []

    time_since_last_enemy = 0
    time_since_last_cloud = 0
    time_since_last_power = 0


    while going:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                new_object = {
                    'image': pygame.image.load('images/pig/bullet.png'),
                    'x': player['x'] + 27,
                    'y': player['y'] - 25
                }
                bullets.append(new_object)

        move_player(player)
        update_bullets(bullets)
        update_enemy(enemy)
        update_cloud(cloud)
        update_power(power)
        kill_enemy(bullets, enemy, player)


        bullets = [bullet for bullet in bullets if bullet['y'] > 0]

        if current_time - time_since_last_enemy >= ENEMY_GENERATION_INTERVAL:
            new_enemy = {
                'image': pygame.image.load('images/pig/Japan_plane.png'),
                'x': random.randint(0, 750),
                'y': 0
            }
            enemy.append(new_enemy)
            time_since_last_enemy = current_time

        enemy = [enemy for enemy in enemy if enemy['y'] < 600]

        if current_time - time_since_last_cloud >= CLOUD_GENERATOR_INTERVAL:
            new_cloud = {
                'image': pygame.image.load('images/pig/cloud.png'),
                'x': random.randint(0, 750),
                'y': 0
            }
            cloud.append(new_cloud)
            time_since_last_cloud = current_time

        cloud = [cloud for cloud in cloud if cloud['y'] < 600]

        if current_time - time_since_last_power >= POWER_UP_GENERATION_INTERVAL:
            new_power = {
                'image': pygame.image.load('images/pig/down1.png'),
                'x': random.randint(0, 750),
                'y': 0
            }
            power.append(new_power)
            time_since_last_power = current_time

        power = [power for power in power if power['y'] < 600]
#Eliminar power up
        for p in power:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡power-up!")
                power.remove(p)

#Eliminar enemy
        for p in enemy:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡muerte!")
                enemy.remove(p)


        

        draw_player(screen, player, bullets, enemy, cloud, power)
        draw_overlay(screen, overlay_font, player)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()