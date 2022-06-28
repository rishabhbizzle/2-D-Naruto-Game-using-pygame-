from numpy import append
import pygame
import sys
import os

pygame.init()

HEIGHT = 500
WIDTH = 900
CHARACTER_WIDTH = 55
CHARACTER_HEIGHT = 40
BLACK = (0, 0, 0)
NARUTO = (255, 0, 0)
SASUKE = (255, 255, 0)
PURPLE = (128,0,128)


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
 
FPS = 60

HEALTH_FONT = pygame.font.SysFont('arial', 30)
WINNER_FONT = pygame.font.SysFont('arial', 100)

SASUKE_HIT = pygame.USEREVENT + 1
NARUTO_HIT = pygame.USEREVENT + 2

SASUKE_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets', 'sasuke.png'))
NARUTO_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets', 'naruto.png'))
LOGO1 = pygame.image.load(os.path.join('Assets', 'logo.png'))

LOGO = pygame.transform.scale(LOGO1, (120, 40))
SASUKE_CHARACTER = pygame.transform.scale(SASUKE_CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
NARUTO_CHARACTER = pygame.transform.scale(NARUTO_CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))


SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))

#Display or Window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D NARUTO VS SASUKE")

WHITE = (255, 255, 255)

def sasuke_movement(keys_pressed, sasuke):
    if keys_pressed[pygame.K_a] and sasuke.x - VEL > 0:
        sasuke.x -= VEL
    if keys_pressed[pygame.K_d] and sasuke.x + sasuke.width < BORDER.x:
        sasuke.x += VEL
    if keys_pressed[pygame.K_s] and sasuke.y + sasuke.height < HEIGHT > 0:
        sasuke.y += VEL
    if keys_pressed[pygame.K_w] and sasuke.y - VEL > 0:
        sasuke.y -= VEL

def naruto_movement(keys_pressed, naruto):
    if keys_pressed[pygame.K_LEFT] and naruto.x - VEL > BORDER.x + BORDER.width:
        naruto.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and naruto.x + naruto.width < WIDTH:
        naruto.x += VEL
    if keys_pressed[pygame.K_DOWN] and naruto.y + naruto.height < HEIGHT > 0:
        naruto.y += VEL
    if keys_pressed[pygame.K_UP] and naruto.y - VEL > 0:
        naruto.y -= VEL

def handle_bullets(sasuke_bullets, naruto_bullets, sasuke, naruto):
    for bullet in sasuke_bullets:
        bullet.x += BULLET_VEL
        if naruto.colliderect(bullet):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            sasuke_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            sasuke_bullets.remove(bullet)

    for bullet in naruto_bullets:
        bullet.x -= BULLET_VEL
        if sasuke.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            naruto_bullets.remove(bullet)
        elif bullet.x < 0:
            naruto_bullets.remove(bullet)


def draw_window(naruto, sasuke, naruto_bullets, sasuke_bullets, naruto_health, sasuke_health): #functon of display bg
    
    WIN.blit(SPACE, (0, 0)) # Assigned a color to the game window or u can say background
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(LOGO, (390, 10))


    naruto_health_text = HEALTH_FONT.render("Health: " + str(naruto_health), 1, WHITE)
    sasuke_health_text = HEALTH_FONT.render("Health: " + str(sasuke_health), 1, WHITE)

    WIN.blit(naruto_health_text, (WIDTH - naruto_health_text.get_width() - 10, 10))
    WIN.blit(sasuke_health_text, (10, 10))

    WIN.blit(SASUKE_CHARACTER, (sasuke.x, sasuke.y))
    WIN.blit(NARUTO_CHARACTER, (naruto.x, naruto.y))


    for bullet in naruto_bullets:
        pygame.draw.rect(WIN, NARUTO, bullet)
    for bullet in sasuke_bullets:
        pygame.draw.rect(WIN, SASUKE, bullet)

    pygame.display.update() # Updating the color of display with this command

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Game's main function
def main():
    naruto = pygame.Rect(700, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    sasuke = pygame.Rect(100, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    naruto_bullets = []
    sasuke_bullets = []

    naruto_health = 10
    sasuke_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS) # Assigning a fixed framerate for the game
        #For checking if the user closed the game then our loop will break 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(sasuke_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(sasuke.x + sasuke.width, sasuke.y + sasuke.height//2 - 2, 10, 5)
                    sasuke_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len (naruto_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(naruto.x, naruto.y + naruto.height//2 - 2, 10, 5)
                    naruto_bullets.append(bullet)

            if event.type == NARUTO_HIT:
                naruto_health -= 1  

            if event.type == SASUKE_HIT:
                sasuke_health -= 1
        
        winner_text = ""
        if naruto_health <= 0:
            winner_text = "SASUKE Wins!"

        if sasuke_health <= 0:
            winner_text = "NARUTO Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()

        sasuke_movement(keys_pressed, sasuke)
        naruto_movement(keys_pressed, naruto)
        
        handle_bullets(sasuke_bullets, naruto_bullets, sasuke, naruto)
   
        draw_window(naruto, sasuke, naruto_bullets, sasuke_bullets, naruto_health, sasuke_health)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()