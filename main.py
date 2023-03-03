import pygame
import sys
pygame.init()

screen = pygame.display.set_mode((800,400))  # this is to make base screen/ basic surface on which we will do the work

pygame.display.set_caption('Maze Runner') # this is to change the name of the screen

clock = pygame.time.Clock()  # this is the clock which will help in fixing the frame

text_font = pygame.font.Font('font/Pixeltype.ttf',50) # this will collect the text properties from pygame and will put it into variable text_font
#test_surface = pygame.Surface((100,200))
#test_surface.fill('Blue')
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

text_surface = text_font.render('Score',False,(65,65,70)) 
text_rect = text_surface.get_rect(center=(400,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800,300))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))

player_gravity = 0  
point =0

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit() # this is the opposite of the pygame.init()
            sys.exit() # this will stop the code to run update command
        

        if player_rect.bottom ==300:

            if events.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(events.pos):
                    player_gravity=-20

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    player_gravity =-20
        
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen,'#c0e8ec',text_rect)
    pygame.draw.rect(screen,'#c0e8ec',text_rect,10,2)

    screen.blit(text_surface,text_rect)
    snail_rect.right -=4
    if snail_rect.left <= -100:
        snail_rect.right = 800

    player_gravity+=1
    player_rect.y +=player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom=300
    
    if snail_rect.colliderect(player_rect):
            point+=1
    print(point)
    screen.blit(snail_surface,snail_rect)
    screen.blit(player_surface,player_rect)




    pygame.display.update()
    clock.tick(60) # this tells the loop not to run more then 60 per seconds
