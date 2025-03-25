import random
WIDTH = 1920
HEIGHT = 1080

initial_time_p1 = 120  
initial_time_p2 = 50   


PLAYER1_X = random.randint(1,1920)
PLAYER1_Y = random.randint(1,1080)
PLAYER2_X = random.randint(1,1920)
PLAYER2_Y = random.randint(1,1080)

PLAYER1_BULLETS = 10
PLAYER2_BULLETS = 10

last_player1_shot = None
last_player2_shot = None

PLAYER1_SHOTS = []
PLAYER2_SHOTS = []

PLAYER1_SCORE = 0
PLAYER2_SCORE = 0

PLAYER1 = True
PLAYER2 = True

show_text_p1 = True 
show_text_p2 = True 

speed = 3

targets = []



running = True