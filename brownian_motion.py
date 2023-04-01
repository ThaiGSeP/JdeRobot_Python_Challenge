import pygame
import numpy as np
import time
import math
import random

pygame.init()

# Set up window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

BORDER_WIDTH, BORDER_HEIGHT = 400, 300
BORDER_THICKNESS = 5
BORDER_COLOR = (255, 156, 0)
INSIDE_BORDER_COLOR = (200, 200, 200)

PARTICLE_COLOR = (0, 150, 255)
PARTICLE_RADIUS = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brownian Motion")

INITIAL_VELOCITY = -100

LIMIT_ANGULAR_VELOCITY = 2
LIMIT_ROTATE_TIME = 0.7

# Set up particles


class Particle:
    def __init__(self, x0, y0, dx0, dy0):
        self.x = x0     # X position
        self.y = y0     # Y position
        self.dx = dx0   # Velocity in X dirrection
        self.dy = dy0   # Velocity in Y dirrection
        self.w = 0      # Angular velocity
        self.rotate_time_left = 0
        self.last_move_time = time.time()
        self.color = PARTICLE_COLOR
        self.radius = PARTICLE_RADIUS

    def straight_move(self, delta_t):
        self.x += self.dx * (delta_t)
        self.y += self.dy * (delta_t)

    def rotate(self, delta_t):
        self.dx = self.dx * math.cos(self.w * delta_t) - \
            self.dy * math.sin(self.w * delta_t)
        self.dy = self.dy * math.cos(self.w * delta_t) + \
            self.dx * math.sin(self.w * delta_t)

    def move(self):
        current_time = time.time()
        dt_move = max(0, current_time - self.last_move_time -
                      self.rotate_time_left)
        dt_rotate = min(self.rotate_time_left,
                        current_time - self.last_move_time)
        self.straight_move(dt_move)
        self.rotate(dt_rotate)
        self.last_move_time = current_time
        self.rotate_time_left -= dt_rotate

    def set_w(self):
        self.w = (0.5 - random.random())*2*LIMIT_ANGULAR_VELOCITY

    def set_rotate_time(self):
        self.rotate_time_left = random.random()*LIMIT_ROTATE_TIME

def main():
    particle = Particle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 0, INITIAL_VELOCITY)

    # Set up clock
    clock = pygame.time.Clock()
    dt = 0.01  # time step

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw inside box
        pygame.draw.rect(screen, INSIDE_BORDER_COLOR, ((SCREEN_WIDTH - BORDER_WIDTH) //
                        2, (SCREEN_HEIGHT - BORDER_HEIGHT)//2, BORDER_WIDTH, BORDER_HEIGHT), 0)

        # Draw border
        pygame.draw.rect(screen, BORDER_COLOR, ((SCREEN_WIDTH - BORDER_WIDTH)//2-BORDER_THICKNESS,
                        (SCREEN_HEIGHT - BORDER_HEIGHT)//2-BORDER_THICKNESS, BORDER_WIDTH+BORDER_THICKNESS, BORDER_HEIGHT+BORDER_THICKNESS), BORDER_THICKNESS)

        # Update particle position
        particle.move()
        if (particle.x < ((SCREEN_WIDTH-BORDER_WIDTH)//2 + particle.radius)):
            particle.dx = - particle.dx
            particle.set_rotate_time()
            particle.set_w()
            particle.x = ((SCREEN_WIDTH-BORDER_WIDTH)//2 + particle.radius)

        elif (particle.x > ((SCREEN_WIDTH+BORDER_WIDTH)//2) - particle.radius):
            particle.dx = - particle.dx
            particle.set_rotate_time()
            particle.set_w()
            particle.x = ((SCREEN_WIDTH+BORDER_WIDTH)//2) - particle.radius

        elif (particle.y < ((SCREEN_HEIGHT-BORDER_HEIGHT)//2 + particle.radius)):
            particle.dy = - particle.dy
            particle.set_rotate_time()
            particle.set_w()
            particle.y = ((SCREEN_HEIGHT-BORDER_HEIGHT)//2 + particle.radius)

        elif (particle.y >= ((SCREEN_HEIGHT+BORDER_HEIGHT)//2) - particle.radius):
            particle.dy = - particle.dy
            particle.set_rotate_time()
            particle.set_w()
            particle.y = ((SCREEN_HEIGHT+BORDER_HEIGHT)//2) - particle.radius

        # Draw particle
        pygame.draw.circle(screen, particle.color,
                        (particle.x, particle.y), particle.radius)
        pygame.display.update()

        # Set frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
