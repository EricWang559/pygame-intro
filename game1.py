import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('My game', False, 'Black')
score_rect = score_surf.get_rect(center = (400,50))
snail_surf = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

player_surf = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        ''' MOUSE STUFF
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
            if player_rect.collidepoint(event.pos) : print('collision')
        if event.type == pygame.MOUSEBUTTONUP:
            print('mouse up')
        '''
        
        # ARROW STUFF
        if event.type == pygame.KEYUP:
            player_rect.y += 1
        if event.type == pygame.KEYDOWN:
            player_rect.y -= 1

    #blit = block image transfer
    screen.blit(sky_surf, (0,0)) 
    screen.blit(ground_surf, (0,300))
    pygame.draw.rect(screen, 'Pink', score_rect)
    screen.blit(score_surf, score_rect)

    snail_rect.x -= 4
    screen.blit(snail_surf, snail_rect)
    if snail_rect.right <= 0: snail_rect.left = 800
    #print(player_rect.left)
    screen.blit(player_surf,player_rect)

    '''
    if (player_rect.colliderect(snail_rect)):
        print('Collision happening')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print('collision')
    print(pygame.mouse.get_pressed())
    '''

    pygame.display.update()
    clock.tick(60) #framerate = 60

     