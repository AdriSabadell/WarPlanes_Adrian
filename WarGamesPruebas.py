import pygame
import pygame.freetype
import random

FPS = 60
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
PLAYER_VEL = 7
PLAYER_POWER_VEL = 10
BULLET_SPEED = 13  
ENEMY_SPEED = 5
ENEMY_GENERATION_INTERVAL = 1500
CLOUD_SPEED = 1
CLOUD_GENERATOR_INTERVAL = 5000
POWER_UP_GENERATION_INTERVAL = 10000
POWER_SPEED = 3
TOTAL_TIME = 60
ENEMY_SPEED_BOSS = 8
ENEMY_BOSS_GENERATION_INTERVAL = 4250
ORIGINAL_BULLET_SPEED = BULLET_SPEED
POWER_UP_DURATION = 10000  # Duración en milisegundos (10 segundos)
power_up_active = False
power_up_start_time = 0

# game states
GAME_STATE_MENU = 1
GAME_STATE_PLAYING1 = 2
GAME_STATE_WIN = 3
GAME_STATE_LOOSE = 4
GAME_STATE_EXIT = 5
GAME_STATE_PLAYING2 = 6
GAME_STATE_VICTORY = 7



def move_player(player):
    global PLAYER_VEL, power_up_active, power_up_start_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player['x'] > 0:
        player['x'] -= (PLAYER_POWER_VEL if power_up_active else PLAYER_VEL)
        player['moving_left'] = True
        player['moving_right'] = False
    elif keys[pygame.K_RIGHT] and player['x'] < WINDOW_SIZE_X - 75:
        player['x'] += (PLAYER_POWER_VEL if power_up_active else PLAYER_VEL)
        player['moving_left'] = False
        player['moving_right'] = True
    else:
        # El jugador no se está moviendo en ninguna dirección
        player['moving_left'] = False
        player['moving_right'] = False

player_images = {
    'idle': pygame.image.load('images/pig/USA_plane.png'),
    'right': pygame.image.load('images/pig/USA_plane_der.png'),
    'left': pygame.image.load('images/pig/USA_plane_izq.png')
}


def draw_player(screen, player, bullets, enemy, cloud, power, boss):
    screen.fill((0, 128, 255))

    if player['moving_left']:
        sprite = player_images['left']
    elif player['moving_right']:
        sprite = player_images['right']
    else:
        sprite = player_images['idle']

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

    for obj in boss:
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

def update_boss(boss):
    for obj in boss:
        obj['y'] += ENEMY_SPEED_BOSS


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
    kill_sound = pygame.mixer.Sound('sounds/muerte_enemigo.mp3')
    for bullet in bullets:
        bullet_rect = bullet['image'].get_rect().move(bullet['x'], bullet['y'])
        for idx, enemy in enumerate(enemies):
            enemy_rect = enemy['image'].get_rect().move(enemy['x'], enemy['y'])
            if bullet_rect.colliderect(enemy_rect):
                bullets_to_remove.append(bullets.index(bullet))
                enemies_to_remove.append(idx)
                player['points'] += 1 
                kill_sound.play()
            
    for index in sorted(bullets_to_remove, reverse=True):
        del bullets[index]

    for index in sorted(enemies_to_remove, reverse=True):
        del enemies[index]

def kill_boss_enemy(bullets, bosses, player):
    bullets_to_remove = []
    boss_to_remove = []
    kill_sound = pygame.mixer.Sound('sounds/muerte_enemigo.mp3')
    for bullet in bullets:
        bullet_rect = bullet['image'].get_rect().move(bullet['x'], bullet['y'])
        for idx, boss in enumerate(bosses):
            boss_rect = boss['image'].get_rect().move(boss['x'], boss['y'])
            if bullet_rect.colliderect(boss_rect):
                bullets_to_remove.append(bullets.index(bullet))
                boss_to_remove.append(idx)
                player['points'] += 1 
                kill_sound.play()
            
    for index in sorted(bullets_to_remove, reverse=True):
        del bullets[index]

    for index in sorted(boss_to_remove, reverse=True):
        del bosses[index]




def draw_overlay(screen, font, player):
    font.render_to(screen, (50, 550), 'Puntuación: ' + str(player['points']))


def game_menu(screen):
    menu_music = pygame.mixer.Sound('sounds/Music.mp3')
    #title=pygame.image.load('images/menu/title.png')
    start_btn_light=pygame.image.load('images/menu/start_button.png')
    start_btn_dark=pygame.image.load('images/menu/start_buttondark.png')
    exit_btn_light=pygame.image.load('images/menu/exit_button.png')
    exit_btn_dark=pygame.image.load('images/menu/exit_buttondark.png')
    start_btn=start_btn_light
    exit_btn=exit_btn_light
    background=pygame.image.load('images/menu/fondo2.png')
    going=True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going=False
                result=GAME_STATE_EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                square=start_btn.get_rect().move(150, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_PLAYING1
                square=exit_btn.get_rect().move(450, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_EXIT
        square=start_btn.get_rect().move(150, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            start_btn=start_btn_dark
        else:
            start_btn=start_btn_light
        square=exit_btn.get_rect().move(450, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            exit_btn=exit_btn_dark
        else:
            exit_btn=exit_btn_light
        screen.blit(background, background.get_rect())
        #screen.blit(title, title.get_rect().move(400-352, 50))
        screen.blit(start_btn, start_btn.get_rect().move(150,500))
        screen.blit(exit_btn, exit_btn.get_rect().move(450,500))
        pygame.display.flip()
        menu_music.play()
    menu_music.stop()
    return result

def win_menu(screen):
    title=pygame.image.load('images/menu/title.png')
    start_btn_light=pygame.image.load('images/menu/start_button.png')
    start_btn_dark=pygame.image.load('images/menu/start_buttondark.png')
    exit_btn_light=pygame.image.load('images/menu/exit_button.png')
    exit_btn_dark=pygame.image.load('images/menu/exit_buttondark.png')
    start_btn=start_btn_light
    exit_btn=exit_btn_light
    background=pygame.image.load('images/menu/victoria.png')
    going=True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going=False
                result=GAME_STATE_EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                square=start_btn.get_rect().move(150, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_PLAYING2
                square=exit_btn.get_rect().move(450, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_EXIT
        square=start_btn.get_rect().move(150, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            start_btn=start_btn_dark
        else:
            start_btn=start_btn_light
        square=exit_btn.get_rect().move(450, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            exit_btn=exit_btn_dark
        else:
            exit_btn=exit_btn_light
        screen.blit(background, background.get_rect())
        screen.blit(title, title.get_rect().move(400-352, 50))
        screen.blit(start_btn, start_btn.get_rect().move(150,500))
        screen.blit(exit_btn, exit_btn.get_rect().move(450,500))
        pygame.display.flip()
        
    return result

def loose_menu(screen):
    loose_music = pygame.mixer.Sound('sounds/Lose_Music.mp3')
    #title=pygame.image.load('images/menu/title.png')
    start_btn_light=pygame.image.load('images/menu/start_button.png')
    start_btn_dark=pygame.image.load('images/menu/start_buttondark.png')
    exit_btn_light=pygame.image.load('images/menu/exit_button.png')
    exit_btn_dark=pygame.image.load('images/menu/exit_buttondark.png')
    start_btn=start_btn_light
    exit_btn=exit_btn_light
    background=pygame.image.load('images/menu/fondoloose.png')
    going=True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going=False
                result=GAME_STATE_EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                square=start_btn.get_rect().move(150, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_PLAYING1
                square=exit_btn.get_rect().move(450, 500)
                if square.collidepoint(pygame.mouse.get_pos()):
                    going=False
                    result=GAME_STATE_EXIT
        square=start_btn.get_rect().move(150, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            start_btn=start_btn_dark
        else:
            start_btn=start_btn_light
        square=exit_btn.get_rect().move(450, 500)
        if square.collidepoint(pygame.mouse.get_pos()):
            exit_btn=exit_btn_dark
        else:
            exit_btn=exit_btn_light
        screen.blit(background, background.get_rect())
        #screen.blit(title, title.get_rect().move(400-352, 50))
        screen.blit(start_btn, start_btn.get_rect().move(150,500))
        screen.blit(exit_btn, exit_btn.get_rect().move(450,500))
        pygame.display.flip()
        loose_music.play()
    loose_music.stop()
    return result

def game_playing1(screen):
    player = create_player()
    overlay_font = pygame.freetype.Font("fonts/Lato-Black.ttf", 32)

    shooting_sound = pygame.mixer.Sound('sounds/Shot.mp3')

    clock = pygame.time.Clock()
    going = True
    bullets = []
    enemy = []
    cloud = []
    power = []
    boss = []

    time_since_last_enemy = 0
    time_since_last_cloud = 0
    time_since_last_power = 0
    time_since_last_boss = 0

    global power_up_active, power_up_start_time

    while going:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
                result=GAME_STATE_MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shooting_sound.play()
                new_object = {
                    'image': pygame.image.load('images/pig/bullet.png'),
                    'x': player['x'] + 27,
                    'y': player['y'] - 25

                }
                bullets.append(new_object)

        move_player(player)
        update_bullets(bullets)
        update_enemy(enemy)
        update_boss(boss)
        update_cloud(cloud)
        update_power(power)
        kill_enemy(bullets, enemy, player)
        kill_boss_enemy(bullets, boss, player)

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

        if current_time - time_since_last_boss >= ENEMY_BOSS_GENERATION_INTERVAL:
            new_boss = {
                'image': pygame.image.load('images/pig/Japan_boss.png'),
                'x': random.randint(0, 750),
                'y': 0
                
            }
            boss.append(new_boss)
            time_since_last_boss = current_time
            print("Boss")

    

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
                'image': pygame.image.load('images/pig/power.png'),
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
                power_up_active = True
                power_up_start_time = current_time
                power.remove(p)

        # Desactivar power-up después de 10 segundos
        if power_up_active and current_time - power_up_start_time >= POWER_UP_DURATION:
            power_up_active = False

#Eliminar player con enemy
        for p in enemy:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡muerte!")
                enemy.remove(p)
                going = False
                result=GAME_STATE_LOOSE

#Eliminar player con boss
        for p in boss:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡muerte!")
                boss.remove(p)
                going = False
                result=GAME_STATE_LOOSE
        
        if player['points'] >= 10:
            going = False
            result = GAME_STATE_PLAYING2
        

        draw_player(screen, player, bullets, enemy, cloud, power, boss)
        draw_overlay(screen, overlay_font, player)
        pygame.display.flip()
        clock.tick(FPS)

    return result


def game_playing2(screen):
    player = create_player()
    overlay_font = pygame.freetype.Font("fonts/Lato-Black.ttf", 32)

    shooting_sound = pygame.mixer.Sound('sounds/Shot.mp3')

    clock = pygame.time.Clock()
    going = True
    bullets = []
    enemy = []
    cloud = []
    power = []
    boss = []

    time_since_last_enemy = 0
    time_since_last_cloud = 0
    time_since_last_power = 0
    time_since_last_boss = 0


    while going:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
                result=GAME_STATE_MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shooting_sound.play()
                new_object = {
                    'image': pygame.image.load('images/pig/bullet.png'),
                    'x': player['x'] + 27,
                    'y': player['y'] - 25

                }
                bullets.append(new_object)

        move_player(player)
        update_bullets(bullets)
        update_enemy(enemy)
        update_boss(boss)
        update_cloud(cloud)
        update_power(power)
        kill_enemy(bullets, enemy, player)
        kill_boss_enemy(bullets, boss, player)

        bullets = [bullet for bullet in bullets if bullet['y'] > 0]

        if current_time - time_since_last_enemy >= ENEMY_GENERATION_INTERVAL:
            new_enemy = {
                'image': pygame.image.load('images/pig/Japan_boss.png'),
                'x': random.randint(0, 750),
                'y': 0
            }
            enemy.append(new_enemy)
            time_since_last_enemy = current_time

        enemy = [enemy for enemy in enemy if enemy['y'] < 600]

        if current_time - time_since_last_boss >= ENEMY_BOSS_GENERATION_INTERVAL:
            new_boss = {
                'image': pygame.image.load('images/pig/Japan_plane.png'),
                'x': random.randint(0, 750),
                'y': 0
                
            }
            boss.append(new_boss)
            time_since_last_boss = current_time
            print("Boss")

    

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
                'image': pygame.image.load('images/pig/power.png'),
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

#Eliminar player con enemy
        for p in enemy:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡muerte!")
                enemy.remove(p)
                going = False
                result=GAME_STATE_LOOSE

#Eliminar player con boss
        for p in boss:
            power_rect = p['image'].get_rect().move(p['x'], p['y'])
            player_rect = player['right'].get_rect().move(player['x'], player['y'])

            if power_rect.colliderect(player_rect):
                print("¡muerte!")
                boss.remove(p)
                going = False
                result=GAME_STATE_LOOSE
        
        if player['points'] >= 20:
            going = False
            result = GAME_STATE_WIN
        

        draw_player(screen, player, bullets, enemy, cloud, power, boss)
        draw_overlay(screen, overlay_font, player)
        pygame.display.flip()
        clock.tick(FPS)

    return result


def main():
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_SIZE_X, WINDOW_SIZE_Y])
    game_icon = pygame.image.load('images/icon.png')


    
    pygame.display.set_caption('Exemple 5')
    pygame.display.set_icon(game_icon)


    game_state=GAME_STATE_MENU
    while game_state!=GAME_STATE_EXIT:
        if game_state==GAME_STATE_MENU:
            game_state=game_menu(screen)
        elif game_state==GAME_STATE_PLAYING1:
            game_state=game_playing1(screen)
        elif game_state==GAME_STATE_PLAYING2:
            game_state=game_playing2(screen)
        elif game_state==GAME_STATE_WIN:
            game_state=win_menu(screen)
        elif game_state==GAME_STATE_LOOSE:
            game_state=loose_menu(screen)

    pygame.quit()

main()