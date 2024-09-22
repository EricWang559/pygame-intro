import pygame
import random
from random import randint
from sys import exit
from time import sleep

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))

    pill_message_surf = test_font.render(f'Pills: {pill_count}',False,(64,64,64))
    pill_message_rect = pill_message_surf.get_rect(topright = (800, 0))
    
    screen.blit(score_surf,score_rect)
    screen.blit(pill_message_surf,pill_message_rect)
    #print(current_time)
    return current_time

score = 0

'''
def display_hp():
    hearts = 3
    heart_xpos = 0
    heart_surf = pygame.image.load('graphics/heart.png')
    heart_rect = heart_surf.get_rect(topleft = (0,heart_xpos))
    if player_rect.colliderect(snail_rect):
        hearts -=1

    for i in range (hearts):
        screen.blit(heart_surf, heart_rect)
        heart_xpos+=30
        heart_rect = heart_surf.get_rect(topleft = (0,heart_xpos))
        
'''

def draw_grid(x, y):
    for i in range(0,x,50):
        pygame.draw.line(screen, 'Black',(0,i),(x,i))
        pygame.draw.line(screen, 'Black',(i,0),(i,x))

# Initialize variables to store previous position, time, and the last print time
prev_x, prev_y = 0, 0
prev_time = pygame.time.get_ticks()
last_print_time = 0  # Time when the last position was printed

def showPos(player_rect):
    global prev_x, prev_y, prev_time, last_print_time
    
    # Get the current time and position
    current_time = pygame.time.get_ticks()
    current_x, current_y = player_rect.x, player_rect.y

    # Calculate time since the last print
    time_since_last_print = (current_time - last_print_time) / 1000  # Convert milliseconds to seconds

    if time_since_last_print >= 1:  # Check if 0.5 seconds have passed
        # Calculate time difference (in seconds for speed calculation)
        delta_time = (current_time - prev_time) / 1000  # Convert milliseconds to seconds

        if delta_time > 0:
            # Calculate the change in position
            delta_x = current_x - prev_x
            delta_y = current_y - prev_y
            
            # Calculate the instantaneous speed
            speed = ((delta_x ** 2 + delta_y ** 2) ** 0.5) / delta_time  # Speed in pixels per second

            # Print player position and speed
            print(f"Player position: ({current_x},{current_y}), Speed: {speed:.2f} pixels/second")
        
        # Update the last print time
        last_print_time = current_time

    # Update the previous position and time for the next frame
    prev_x, prev_y = current_x, current_y
    prev_time = current_time


def obstacle_movement(obstacle_list, os):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= os

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            elif obstacle_rect.bottom == 210:
                screen.blit(fly_surf, obstacle_rect)

            
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:  # Ensure there are obstacles to check
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):  # Check for collision
                print("Player hit an enemy!")  # Debugging print
                return False  # End the game on collision
    return True  # No collision, continue the game



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
#snail_rect = snail_surf.get_rect(bottomright = (600, 300))
snail_speed = 4

fly_surf = pygame.image.load('graphics/fly1.png').convert_alpha()

obstacle_rect_list = []
obstacle_speed = 5

player_surf = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
player_force = 0
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

scprinted = False
shopprinted = False
owprinted = False


pill_surf = pygame.image.load('graphics/pill.png').convert_alpha()
pill_rect = pill_surf.get_rect(midbottom = (int(random.randrange(250, 750)), (int(random.randrange(50, 300)))))
show_pill = True
pill_count = 0
pill_clicked = False
pill_got = False

numJump = 0

onGround = True
belowGround = False

#toggle modes
allow_x_movement = False
have_grid = False
show_pos_player = False
inf_jumps = False
borderOn = True
r_wall = 0

#screens
menu_screen = True
shop_screen = False

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


#Timer 2
pill_timer = pygame.USEREVENT + 2
def pillTimer():
    if player_rect.colliderect(pill_rect):
        pygame.time.set_timer(pill_timer, 3000)
    else:
        pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game Exited.")
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_h] or keys[pygame.K_RCTRL]:
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
                if keys[pygame.K_p] or keys[pygame.K_a]:
                    if show_pos_player:
                        show_pos_player = False
                    elif show_pos_player == False:
                        show_pos_player = True
                    print("show player pos: ", show_pos_player)
                if keys[pygame.K_t] or keys[pygame.K_s]:
                    inf_jumps = not inf_jumps
                    print("inf jumps on" if inf_jumps else "inf jumps off")
                if keys[pygame.K_o] or keys[pygame.K_d]:
                    borderOn = not borderOn
                    print("borders on" if borderOn else "borders off")
                if keys[pygame.K_i] or keys[pygame.K_f]:
                    if r_wall == 0:
                        r_wall = -200
                        print("walls off")
                    elif r_wall == -200:
                        r_wall = 0
                        print("walls on")
                if keys[pygame.K_RSHIFT]:
                    if obstacle_speed == 5:
                        obstacle_speed = 0
                        player_gravity = 0
                        print("obs speed off")
                    elif obstacle_speed == 0:
                        obstacle_speed = 5
                        player_force = 0
                        print("obs speed on")
                       

                if keys[pygame.K_r]:
                    game_active = False
                    menu_screen = True
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
                if obstacle_speed != 0:
                    if onGround:
                        player_gravity = -20
                    if inf_jumps:
                        player_gravity = -20
                else:
                    player_force = -5
            if(keys[pygame.K_DOWN]):
                if obstacle_speed == 0:
                    if player_gravity < 0:
                        player_gravity = 0
                    player_force = 5
            if keys[pygame.K_UP] and keys[pygame.K_DOWN] and obstacle_speed == 0:
                player_force = 0
            if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and obstacle_speed == 0:
                player_force = 0
           

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
                    #snail_rect.left = 800  # Reset the snail position
                    snail_speed = 4        # Reset snail speed
                    player_rect.midbottom = (80, 300) 
                    start_time = int(pygame.time.get_ticks() / 1000)
                    speed_factor = 1
                    show_pill = True
                    pill_got = False
                    pill_count = 0
                    pill_rect = pill_surf.get_rect(midbottom = (int(random.randrange(250, 750)), (int(random.randrange(50, 300)))))
                    scprinted = False
                    shopprinted = False
                    owprinted = False
                    player_force = 0

            if menu_screen:
                
                if not scprinted:
                    print("menu screen")
                    scprinted = True

            elif shop_screen:
                
                if not shopprinted:
                    print("shop screen")
                    shopprinted = True

        if event.type == obstacle_timer and game_active and obstacle_speed != 0:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (random.randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))
        if event.type == pill_timer:
            if not pill_got:
                speed_factor = 1
                print("pill effect up!")
                pill_got = False

    if game_active:
        #blit = block image transfer
        screen.blit(sky_surf, (0,0)) 
        screen.blit(ground_surf, (0,300))
        score = display_score()
        if(have_grid):
            draw_grid(800,400)
        if(show_pos_player):
            showPos(player_rect)

        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        
        #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))
        #pygame.draw.line(screen, 'Gold',(0,0),pygame.mouse.get_pos(),10)
        
        #screen.blit(score_surf, score_rect)

        '''
        snail_rect.x -= snail_speed
        screen.blit(snail_surf, snail_rect)
        if snail_rect.right <= 0: 
            snail_rect.left = 800
            if random.randint(0,2) == (1 or 2):
                show_pill = True
                pill_rect = pill_surf.get_rect(midbottom = (int(random.randrange(250, 750)), (int(random.randrange(50, 300)))))
        '''

        #print(player_rect.left)

        #pill
        if show_pill:
            screen.blit(pill_surf, pill_rect)
            pillTimer()
            if player_rect.colliderect(pill_rect):
                #peed_factor = 1.5
                pill_count+=1
                t1 = pygame.time.get_ticks()
                print(f"{pill_count} pills taken")
                show_pill = False
                pill_got = True
                

        #player
        if(obstacle_speed != 0):
            player_gravity += 1
        player_rect.y += player_gravity
        if obstacle_speed == 0:
            player_rect.y += player_force

        if(allow_x_movement):
            player_rect.x += player_xspeed

        #right wall
        if player_rect.left >= 800:
            print("border crossing at x > 800")
            player_rect.right = 0

        #left wall
        elif player_rect.right <= r_wall:
            print("border crossing at x < 0")
            player_rect.left = 800

        if not borderOn:
            #move to bottom ground
            if player_rect.bottom <= 0: 
                print("bottom ground crossing at x < 0")
                player_rect.bottom = 600
                belowGround = True
        elif borderOn:
            if player_rect.top <= 0:
                player_rect.top = 0
                if not owprinted:
                    owprinted = True
                    #print("ow you hit your head")
        
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
        if player_rect.bottom == 300 or player_rect.bottom == 400:
            onGround = True
            owprinted = False
        else:
            onGround = False
            owprinted = False
        

        screen.blit(player_surf,player_rect)

        #MOUSE
        mouse_pos = pygame.mouse.get_pos()
        
        if player_rect.collidepoint(mouse_pos):
            print("mouse on player")
        
        if pill_rect.collidepoint(mouse_pos):
            print("mouse on pill")

        '''
        if snail_rect.collidepoint(mouse_pos):
            print("mouse on snail")
        '''

        #obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list, obstacle_speed)

        
        # collisions
        game_active = collisions(player_rect, obstacle_rect_list)
                
        
        
        if pill_clicked:
            print('click')
            game_active = False
            shop_screen = True
            menu_screen = False
            pill_clicked = False


    else: #INTRO/MENU SCREEN
        if menu_screen:
            screen.fill((94,129,162))
            screen.blit(player_stand, player_stand_rect)
            obstacle_rect_list.clear()

            score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(game_name, game_name_rect)

            pill_message = test_font.render(f"Pills eaten: {pill_count}", False, (111,196,169))
            pill_message_rect = pill_message.get_rect(center = (400, 360))

            if score == 0:
                screen.blit(game_message, game_message_rect)
            else:
                screen.blit(score_message, score_message_rect)
                screen.blit(pill_message, pill_message_rect)
        elif shop_screen: #shop screen
            screen.fill((255,255,255))
        else: #dead screen
            screen.fill('Black')
            

    pygame.display.update()
    clock.tick(60) #framerate = 60