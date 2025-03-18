import pygame
import random


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.bullets = 10
        self.time_left = 60
        self.score = 0
        self.controls = controls

    def move(self, dx):
        pass

    def shoot(self):
        pass

    def draw(self, screen):
        pass

    def add_bullets(self, count):
        pass

    def add_time(self, seconds):
        pass


class Bullet:
    def __init__(self, x, y):
        pass

    def move(self):
        pass

    def draw(self, screen):
        pass


class Target:
    def __init__(self):
        pass

    def draw(self, screen):
        pass


class Item:
    def __init__(self, x, y, effect_type):
        pass

    def apply_effect(self, player):
        pass

    def draw(self, screen):
        pass


class Game:
    def __init__(self):
        pass

    def run(self):
        pass
    def clock_tick(self):
        pass

    def handle_events(self):
        pass

        

    def update(self):
        pass


        
    def draw(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.run()
