import pygame
import sys
def display_score():
    time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = text_font.render(f'Score: {time}',False,(65,65,65))
    score_rect = score_surf.get_rect(center=(720,50))
    screen.blit(score_surf,score_rect)
    return time

    
pygame.init()

screen = pygame.display.set_mode((800,400))  # this is to make base screen/ basic surface on which we will do the work

pygame.display.set_caption('Maze Runner') # this is to change the name of the screen

clock = pygame.time.Clock()  # this is the clock which will help in fixing the frame

text_font = pygame.font.Font('font/Pixeltype.ttf',50) # this will collect the text properties from pygame and will put it into variable text_font
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# text_surface = text_font.render('Score',False,(65,65,70)) 
# text_rect = text_surface.get_rect(center=(400,50))
game_over1_surf = text_font.render('Mr. Jumpy',False,(111,196,169))
game_over1_rect = game_over1_surf.get_rect(center=(400,50))
game_over2_surf =  text_font.render("Press Enter to Start",False,(111,196,169))
game_over2_rect = game_over2_surf.get_rect(center=(400,350))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800,300))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80,300))
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png')
player_stand_surf= pygame.transform.scale2x(player_stand_surf)
player_stand_rect = player_stand_surf.get_rect(center=(400,200))

player_gravity = 0  
game_status = True
start_time =0

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit() # this is the opposite of the pygame.init()
            sys.exit() # this will stop the code to run update command
        

        if player_rect.bottom <=300 and player_rect.bottom >=150 and game_status:

            if events.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(events.pos):
                    player_gravity=-20

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    player_gravity =-20

        if events.type == pygame.KEYDOWN and not game_status:
            if events.key == pygame.K_SPACE:
                game_status=True
                snail_rect.right = 800
                start_time = pygame.time.get_ticks()

    if game_status:
           
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen,'#c0e8ec',text_rect)
        # pygame.draw.rect(screen,'#c0e8ec',text_rect,10,2)

        #screen.blit(text_surface,text_rect)
        score = display_score()
        snail_rect.right -=6
        if snail_rect.left <= -100:
            snail_rect.right = 800

        player_gravity+=1
        player_rect.y +=player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom=300
        
        if snail_rect.colliderect(player_rect):
                game_status=False
        
        screen.blit(snail_surface,snail_rect)
        screen.blit(player_surface,player_rect)
    else:
        screen.fill((94,129,162))     
        screen.blit(game_over1_surf,game_over1_rect)
        screen.blit(player_stand_surf,player_stand_rect)
        score_surf = text_font.render(f'Your Score: {score}',False,(111,196,169))
        score_rect = score_surf.get_rect(center=(400,350))
        if score ==0:
            screen.blit(game_over2_surf,game_over2_rect)
        else:
            screen.blit(score_surf,score_rect)



    pygame.display.update()
    clock.tick(60) # this tells the loop not to run more then 60 per seconds
