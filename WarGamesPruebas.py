import pygame 
import random

FPS = 60
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
PLAYER_VEL = 7
BULLET_SPEED = 15  
ENEMY_SPEED  = 5
ENEMY_GENERATION_INTERVAL = 1500

def move_player(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player['x'] > 0:
        player['x'] -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player['x'] < WINDOW_SIZE_X - 75:
        player['x'] += PLAYER_VEL

def draw_player(screen, player, bullets, enemy):#enemy
    screen.fill((0, 128, 255))  
    sprite = player['right']
    square = sprite.get_rect().move(player['x'], player['y'])
    screen.blit(sprite, square)

    for obj in bullets:
        screen.blit(obj['image'], (obj['x'], obj['y']))
#Enemigos
    for obj in enemy:
        screen.blit(obj['image'], (obj['x'], obj['y']))

def update_bullets(bullets):
    for obj in bullets:
        obj['y'] -= BULLET_SPEED 
#Enemigos
def update_enemy(enemy):
    for obj in enemy:
        obj['y'] += ENEMY_SPEED 


def create_player():
    player = {
        'right': pygame.image.load('images/pig/USA_plane.png'),
        'x': 400 - 27,
        'y': 525 - 15
    }
    return player


def main():
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_SIZE_X, WINDOW_SIZE_Y])
    game_icon = pygame.image.load('images/icon.png')
    player = create_player()

    pygame.display.set_caption('Exemple 5')
    pygame.display.set_icon(game_icon)

    clock = pygame.time.Clock()
    going = True
    bullets = []  # Lista para almacenar los objetos generados
    enemy = []
    time_since_last_enemy = 0
    while going:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Genera un objeto encima del jugador
                new_object = {
                    'image': pygame.image.load('images/pig/bullet.png'),
                    'x': player['x'] + 27,
                    'y': player['y'] - 25
                }
                bullets.append(new_object)  # Agrega el objeto a la lista

        move_player(player)
        update_bullets(bullets)  
        update_enemy(enemy)

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

        draw_player(screen, player, bullets, enemy)
        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()

if __name__ == "__main__":
    main()
