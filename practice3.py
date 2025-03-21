import pygame , time , random
pygame.init() #meqdardehi avalie
window = pygame.display.set_mode((800,600), pygame.RESIZABLE) 
pygame.display.set_caption("mini game")
    
count_down = 60
start_ticks = pygame.time.get_ticks() // 1000

speed = 5

x = random.randint(0,780)
y = random.randint(0,580)
n = random.randint(0,780)
m = random.randint(0,580)
k = random.randint(0,780)
j = random.randint(0,580)
h = random.randint(0,780)
p = random.randint(0,580)
f = random.randint(0,780)
e = random.randint(0,580)

running = True
clock = pygame.time.Clock()

while running:
    window.fill((100,130,93))
    score1 = 0
    score2 = 0
    font = pygame.font.Font(None, 25)
    text_sourface1 = font.render("score 1 : "+ str(score1), True, (255, 255, 255))
    text_sourface3 = font.render("score 2 : "+ str(score2), True, (255, 255, 255))
    window.blit(text_sourface1, (0,0))
    window.blit(text_sourface3, (700,0))

    current_time = pygame.time.get_ticks() // 1000  # دریافت زمان فعلی به ثانیه
    remaining_time1 = max(0, count_down - (current_time - start_ticks))
    remaining_time2 = max(0, count_down - (current_time - start_ticks))

    text_sourface2 = font.render(f"time 1 : {remaining_time1}", True, (255, 255, 255))
    text_sourface4 = font.render(f"time 2 : {remaining_time2}", True, (255, 255, 255))
    window.blit(text_sourface2, (0,20))
    window.blit(text_sourface4, (700,20))

    bullet1 = 10
    bullet2 = 10
    text_sourface5 = font.render(f"bullet 1: {bullet1}", True, (255, 255, 255))
    text_sourface6 = font.render(f"bullet 2: {bullet2}", True, (255, 255, 255))
    window.blit(text_sourface5, (0,40))
    window.blit(text_sourface6, (700,40))

    pygame.draw.rect(window, (255, 182,193),((k,j,20,20)), 0)
    pygame.draw.rect(window, (255, 182,193),((h,p,20,20)), 0)
    pygame.draw.rect(window, (255, 182,193),((f,e,20,20)), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP :
            if event.key == pygame.K_1 :
                pygame.draw.circle(window, (250,250,250), (x,y), 5)  
                pygame.display.flip()   
            if event.key == pygame.K_0 :   
                pygame.draw.circle(window, (0,0,0), (n,m), 5) 
                pygame.display.flip()    


        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_d :
                x += speed
            if event.key == pygame.K_a :
                x -= speed
            if event.key == pygame.K_w :
                y -= speed   
            if event.key == pygame.K_s :
                y += speed

            if event.key == pygame.K_UP :
                m -= speed 
            if event.key == pygame.K_DOWN :
                m += speed 
            if event.key == pygame.K_LEFT :
                n -= speed 
            if event.key == pygame.K_RIGHT :
                n += speed    


    pygame.display.flip()
              
    clock.tick(60)
