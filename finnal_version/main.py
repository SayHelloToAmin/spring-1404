import pygame, sys, random, time
from pygame.locals import *
from config import *




pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whats This Game")
BACKGROUND_IMAGE = "finnal_version\media\BackGround.jpg"
background = pygame.image.load(BACKGROUND_IMAGE)
win.blit(background, (0, 0))



time_left_p1 = initial_time_p1
time_left_p2 = initial_time_p2
font = pygame.font.Font(None, 36) 
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks()
blink_timer = pygame.time.get_ticks()


# background music setting
pygame.mixer.init() 
pygame.mixer.music.load("finnal_version\media\Background.mp3") 
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  

# shot soundeffect setting
shoot_sound = pygame.mixer.Sound("finnal_version\media\Headshot.wav")  
shoot_sound.set_volume(0.3) 





blink1 = False
blink2 = False
while running:
    clock.tick(72)
    win.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 1000: 
        if time_left_p1 > 0:
                time_left_p1 -= 1
        if time_left_p2 > 0:
            time_left_p2 -= 1
        last_update = current_time 
        blink = True
    else:
        blink = False

    #timer blink 
    if time_left_p1 < 30:
        color_p1 = (255, 0, 0) 
        if current_time - blink_timer >= 500: 
            show_text_p1 = not show_text_p1
            blink_timer = current_time
    else:
        color_p1 = (255, 255, 255)  
        show_text_p1 = True  

    if time_left_p2 < 30:
        color_p2 = (255, 0, 0) 
        if current_time - blink_timer >= 500:
            show_text_p2 = not show_text_p2
            blink_timer = current_time
    else:
        color_p2 = (255, 255, 255)  
        show_text_p2 = True






    # Texts

    if show_text_p1:
        timer_text_p1 = font.render(f"Player 1 Time: {time_left_p1}s", True, color_p1)
        win.blit(timer_text_p1, (20, 20))

    if show_text_p2:
        timer_text_p2 = font.render(f"Player 2 Time: {time_left_p2}s", True, color_p2)
        win.blit(timer_text_p2, (WIDTH - timer_text_p2.get_width() - 20, 20))


    timer_text_p1 = font.render(f"Player 1 Bullets: {PLAYER1_BULLETS}", True, (255, 255, 255))
    win.blit(timer_text_p1, (20, 42))
    timer_text_p1 = font.render(f"Player 2 Bullets: {PLAYER2_BULLETS}", True, (255, 255, 255))
    win.blit(timer_text_p1, (1685, 42))
    #-----------------------------------------------------





    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        if PLAYER1_X <= 1:
            pass
        else:
            PLAYER1_X -= speed
    if keys[pygame.K_RIGHT]:
        if PLAYER1_X >= 1919:
            PLAYER1_X = 1919
        else:
            PLAYER1_X += speed
    if keys[pygame.K_UP]:
        if PLAYER1_Y <= 1:
            PLAYER1_Y = 1
        else:
            PLAYER1_Y -= speed
    if keys[pygame.K_DOWN]:
        if PLAYER1_Y >= 1079:
            PLAYER1_Y = 1079
        else:
            PLAYER1_Y += speed
    if keys[pygame.K_a]:
        if PLAYER2_X <= 1:
            PLAYER2_X = 1
        else:
            PLAYER2_X -= speed
    if keys[pygame.K_d]:
        if PLAYER2_X >= 1919:
            PLAYER2_X = 1919
        else:
            PLAYER2_X += speed
    if keys[pygame.K_w]:
        if PLAYER2_Y <= 1:
            PLAYER2_y = 1
        else:
            PLAYER2_Y -= speed
    if keys[pygame.K_s]:
        if PLAYER2_Y >= 1079:
            PLAYER2_Y = 1079
        else:
            PLAYER2_Y += speed

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if PLAYER2_BULLETS != 0:
                    PLAYER2_SHOTS.append((PLAYER2_X , PLAYER2_Y))
                    PLAYER2_BULLETS -= 1
                    shoot_sound.play()
                else:
                    pass
            if event.key == K_RSHIFT:
                if PLAYER1_BULLETS != 0:
                    PLAYER1_SHOTS.append((PLAYER1_X , PLAYER1_Y))
                    PLAYER1_BULLETS -= 1
                    shoot_sound.play()
                else:
                    pass
    




    pygame.draw.circle(win, (250,250,250), (PLAYER1_X,PLAYER1_Y), 5)
    pygame.draw.circle(win, (0,0,0), (PLAYER2_X,PLAYER2_Y), 5)

    for shot in PLAYER2_SHOTS:
        pygame.draw.circle(win, (0,0,0), (shot[0],shot[1]), 3)
    for shot in PLAYER1_SHOTS:
        pygame.draw.circle(win, (250,250,250), (shot[0],shot[1]), 3)

    pygame.display.update()
