import pygame
import sys
from random import randint

#display score
def display_score():
    time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = text_font.render(f'Score: {time}',False,(65,65,65))
    score_rect = score_surf.get_rect(center=(720,50))
    screen.blit(score_surf,score_rect)
    return time

# obstacle
def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle in obstacle_rect_list:
            obstacle.right -=6
            if obstacle.bottom == 300:
                screen.blit(snail_surface,obstacle)
            else:
                screen.blit(fly_surf,obstacle)
        obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.right >=-100]
        return obstacle_rect_list
    return []

 # collition   
def collitions(player,obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle in obstacle_rect_list:
            if player.colliderect(obstacle):
                return False
    return True
    
pygame.init()

#variables
screen = pygame.display.set_mode((800,400))  # this is to make base screen/ basic surface on which we will do the work
pygame.display.set_caption('Mr. Jumpy') # this is to change the name of the screen
clock = pygame.time.Clock()  # this is the clock which will help in fixing the frame
player_gravity = 0  
game_status = True
start_time =0
obstacle_rect_list =[]
obstacle_time = pygame.USEREVENT+0
pygame.time.set_timer(obstacle_time,1200)

text_font = pygame.font.Font('font/Pixeltype.ttf',50) # this will collect the text properties from pygame and will put it into variable text_font
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

game_over1_surf = text_font.render('Mr. Jumpy',False,(111,196,169))
game_over1_rect = game_over1_surf.get_rect(center=(400,50))
game_over2_surf =  text_font.render("Press Enter to Start",False,(111,196,169))
game_over2_rect = game_over2_surf.get_rect(center=(400,350))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_1_rect = player_walk_1.get_rect(midbottom=(80,300))
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_surf= pygame.transform.scale2x(player_stand_surf)
player_stand_rect = player_stand_surf.get_rect(center=(400,200))



while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit() # this is the opposite of the pygame.init()
            sys.exit() # this will stop the code to run update command
        

        if player_walk_1_rect.bottom <=300 and player_walk_1_rect.bottom >=150 and game_status:

            if events.type == pygame.MOUSEBUTTONDOWN:
                if player_walk_1_rect.collidepoint(events.pos):
                    player_gravity=-20

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    player_gravity =-20
            
            if events.type == obstacle_time:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (800,300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),160)))
                

        if events.type == pygame.KEYDOWN and not game_status:
            if events.key == pygame.K_SPACE:
                game_status=True
                start_time = pygame.time.get_ticks()

    if game_status:
           
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        player_gravity+=1
        player_walk_1_rect.y +=player_gravity

        if player_walk_1_rect.bottom >= 300:
            player_walk_1_rect.bottom=300

        game_status =  collitions(player_walk_1_rect,obstacle_rect_list)
        
        
        screen.blit(player_walk_1,player_walk_1_rect)
    else:
        screen.fill((94,129,162))     
        screen.blit(game_over1_surf,game_over1_rect)
        screen.blit(player_stand_surf,player_stand_rect)
        obstacle_rect_list.clear()
        player_walk_1_rect.bottom = 300
        player_gravity =0

        score_surf = text_font.render(f'Your Score: {score}',False,(111,196,169))
        score_rect = score_surf.get_rect(center=(400,350))
        if score ==0:
            screen.blit(game_over2_surf,game_over2_rect)
        else:
            screen.blit(score_surf,score_rect)



    pygame.display.update()
    clock.tick(60) # this tells the loop not to run more then 60 per seconds
