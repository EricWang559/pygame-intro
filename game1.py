import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('My game', False, (64,64,64))
score_rect = score_surf.get_rect(center = (400,50))
snail_surf = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

player_surf = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
player_xspeed = 0
numJump = 0

onGround = True
belowGround = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or pygame.K_UP) and onGround:
                numJump+=1
                print(f'jump {numJump}')
                player_gravity = -20

                if event.key == pygame.K_LEFT:
                    player_xspeed = -7  # Move left
                if event.key == pygame.K_RIGHT:
                    player_xspeed = 7   # Move right

            if event.key == pygame.K_LEFT:
                player_xspeed = -7  # Move left
                if onGround:
                    player_gravity = 0

            if event.key == pygame.K_RIGHT:
                player_xspeed = 7   # Move right
                if onGround:
                    player_gravity = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player_xspeed = 0


        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20

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

    #blit = block image transfer
    screen.blit(sky_surf, (0,0)) 
    screen.blit(ground_surf, (0,300))
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
    
    #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))
    #pygame.draw.line(screen, 'Gold',(0,0),pygame.mouse.get_pos(),10)
    
    screen.blit(score_surf, score_rect)

    snail_rect.x -= 4
    screen.blit(snail_surf, snail_rect)
    if snail_rect.right <= 0: snail_rect.left = 800
    #print(player_rect.left)

    #player
    player_gravity += 1
    player_rect.y += player_gravity

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
    

    '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print('jump')
    
    if (player_rect.colliderect(snail_rect)):
        print('Collision happening')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print('collision')
    print(pygame.mouse.get_pressed())
    '''

    pygame.display.update()
    clock.tick(60) #framerate = 60

     