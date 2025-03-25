import random 
from config import *
import pygame
import sys

class Player:
    def __init__(self, name, x, y, bullets, time):
        self.name = name
        self.x = x
        self.y = y
        self.bullets = bullets
        self.score = 0
        self.shots = []
        self.time_left = time
        self.player = True
        self.show_text = True 
        self.last_shot = []


    def move(self, dx, dy):
        self.x = max(0, min(WIDTH, self.x + dx))
        self.y = max(0, min(HEIGHT, self.y + dy))

    def shoot(self):
        if self.bullets > 0 and self.time_left > 0:
            self.shots.append((self.x, self.y))
            if len(self.shots) == 1:
                self.last_shot = [(self.x , self.y)]
            else:
                if len(self.shots) > 2:
                    self.last_shot.pop(0)
                self.last_shot.append((self.x , self.y))
            self.bullets -= 1
            Game.shoot_sound.play()
            return True
        return False


class Game:
    pygame.mixer.init() 
    # shot sound effect setting
    shoot_sound = pygame.mixer.Sound("finnal_version\media\Headshot.wav")  
    shoot_sound.set_volume(0.3) 
    #-----------------------------------------------------
    hit_sound = pygame.mixer.Sound("finnal_version\media\hit_target.wav")  
    hit_sound.set_volume(0.3) 
    hit_item_sound = pygame.mixer.Sound("finnal_version\media\hit_item.wav")  
    hit_item_sound.set_volume(0.3) 



    target_char = pygame.image.load("finnal_version/media/target.png")
    target_char = pygame.transform.scale(target_char, (45, 45))
    icon = pygame.image.load("finnal_version/media/extra_itemm.png")
    extra_icon = pygame.transform.scale(icon , (45, 40))

    players = [
                Player("Player 1", random.randint(1, 1280), random.randint(1, 720), 10, 120),
                Player("Player 2", random.randint(1, 1280), random.randint(1, 720), 10, 10)
            ]


    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Whats This Game")



        # image loaders
        self.background = pygame.image.load("finnal_version/media/BackGround.jpg")
        self.player1_char = pygame.image.load("finnal_version/media/player1_char.png")
        self.player2_char = pygame.image.load("finnal_version/media/player2_char.png")
        self.player1_char = pygame.transform.scale(self.player1_char, (40, 40))
        self.player2_char = pygame.transform.scale(self.player2_char, (40, 40))
        self.background = pygame.transform.scale(self.background, (1280, 720))

        #-----------------------------------------------------

        # background music setting
        pygame.mixer.music.load("finnal_version\media\Background.mp3") 
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  
        #-----------------------------------------------------

        # shot sound effect setting

        shoot_sound = pygame.mixer.Sound("finnal_version\media\Headshot.wav")  
        shoot_sound.set_volume(0.3) 
        #-----------------------------------------------------

        self.clock = pygame.time.Clock()
        self.last_update = pygame.time.get_ticks()
        self.blink_timer = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.targets = []
        self.bonus_items = []


    def run(self):
        while self.running:
            self.clock.tick(72)
            self.current_time = pygame.time.get_ticks()
            self.win.blit(self.background, (0, 0))
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Game.players[0].move(-3, 0)
        if keys[pygame.K_RIGHT]:
            Game.players[0].move(3, 0)
        if keys[pygame.K_UP]:
            Game.players[0].move(0, -3)
        if keys[pygame.K_DOWN]:
            Game.players[0].move(0, 3)
        if keys[pygame.K_a]:
            Game.players[1].move(-3, 0)
        if keys[pygame.K_d]:
            Game.players[1].move(3, 0)
        if keys[pygame.K_w]:
            Game.players[1].move(0, -3)
        if keys[pygame.K_s]:
            Game.players[1].move(0, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game.players[1].shoot()
                if event.key == pygame.K_RSHIFT:
                    Game.players[0].shoot()


    def update(self):
            spawn_target(self.targets, 5, pygame)
            self.targets = remove_hit_targets(self.targets, Game.players[0].shots, Game.players[1].shots, Game.players[0].last_shot, Game.players[1].last_shot)



            if self.current_time - self.last_update >= 1000: 
                if Game.players[0].time_left > 0:
                        Game.players[0].time_left -= 1
                else:
                    Game.players[0].player = False
                if Game.players[1].time_left > 0:
                    Game.players[1].time_left -= 1
                else:
                    Game.players[1].player = False
                self.last_update = self.current_time 

            #extra items 
            if random.randint(1, 500) == 1: 
                self.bonus_items.append(BonusItem(pygame))


            
            new_items = []
            for item in self.bonus_items:
                t , y = item.is_hit(Game.players[0].shots)
                if t :
                    item.apply_effect(Game.players[0], Game.players[1], self.targets)
                    continue
                t , y = item.is_hit(Game.players[1].shots)
                if t:
                    item.apply_effect(Game.players[1], Game.players[0], self.targets)
                    continue
                new_items.append(item)
            self.bonus_items = new_items


            #timer blink 

            if Game.players[0].time_left < 30:
                self.color_p1 = (255, 0, 0) 
                if self.current_time - self.blink_timer >= 500: 
                    Game.players[0].show_text = not Game.players[0].show_text
                    self.blink_timer = self.current_time
            else:
                self.color_p1 = (255, 255, 255)  
                Game.players[0].show_text = True  

            if Game.players[1].time_left < 30:
                self.color_p2 = (255, 0, 0) 
                if self.current_time - self.blink_timer >= 500:
                    Game.players[1].show_text = not Game.players[1].show_text
                    self.blink_timer = self.current_time
            else:
                self.color_p2 = (255, 255, 255)  
                Game.players[1].show_text = True
            #-----------------------------------------------------

    def draw(self):
        for player in Game.players:
            pygame.draw.circle(self.win, (250, 250, 250) if player.name == "Player 1" else (0, 0, 0), (player.x, player.y), 5)
            for shot in player.shots:
                self.win.blit(self.player1_char if player.name == "Player 1" else self.player2_char, (shot[0]-20 , shot[1]-20))

        for target in self.targets:
            target.draw(self.win, pygame)

        for item in self.bonus_items:
            item.draw(self.win, pygame)


        # Texts

        if Game.players[0].show_text:
            timer_text_p1 = self.font.render(f"Player 1 Time: {Game.players[0].time_left}s", True, self.color_p1)
            self.win.blit(timer_text_p1, (20, 20))

        if Game.players[1].show_text:
            timer_text_p2 = self.font.render(f"Player 2 Time: {Game.players[1].time_left}s", True, self.color_p2)
            self.win.blit(timer_text_p2, (WIDTH - timer_text_p2.get_width() - 20, 20))


        timer_text_p1 = self.font.render(f"Player 1 Bullets: {Game.players[0].bullets}", True, (255, 255, 255))
        self.win.blit(timer_text_p1, (20, 42))
        timer_text_p1 = self.font.render(f"Player 2 Bullets: {Game.players[1].bullets}", True, (255, 255, 255))
        self.win.blit(timer_text_p1, (1045, 42))


        score_text_p1 = self.font.render(f"Player 1 Score: {Game.players[0].score}", True, (255, 255, 255))
        self.win.blit(score_text_p1, (20, 690))

        score_text_p2 = self.font.render(f"Player 2 Score: {Game.players[1].score}", True, (255, 255, 255))
        self.win.blit(score_text_p2, (1055, 690))
        #-----------------------------------------------------




class Target:
    def __init__(self,pygame):
        self.x = random.randint(100, 1280 - 100)
        self.y = random.randint(100, 720 - 100)
        self.radius = 25
        self.spawn_time = pygame.time.get_ticks()
    
    def draw(self, win,pygame):
        win.blit(Game.target_char, (self.x-30, self.y-30))
    
    def is_hit(self, shots):
        for shot in shots:
            if (self.x - shot[0]) ** 2 + (self.y - shot[1]) ** 2 <= self.radius ** 2:
                return True, shot
        return False, None
    
def spawn_target(targets, max_targets , pygame):
    if len(targets) < max_targets:
        targets.append(Target(pygame))

def calculate_score(last_shot, new_shot):

    if  len(last_shot) == 1:
        return 10  
    distance = ((new_shot[0] - last_shot[0][0]) ** 2 + (new_shot[1] - last_shot[0][1]) ** 2) ** 0.5
    return int(distance / 10)  

def remove_hit_targets(targets, player1_shots, player2_shots, last_player1_shot, last_player2_shot):

    new_targets = []
    for target in targets:
        hit , shot = target.is_hit(player1_shots)
        if hit:
            Game.hit_sound.play()
            Game.players[0].score += calculate_score(last_player1_shot, shot)
            last_player1_shot = shot
            continue
        
        hit, shot = target.is_hit(player2_shots)
        if hit:
            Game.hit_sound.play()
            Game.players[1].score += calculate_score(last_player2_shot, shot)
            last_player2_shot = shot
            continue
        
        new_targets.append(target)
    return new_targets




class BonusItem(Target):
    def __init__(self,pygame):
        super().__init__(pygame) 
        self.type = random.choice(["extra_bullets", "extra_time", "reduce_opponent_time", "remove_target"])
        
        

    def draw(self, win, pygame):
        win.blit(Game.extra_icon, (self.x - 25, self.y - 25))

    def apply_effect(self, player, opponent, targets):
        Game.hit_item_sound.play()
        
        if self.type == "extra_bullets":
            player.bullets += 5  
        elif self.type == "extra_time":
            player.time_left += 10  
        elif self.type == "reduce_opponent_time":
            opponent.time_left = max(0, opponent.time_left - 10)  
        elif self.type == "remove_target" and targets:
            targets.pop(random.randint(0, len(targets) - 1))  



if __name__ == "__main__":
    game = Game()
    game.run()
