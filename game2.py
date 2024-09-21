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
player_speed = 5  # Controls how fast the player moves left and right

on_ground = True  # Track if the player is on the ground

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get all keys that are pressed
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        player_xspeed = -player_speed  # Move left
    elif keys[pygame.K_RIGHT]:
        player_xspeed = player_speed  # Move right
    else:
        player_xspeed = 0  # Stop moving horizontally when no keys are pressed

    # Jumping with the up arrow key, only if on the ground
    if keys[pygame.K_UP] and on_ground:
        player_gravity = -20
        on_ground = False

    # Apply gravity
    player_gravity += 1
    player_rect.y += player_gravity

    # Ensure the player stays on the ground
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
        player_gravity = 0  # Reset gravity when on the ground
        on_ground = True

    # Update player horizontal position
    player_rect.x += player_xspeed

    # Screen wrapping for horizontal movement
    if player_rect.left >= 800:
        player_rect.right = 0
    if player_rect.right <= 0:
        player_rect.left = 800

    # Draw the background, ground, and player
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    screen.blit(score_surf, score_rect)

    # Move the snail
    snail_rect.x -= 4
    screen.blit(snail_surf, snail_rect)
    if snail_rect.right <= 0:
        snail_rect.left = 800

    # Draw the player
    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)
