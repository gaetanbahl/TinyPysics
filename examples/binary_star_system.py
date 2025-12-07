#!/usr/bin/env python3
"""
Binary Star System Demo

Physics concepts demonstrated:
- Gravitational field superposition
- Lagrange points
- Complex orbital trajectories
- Three-body dynamics

This simulation shows a small body orbiting around two massive
attractors (binary star system). The resulting trajectory can
be highly complex due to the competing gravitational fields.

Controls:
    T       - Toggle motion trail (recommended for seeing complex orbits)

Teaching applications:
- Demonstrate gravitational field addition
- Explore Lagrange point concepts
- Show chaotic vs stable orbital regions
- Discuss binary star planetary systems

Note: The simulation runs continuously for best effect.
"""

import random
import time
import pygame
from pygame.locals import QUIT, KEYDOWN, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject
from tiny_pysics.forces import GravitationalForce
from tiny_pysics.utils import toggle

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Black large dot - Stars
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 7)
    text = font.render("Binary stars", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black small dot - Orbiter
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 3)
    text = font.render("Orbiting body", True, (0, 0, 0))
    screen.blit(text, (25, y))
    # Keybinds
    y += 30
    text = font.render("T - Toggle trail", True, (100, 100, 100))
    screen.blit(text, (10, y))
    y += 18
    text = font.render("R - Reset", True, (100, 100, 100))
    screen.blit(text, (10, y))


def create_simulation():
    """Create and return simulation objects."""
    # Create binary star system
    star1 = PhysObject(400, 250, 4000)  # First star
    star2 = PhysObject(600, 250, 7000)  # Second star (more massive)

    # Create orbiting body (satellite or planet)
    orbiter = PhysObject(
        random.randint(200, 500),
        random.randint(150, 300),
        80
    )

    # Add gravitational forces from both stars
    grav1 = GravitationalForce(orbiter, star1)
    grav2 = GravitationalForce(orbiter, star2)
    orbiter.add_force(grav1, dynamic=True)
    orbiter.add_force(grav2, dynamic=True)

    # Set timestep
    orbiter.set_timestep(0.05)

    # Give initial velocity via Verlet previous position
    orbiter._prev_position[0] = orbiter.x + 0.5
    orbiter._prev_position[1] = orbiter.y - 0.5
    orbiter.vx = -10
    orbiter.vy = 10

    return star1, star2, orbiter


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Binary Star System - Dual Gravity")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create simulation
    star1, star2, orbiter = create_simulation()

    # Simulation state
    trace_mode = False
    loop = True

    while loop:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False

            if event.type == KEYDOWN:
                if event.key == K_t:
                    trace_mode = toggle(trace_mode)
                elif event.key == K_r:
                    star1, star2, orbiter = create_simulation()
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Draw stars
        pygame.draw.circle(screen, (0, 0, 0), (int(star1.x), int(star1.y)), 10)
        pygame.draw.circle(screen, (0, 0, 0), (int(star2.x), int(star2.y)), 10)

        # Draw orbiter
        pygame.draw.circle(screen, (0, 0, 0), (int(orbiter.x), int(orbiter.y)), 3)

        # Draw legend
        draw_legend(screen, font)

        # Update physics and measure performance
        start = time.time()
        orbiter.tick_euler()
        elapsed = time.time() - start

        # Print FPS
        if elapsed > 0:
            print(f"FPS: {1/elapsed:.0f}")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
