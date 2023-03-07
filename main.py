import pygame
import sys
from random import randint,choice

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/Player/jump.png')
        self.player_list = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.image = self.player_list[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity =0

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            jump_audio()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity +=1
        self.rect.bottom += self.gravity
        if self.rect.bottom > 300 : self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom != 300:
            self.image = self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index >= len(self.player_list): self.player_index =0
            self.image = self.player_list[int(self.player_index)]

    def update(self):
        self.user_input()
        self.apply_gravity()
        self.animation()
        if game_status == False:
            self.rect.bottom=300

#obstacle class
class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 =pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.obstacle_list = [fly1,fly2]
            self.index =0 
            y_pos = 190
        else:
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.obstacle_list = [snail1,snail2]
            self.index = 0
            y_pos = 300
        self.image = self.obstacle_list[self.index]
        self.rect= self.image.get_rect(midbottom=(randint(900,1100),y_pos))

    def animation(self):
        if self.index ==0: self.index =1
        else: self.index=0
        self.image = self.obstacle_list[self.index]
    
    def destroy(self):
        if self.rect.right <=-100:
            self.kill()

    def update(self):
        self.animation()
        self.rect.right -=6
        self.destroy()

#display score
def display_score():
    time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = text_font.render(f'Score: {time}',False,(65,65,65))
    score_rect = score_surf.get_rect(center=(720,50))
    screen.blit(score_surf,score_rect)
    return time

#collision
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle,False):
        obstacle.empty()
        return False
    else: return True

#jump audio        
def jump_audio():
    pygame.mixer.init()
    pygame.mixer.music.load('audio/jump.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()

pygame.init()

#variables
screen = pygame.display.set_mode((800,400))  # this is to make base screen/ basic surface on which we will do the work
pygame.display.set_caption('Mr. Jumpy') # this is to change the name of the screen
clock = pygame.time.Clock()  # this is the clock which will help in fixing the frame 
game_status = False
score =0
High_Score =0
start_time =0

obstacle_time = pygame.USEREVENT+0
pygame.time.set_timer(obstacle_time,1200)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

bg_audio = pygame.mixer.Sound('audio/music.wav')

text_font = pygame.font.Font('font/Pixeltype.ttf',50) # this will collect the text properties from pygame and will put it into variable text_font
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

game_over1_surf = text_font.render('Mr. Jumpy',False,(111,196,169))
game_over1_rect = game_over1_surf.get_rect(center=(400,50))
game_over2_surf =  text_font.render("Press Enter to Start",False,(111,196,169))
game_over2_rect = game_over2_surf.get_rect(center=(400,350))

player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_surf= pygame.transform.scale2x(player_stand_surf)
player_stand_rect = player_stand_surf.get_rect(center=(400,210))


while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit() # this is the opposite of the pygame.init()
            sys.exit() # this will stop the code to run update command
        
        bg_audio.set_volume(0.01)
        bg_audio.play(loops=-1)

                              
        if events.type == obstacle_time and game_status:
            obstacle.add(Obstacles(choice(['fly','snail','snail','snail'])))
                

        if events.type == pygame.KEYDOWN and not game_status:
            if events.key == pygame.K_SPACE:
                game_status=True
                start_time = pygame.time.get_ticks()

    if game_status:
           
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        if High_Score <= score:
            High_Score = score

        player.draw(screen)
        player.update()
        obstacle.draw(screen)
        obstacle.update()

        game_status =  collision_sprite()
        
    else:
        screen.fill((94,129,162))     
        screen.blit(game_over1_surf,game_over1_rect)
        screen.blit(player_stand_surf,player_stand_rect)
        high_score_surf = text_font.render(f'High Score: {High_Score}',False,(111,196,169))
        high_score_rect = high_score_surf.get_rect(center = (400,90))
        
        score_surf = text_font.render(f'Your Score: {score}',False,(111,196,169))
        score_rect = score_surf.get_rect(center=(400,350))
        if score ==0:
            screen.blit(game_over2_surf,game_over2_rect)
        else:
            screen.blit(score_surf,score_rect)
            screen.blit(high_score_surf,high_score_rect)



    pygame.display.update()
    clock.tick(60) # this tells the loop not to run more then 60 per seconds
