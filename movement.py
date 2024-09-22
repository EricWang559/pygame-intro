import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((500,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

game_active = True
player_xspeed = 0
player_yspeed = 0

player = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_rect = player.get_rect(center = (250,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game Exited.")
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()
            exit()

        if game_active:
            # Horizontal movement
            if keys[pygame.K_LEFT]:
                player_xspeed = -5  # Move left
            if keys[pygame.K_RIGHT]:
                player_xspeed = 5 # Move right
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                player_xspeed = 0
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                player_xspeed = 0
                    
            # Jumping with the up arrow key, only if on the ground
            if (keys[pygame.K_UP]):
                player_yspeed = -5
            if(keys[pygame.K_DOWN]):
                player_yspeed = 5
            if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
                player_yspeed = 0
            if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                player_yspeed = 0
        else:
            pass
        
    if game_active:
            screen.fill('Light Blue')

            player_rect.x += player_xspeed
            player_rect.y += player_yspeed

            if player_rect.bottom <= 0:
                player_rect.bottom = 400
            elif player_rect.top >= 400:
                player_rect.top = 0
            if player_rect.left >= 500:
                player_rect.left = 0
            elif player_rect.right <= 0:
                player_rect.right = 500


            screen.blit(player, player_rect)

    pygame.display.update()
    clock.tick(60) #framerate = 60