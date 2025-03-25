import random
from config import *  # Import settings like WIDTH and HEIGHT
import pygame
import sys
import time

class Player:
    def __init__(self, id , name, x, y, bullets, time):
        # Initialize player properties
        self.name = name  # Player's name
        self.id = id  # Unique ID for the player
        self.x = x  # Player's x-coordinate
        self.y = y  # Player's y-coordinate
        self.bullets = bullets  # Number of bullets available
        self.score = 0  # Initial score
        self.shots = []  # List of shot coordinates
        self.time_left = time  # Time remaining for the player
        self.player = True  # Player status (active/inactive)
        self.show_text = True  # Toggle text visibility
        self.last_shot = []  # Stores the last shot's coordinates

    def move(self, dx, dy):
        # Move the player while ensuring they stay within screen boundaries
        self.x = max(0, min(WIDTH, self.x + dx))
        self.y = max(0, min(HEIGHT, self.y + dy))

    def shoot(self):
        # Shoot a bullet if bullets and time are available
        if self.bullets > 0 and self.time_left > 0:
            self.shots.append((self.x, self.y))  # Register the shot
            if len(self.shots) == 1:
                self.last_shot = [(self.x , self.y)]
            else:
                if len(self.shots) > 2:
                    self.last_shot.pop(0)  # Keep track of recent shots only
                self.last_shot.append((self.x , self.y))
            self.bullets -= 1  # Reduce bullets count
            Game.shoot_sound.play()  # Play shooting sound
            return True
        return False  # Return False if no bullets or time left

class Game:
    pygame.mixer.init()  # Initialize pygame mixer

    # Sound effect settings
    shoot_sound = pygame.mixer.Sound("finnal_version\\media\\Headshot.wav")
    shoot_sound.set_volume(0.3)
    hit_sound = pygame.mixer.Sound("finnal_version\\media\\hit_target.wav")
    hit_sound.set_volume(0.3)
    hit_item_sound = pygame.mixer.Sound("finnal_version\\media\\hit_item.wav")
    hit_item_sound.set_volume(0.3)

    # Load images for targets and bonus items
    target_char = pygame.image.load("finnal_version/media/target.png")
    target_char = pygame.transform.scale(target_char, (45, 45))
    icon = pygame.image.load("finnal_version/media/extra_itemm.png")
    extra_icon = pygame.transform.scale(icon , (45, 40))

    players = [
        # Initialize two players with random positions, bullets, and time limits
        Player("Player 1", "Player 1", random.randint(1, 1280), random.randint(1, 720), 10, 50),
        Player("Player 2", "Player 2", random.randint(1, 1280), random.randint(1, 720), 10, 51)
    ]

    def __init__(self):
        # Initialize game properties
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))  # Game window
        pygame.display.set_caption("Whats This Game")

        # Load images
        self.background = pygame.image.load("finnal_version/media/BackGround.jpg")
        self.player1_char = pygame.image.load("finnal_version/media/player1_char.png")
        self.player2_char = pygame.image.load("finnal_version/media/player2_char.png")
        self.player1_char = pygame.transform.scale(self.player1_char, (40, 40))
        self.player2_char = pygame.transform.scale(self.player2_char, (40, 40))
        self.background = pygame.transform.scale(self.background, (1280, 720))

        # Set background music
        pygame.mixer.music.load("finnal_version\\media\\BG.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop the music

        self.clock = pygame.time.Clock()  # Game clock
        self.last_update = pygame.time.get_ticks()  # Last update timestamp
        self.blink_timer = pygame.time.get_ticks()  # Blink text timer
        self.font = pygame.font.Font(None, 36)  # Set font for texts
        self.running = True  # Game running status
        self.targets = []  # List of targets in the game
        self.bonus_items = []  # List of bonus items in the game
        self.floating_texts = []  # List of floating texts in the game

    def run(self):
        # Main game loop
        while self.running:
            self.clock.tick(72)  # Set frame rate
            self.current_time = pygame.time.get_ticks()  # Get current time
            self.win.blit(self.background, (0, 0))  # Draw background
            self.handle_events()  # Process player inputs
            self.update()  # Update game state
            self.draw()  # Render game elements
            pygame.display.update()  # Update display

    def handle_events(self):
        # Handle keyboard and player inputs
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
                pygame.quit()  # Close game
                sys.exit()  # Exit system
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game.players[1].shoot()  # Player 2 shoots
                if event.key == pygame.K_RSHIFT:
                    Game.players[0].shoot()  # Player 1 shoots

    def update(self):
        # Spawn new targets if the number of targets is below the limit
        spawn_target(self.targets, 4, pygame)

        # Check for hit targets and update the target list
        self.targets = remove_hit_targets(
            self.targets,
            Game.players[0].shots, Game.players[1].shots,
            Game.players[0].last_shot, Game.players[1].last_shot
        )

        # Remove floating texts that have expired
        self.floating_texts = [text for text in self.floating_texts if text.draw(self.win, self.font)]

        # Update player timers every second
        if self.current_time - self.last_update >= 1000:
            if Game.players[0].time_left > 0:
                Game.players[0].time_left -= 1  # Decrease player 1's time
            else:
                Game.players[0].player = False  # Player 1 is out of time

            if Game.players[1].time_left > 0:
                Game.players[1].time_left -= 1  # Decrease player 2's time
            else:
                Game.players[1].player = False  # Player 2 is out of time

            self.last_update = self.current_time  # Update the timer

        # Occasionally spawn bonus items randomly
        if random.randint(1, 700) == 1:
            self.bonus_items.append(BonusItem(pygame))

        # Handle bonus items (apply effects if hit by a shot)
        new_items = []
        for item in self.bonus_items:
            t, y = item.is_hit(Game.players[0].shots)
            if t:
                item.apply_effect(Game.players[0], Game.players[1], self.targets, self)  # Player 1 hit bonus
                continue
            t, y = item.is_hit(Game.players[1].shots)
            if t:
                item.apply_effect(Game.players[1], Game.players[0], self.targets, self)  # Player 2 hit bonus
                continue
            new_items.append(item)  # Keep the bonus item if not hit
        self.bonus_items = new_items

        # Blink the timer text if time is less than 30 seconds
        if Game.players[0].time_left < 30:
            self.color_p1 = (255, 0, 0)  # Red color for Player 1 timer
            if self.current_time - self.blink_timer >= 500:  # Toggle visibility every 500ms
                Game.players[0].show_text = not Game.players[0].show_text
                self.blink_timer = self.current_time
        else:
            self.color_p1 = (255, 255, 255)  # Default white color
            Game.players[0].show_text = True

        if Game.players[1].time_left < 30:
            self.color_p2 = (255, 0, 0)  # Red color for Player 2 timer
            if self.current_time - self.blink_timer >= 500:
                Game.players[1].show_text = not Game.players[1].show_text
                self.blink_timer = self.current_time
        else:
            self.color_p2 = (255, 255, 255)  # Default white color
            Game.players[1].show_text = True

        # Set players as inactive if they run out of bullets or time
        if Game.players[0].bullets < 1 or Game.players[0].time_left <= 0:
            Game.players[0].player = False
        if Game.players[1].bullets < 1 or Game.players[1].time_left <= 0:
            Game.players[1].player = False

        # End the game if both players are inactive
        if not Game.players[0].player and not Game.players[1].player:
            self.running = False  # Stop the game loop
            pygame.mixer.music.pause()  # Pause the background music
            self.play_end_sound()  # Play the end sound effect
            self.display_background_effect()  # Display end-game effect
            self.draw_winner()  # Show the winner
            time.sleep(3.5)  # Wait for 3.5 seconds before exiting

    def draw(self):
        # Draw players and their shots
        for player in Game.players:
            pass
            for shot in player.shots:
                self.win.blit(self.player1_char if player.id == "Player 1" else self.player2_char, (shot[0]-20, shot[1]-20))

        # Draw targets on the screen
        for target in self.targets:
            target.draw(self.win, pygame)

        # Draw bonus items on the screen
        for item in self.bonus_items:
            item.draw(self.win, pygame)

        # Draw floating texts
        for text in self.floating_texts:
            text.draw(self.win, self.font)

        # Display timers and bullet counts for both players
        if Game.players[0].show_text:
            timer_text_p1 = self.font.render(f"{Game.players[0].name}'s Time: {Game.players[0].time_left}s", True, self.color_p1)
            self.win.blit(timer_text_p1, (20, 20))  # Player 1 timer

        if Game.players[1].show_text:
            timer_text_p2 = self.font.render(f"{Game.players[1].name}'s Time: {Game.players[1].time_left}s", True, self.color_p2)
            self.win.blit(timer_text_p2, (WIDTH - timer_text_p2.get_width() - 20, 20))  # Player 2 timer

        # Bullets and scores for both players
        bullets_p1 = self.font.render(f"{Game.players[0].name}'s Bullets: {Game.players[0].bullets}", True, (255, 255, 255))
        self.win.blit(bullets_p1, (20, 42))
        bullets_p2 = self.font.render(f"{Game.players[1].name}'s Bullets: {Game.players[1].bullets}", True, (255, 255, 255))
        self.win.blit(bullets_p2, (1045, 42))

        score_p1 = self.font.render(f"{Game.players[0].name}'s Score: {Game.players[0].score}", True, (255, 255, 255))
        self.win.blit(score_p1, (20, 690))  # Player 1 score

        score_p2 = self.font.render(f"{Game.players[1].name}'s Score: {Game.players[1].score}", True, (255, 255, 255))
        self.win.blit(score_p2, (1055, 690))  # Player 2 score

    def draw_winner(self):
        # Fade-out effect while showing the winner
        for i in range(255, 0, -5):
            self.win.fill((0, 0, 0))  # Black background
            
            # Determine the winner or if it's a tie
            if Game.players[0].score > Game.players[1].score:
                winner_text = f"{Game.players[0].name} Wins! Score: {Game.players[0].score}"
            elif Game.players[1].score > Game.players[0].score:
                winner_text = f"{Game.players[1].name} Wins! Score: {Game.players[1].score}"
            else:
                winner_text = f"It's a Tie! Both scored: {Game.players[0].score}"
            
            text_surface = self.font.render(winner_text, True, (255, i, i))  # Gradually fade the text color
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.win.blit(text_surface, text_rect)
            
            pygame.display.update()  # Update display
            pygame.time.wait(30)  # Delay to create fade effect

    def display_background_effect(self):
        # Display a simple background effect with changing colors
        for i in range(10):
            self.win.fill((min(255, max(0, i*25)), min(255, max(0, i*10)), min(255, max(0, i*30))))
            pygame.display.update()
            pygame.time.wait(100)

    def play_end_sound(self):
        # Play victory/end-game sound effect
        victory_sound = pygame.mixer.Sound("finnal_version\\media\\ending.wav")
        victory_sound.set_volume(0.5)
        victory_sound.play()

class Target:
    def __init__(self, pygame):
        # Initialize target with random position and radius
        self.x = random.randint(100, 1280 - 100)  # Random x-coordinate within screen bounds
        self.y = random.randint(100, 720 - 100)  # Random y-coordinate within screen bounds
        self.radius = 25  # Target's radius
        self.spawn_time = pygame.time.get_ticks()  # Time when the target was created
    
    def draw(self, win, pygame):
        # Draw the target on the screen using its coordinates
        win.blit(Game.target_char, (self.x - 30, self.y - 30))
    
    def is_hit(self, shots):
        # Check if a shot has hit the target
        for shot in shots:
            # Calculate the distance between the target and the shot
            if (self.x - shot[0]) ** 2 + (self.y - shot[1]) ** 2 <= self.radius ** 2:
                return True, shot  # Target is hit
        return False, None  # Target is not hit

def spawn_target(targets, max_targets, pygame):
    # Spawn new targets if the current number is less than the maximum
    if len(targets) < max_targets:
        targets.append(Target(pygame))

def calculate_score(last_shot, new_shot):
    # Calculate the score based on the distance between the last and new shot
    if len(last_shot) == 1:
        return 10  # Default score for the first shot
    distance = ((new_shot[0] - last_shot[0][0]) ** 2 + (new_shot[1] - last_shot[0][1]) ** 2) ** 0.5
    return int(distance / 10)  # Score is proportional to the distance

def remove_hit_targets(targets, player1_shots, player2_shots, last_player1_shot, last_player2_shot):
    # Check for targets hit by player shots and update the game state
    new_targets = []  # List to hold targets not hit
    for target in targets:
        hit, shot = target.is_hit(player1_shots)  # Check if Player 1 hits the target
        if hit:
            Game.hit_sound.play()  # Play the hit sound
            Game.players[0].score += calculate_score(last_player1_shot, shot)  # Update Player 1's score
            last_player1_shot = shot  # Update the last shot
            continue  # Skip adding the hit target

        hit, shot = target.is_hit(player2_shots)  # Check if Player 2 hits the target
        if hit:
            Game.hit_sound.play()  # Play the hit sound
            Game.players[1].score += calculate_score(last_player2_shot, shot)  # Update Player 2's score
            last_player2_shot = shot  # Update the last shot
            continue  # Skip adding the hit target

        new_targets.append(target)  # Keep the targets not hit
    return new_targets


class BonusItem(Target):
    def __init__(self, pygame):
        super().__init__(pygame)  # Inherit properties from the Target class
        # Randomly choose a type of bonus effect
        self.type = random.choice(["extra_bullets", "extra_time", "reduce_opponent_time", "remove_target"])
    
    def draw(self, win, pygame):
        # Draw the bonus item on the screen
        win.blit(Game.extra_icon, (self.x - 25, self.y - 25))

    def apply_effect(self, player, opponent, targets, game):
        # Play the sound effect for hitting an item
        Game.hit_item_sound.play()

        # Apply the bonus effect based on the type of bonus
        if self.type == "extra_bullets":
            player.bullets += 5  # Add bullets to the player
            game.floating_texts.append(FloatingText("+5 Bullets", 50, 50, (0, 255, 0)))  # Green floating text

        elif self.type == "extra_time":
            player.time_left += 10  # Add time to the player
            game.floating_texts.append(FloatingText("+10s", 50, 20, (0, 255, 0)))  # Green floating text

        elif self.type == "reduce_opponent_time":
            opponent.time_left = max(0, opponent.time_left - 10)  # Reduce opponent's time
            game.floating_texts.append(FloatingText("-10s Opponent", 1100, 20, (255, 0, 0)))  # Red floating text

        elif self.type == "remove_target" and targets:
            targets.pop(random.randint(0, len(targets) - 1))  # Remove a random target
            game.floating_texts.append(FloatingText("Target Removed!", 600, 100, (255, 255, 0)))  # Yellow floating text

class FloatingText:
    def __init__(self, text, x, y, color, duration=1000):
        # Initialize floating text properties
        self.text = text  # The text to display
        self.x = x  # X-coordinate of the text
        self.y = y  # Y-coordinate of the text
        self.color = color  # Color of the text
        self.duration = duration  # Duration of the text in milliseconds
        self.start_time = pygame.time.get_ticks()  # Timestamp when the text was created

    def draw(self, win, font):
        # Draw the text on the screen if it's still within the duration
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.duration:
            text_surface = font.render(self.text, True, self.color)  # Render the text
            # Display the text with a slight upward motion over time
            win.blit(text_surface, (self.x, self.y - (current_time - self.start_time) // 10))
            return True  # Keep the text visible
        return False  # Remove the text after its duration expires


