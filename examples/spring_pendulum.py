#!/usr/bin/env python3
"""
Spring Pendulum Demo

Physics concepts demonstrated:
- Hooke's Law (F = -kx)
- Simple harmonic motion
- Damping and energy dissipation
- Combined gravitational and elastic forces

This simulation shows a mass attached to a fixed point by a spring,
experiencing gravity and friction. The spring color changes based
on extension, visualizing the elastic force.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate Hooke's Law and spring constant
- Show natural frequency of oscillation
- Explore underdamped, critically damped, and overdamped motion
- Visualize energy transfer between kinetic and potential
"""

import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, Force
from tiny_pysics.forces import ElasticForce, Friction
from tiny_pysics.utils import toggle

# Physical constants
BALL_MASS = 10
REST_LENGTH = 90  # Natural spring length
SPRING_CONSTANT = 10  # Spring stiffness
GRAVITY = 9.81
TIMESTEP = 0.1

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Black small dot - Anchor
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 2)
    text = font.render("Anchor point", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black larger dot - Ball
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 5)
    text = font.render("Mass", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Red line - Spring
    pygame.draw.line(screen, (200, 0, 0), (10, y + 6), (20, y + 6), 2)
    text = font.render("Spring (red = stretched)", True, (0, 0, 0))
    screen.blit(text, (25, y))
    # Keybinds
    y += 30
    text = font.render("SPACE - Start/stop", True, (100, 100, 100))
    screen.blit(text, (10, y))
    y += 18
    text = font.render("T - Toggle trail", True, (100, 100, 100))
    screen.blit(text, (10, y))
    y += 18
    text = font.render("R - Reset", True, (100, 100, 100))
    screen.blit(text, (10, y))


def create_simulation():
    """Create and return simulation objects."""
    ball = PhysObject(400, 250, BALL_MASS)
    anchor = PhysObject(500, 250, 1)  # Fixed anchor point
    ball.set_timestep(TIMESTEP)

    # Create forces
    spring = ElasticForce(ball, anchor, REST_LENGTH, SPRING_CONSTANT)
    weight = Force(0, GRAVITY * BALL_MASS)  # Gravity force
    friction = Friction(ball, k=0.01, power=1)  # Linear damping

    # Apply forces
    ball.add_force(weight)
    ball.add_force(spring, dynamic=True)
    ball.add_force(friction, dynamic=True)

    return ball, anchor


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Spring Pendulum - Hooke's Law")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    screen.fill((255, 255, 255))

    # Create simulation
    ball, anchor = create_simulation()

    # Simulation state
    running = False
    trace_mode = False
    loop = True

    while loop:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    running = toggle(running)
                elif event.key == K_t:
                    trace_mode = toggle(trace_mode)
                elif event.key == K_r:
                    ball, anchor = create_simulation()
                    running = False
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Update physics
        if running:
            ball.tick()

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Calculate spring stretch for color coding
        distance = ball.distance(anchor)
        # Color intensity based on stretch (red = stretched)
        stretch_factor = 1 - math.exp(-distance / 160)
        spring_color = (int(254 * stretch_factor), 0, 0)

        # Draw spring line
        pygame.draw.line(
            screen,
            spring_color,
            (int(anchor.x), int(anchor.y)),
            (int(ball.x), int(ball.y))
        )

        # Draw anchor point
        pygame.draw.circle(screen, (0, 0, 0), (int(anchor.x), int(anchor.y)), 2)

        # Draw ball
        pygame.draw.circle(screen, (0, 0, 0), (int(ball.x), int(ball.y)), 5)

        # Draw legend
        draw_legend(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
