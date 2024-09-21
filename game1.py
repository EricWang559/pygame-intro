import pygame
import random
from sys import exit
from time import sleep

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    #print(current_time)
    return current_time

score = 0

def draw_grid(x, y):
    for i in range(0,x,50):
        pygame.draw.line(screen, 'Black',(0,i),(x,i))
        pygame.draw.line(screen, 'Black',(i,0),(i,x))

def showPos():
    ct = pygame.time.get_ticks()
    if ct % 60 == 0:
        print("player position: ", player_rect.x)
        print("snail position: ", snail_rect.x)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

game_active = False #Show loading screen first

start_time = 0
global_time = pygame.time.get_ticks()


sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#score_surf = test_font.render('My game', False, (64,64,64))
#score_rect = score_surf.get_rect(center = (400,50))
snail_surf = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300))
snail_speed = 4

player_surf = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
player_xspeed = 0
speed_factor = 1

#INTRO SCREEN
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
#player_stand = pygame.transform.scale(player_stand, (200,400))
#player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

pill_surf = pygame.image.load('graphics/pill.png').convert_alpha()
pill_rect = pill_surf.get_rect(midtop = (int(random.randrange(250, 750)), (int(random.randrange(0, 300)))))
show_pill = True
pill_count = 0
pill_clicked = False

numJump = 0

onGround = True
belowGround = False

#toggle modes
allow_x_movement = True
have_grid = False
show_pos_player = False
inf_jumps = False

#screens
snail_screen = True
shop_screen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game Exited.")
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_h]:
                    if allow_x_movement:
                        allow_x_movement = False
                    elif allow_x_movement == False:
                        allow_x_movement = True
                    print("x mvmt: ", allow_x_movement)
                if keys[pygame.K_g]:
                    if have_grid:
                        have_grid = False
                    elif have_grid == False:
                        have_grid = True
                    print("grid: ", have_grid)
                if keys[pygame.K_p]:
                    if show_pos_player:
                        show_pos_player = False
                    elif show_pos_player == False:
                        show_pos_player = True
                    print("show player pos: ", show_pos_player)
                if keys[pygame.K_t]:
                    inf_jumps = not inf_jumps
                    print("inf jumps on")

                if keys[pygame.K_r]:
                    game_active = False
                    sleep(0.1)
                    snail_screen = True
                if keys[pygame.K_q]:
                    print("Game Exited through Q.")
                    exit()
            
            # Horizontal movement
            if keys[pygame.K_LEFT]:
                player_xspeed = -5 * speed_factor  # Move left
            if keys[pygame.K_RIGHT]:
                player_xspeed = 5 * speed_factor # Move right
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                player_xspeed = 0
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                player_xspeed = 0
                
            # Jumping with the up arrow key, only if on the ground
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                if onGround:
                    player_gravity = -20
                if inf_jumps:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
                if pill_rect.collidepoint(event.pos):
                    pill_clicked = True

            '''
            if event.type == pygame.KEYUP:
                print('key up')
            '''
            
            ''' MOUSE STUFF
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
                if player_rect.collidepoint(event.pos) : print('collision')
            if event.type == pygame.MOUSEBUTTONUP:
                print('mouse up')
            '''
            '''
            # ARROW STUFF
            if event.type == pygame.KEYUP:
                player_rect.y += 1
            if event.type == pygame.KEYDOWN:
                player_rect.y -= 1
            '''
        else:
            if event.type == pygame.KEYDOWN:
                if not game_active:
                    game_active = True
                    snail_rect.left = 800  # Reset the snail position
                    snail_speed = 4        # Reset snail speed
                    player_rect.midbottom = (80, 300) 
                    start_time = int(pygame.time.get_ticks() / 1000)
                    speed_factor = 1
                    show_pill = True
                    pill_rect = pill_surf.get_rect(midtop = (int(random.randrange(250, 750)), (int(random.randrange(0, 300)))))
            
            if snail_screen:
                print("snail screen")
            elif shop_screen:
                print("shop screen")
    
    if game_active:
        #blit = block image transfer
        screen.blit(sky_surf, (0,0)) 
        screen.blit(ground_surf, (0,300))
        score = display_score()
        if(have_grid):
            draw_grid(800,400)
        if(show_pos_player):
            showPos()

        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        
        #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))
        #pygame.draw.line(screen, 'Gold',(0,0),pygame.mouse.get_pos(),10)
        
        #screen.blit(score_surf, score_rect)

        snail_rect.x -= snail_speed
        screen.blit(snail_surf, snail_rect)
        if snail_rect.right <= 0: 
            snail_rect.left = 800
            if random.randint(0,2) == 1:
                show_pill = True
                pill_rect = pill_surf.get_rect(midtop = (int(random.randrange(250, 750)), (int(random.randrange(0, 300)))))
            
        #print(player_rect.left)

        #pill
        if show_pill:
            t1 = 0
            screen.blit(pill_surf, pill_rect)
            if player_rect.colliderect(pill_rect):
                #speed_factor = 0.5
                pill_count+=1
                t1 = pygame.time.get_ticks()
                print(f"{pill_count} pills taken")
                show_pill = False
            if pygame.time.get_ticks() - t1 == 1000 and t1 != 0:
                speed_factor = 1 

        #player
        player_gravity += 1
        player_rect.y += player_gravity

        if(allow_x_movement):
            player_rect.x += player_xspeed

        #right wall
        if player_rect.left >= 800:
            print("border crossing at x > 800")
            player_rect.right = 0

        #left wall
        elif player_rect.right <= 0:
            print("border crossing at x < 0")
            player_rect.left = 800

        #move to bottom ground
        if player_rect.bottom <= 0: 
            print("bottom ground crossing at x < 0")
            player_rect.bottom = 600
            belowGround = True
        
        #top ground 
        if player_rect.bottom >= 300 and not belowGround: 
            player_rect.bottom = 300

        #bottom ground
        elif belowGround and player_rect.bottom > 400:
            player_rect.bottom = 400
        
        #back on top ground
        if player_rect.bottom <= 300 and player_rect.bottom >= 0:
            belowGround = False
        
        #check if on ground
        if player_rect.bottom == 300:
            onGround = True
        else:
            onGround = False

        screen.blit(player_surf,player_rect)

        #MOUSE
        mouse_pos = pygame.mouse.get_pos()
        
        if player_rect.collidepoint(mouse_pos):
            print("mouse on player")
        
        if pill_rect.collidepoint(mouse_pos):
            print("mouse on pill")

        if snail_rect.collidepoint(mouse_pos):
            print("mouse on snail")

        if pill_clicked:
            print('click')
            game_active = False
            shop_screen = True
        
        if (player_rect.colliderect(snail_rect)):
            game_active = False
            snail_screen = True
            pill_count+=1


    else: #INTRO/MENU SCREEN
        if snail_screen:
            screen.fill((94,129,162))
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        elif shop_screen: #shop screen
            screen.fill((255,255,255))
        else: #dead screen
            screen.fill('Black')
            

    pygame.display.update()
    clock.tick(60) #framerate = 60