import pygame
import sys

pygame.init()

#setting window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((173, 216, 230))
pygame.display.set_caption("CrabHacks 2025")

#game loop
clock = pygame.time.Clock()

#player settings
crab_size = 40
crab_speed = 5
crab = pygame.Rect(WIDTH // 2, HEIGHT // 2, crab_size, crab_size)
#crab = pygame.image.load()

while True:

    #handle events here
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #PLAYER
    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        crab.x -= crab_speed
    if keys[pygame.K_RIGHT]:
        crab.x += crab_speed
    if keys[pygame.K_UP]:
        crab.y -= crab_speed
    if keys[pygame.K_DOWN]:
        crab.y += crab_speed
    
    #keep player inside screen
    crab.x = max(0, min(crab.x, WIDTH - crab_size))
    crab.y = max(0, min(crab.y, HEIGHT - crab_size))
    
    #GAME SETTINGS 
    #update screen
    screen.fill((173, 216, 230))
    pygame.draw.rect(screen, (255, 120, 0), crab)
    #screen.blit(crab_image, crab)
    pygame.display.flip()

    #control frames per second, basically how fast the game runs
    clock.tick(60)

    