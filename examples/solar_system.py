#!/usr/bin/env python3
"""
Solar System Simulation

Physics concepts demonstrated:
- Kepler's laws of planetary motion
- Orbital mechanics with multiple bodies
- Circular and elliptical orbits
- Gravitational interactions

This simulation creates a simplified solar system with a central
massive body (star) and multiple orbiting bodies (planets). Initial
velocities are calculated for approximately circular orbits.

Controls:
    T       - Toggle motion trail

Teaching applications:
- Demonstrate Kepler's third law (orbital period vs distance)
- Show how mass affects orbital dynamics
- Visualize stable orbital configurations
- Explore perturbations between orbiting bodies

Note: The simulation runs continuously for best effect.
"""

import math
import time
import pygame
from pygame.locals import QUIT, KEYDOWN, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, System
from tiny_pysics.utils import toggle

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60

# Central star mass
STAR_MASS = 400000


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Black large dot - Star
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 7)
    text = font.render("Star", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black small dot - Planets
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 3)
    text = font.render("Planets", True, (0, 0, 0))
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
    system = System()

    # Create central star
    star = PhysObject(400, 250, STAR_MASS)
    system.add_object(star)

    # Create orbiting planets
    planets = []
    for i in range(9):
        # Alternate positions left and right of star
        x_offset = ((-1) ** (i % 2)) * 40 * (i + 1)
        mass = 40 * (i + 1)

        planet = PhysObject(400 + x_offset, 250, mass)

        # Calculate orbital velocity for approximately circular orbit
        # v = sqrt(G*M/r) - simplified with our scaled constants
        orbital_velocity = ((-1) ** (i % 2)) * math.sqrt(6 * STAR_MASS / (3 * (i + 1)) ** 2)
        planet.vy = orbital_velocity

        planets.append(planet)
        system.add_object(planet)

    # Set up gravitational forces
    system.setup_gravity()

    return system, star, planets


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Solar System - Orbital Mechanics")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create simulation
    system, star, planets = create_simulation()

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
                    system, star, planets = create_simulation()
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Draw star (larger)
        pygame.draw.circle(screen, (0, 0, 0), (int(star.x), int(star.y)), 10)

        # Draw planets
        for planet in planets:
            pygame.draw.circle(screen, (0, 0, 0), (int(planet.x), int(planet.y)), 3)

        # Draw legend
        draw_legend(screen, font)

        # Update physics and measure performance
        start = time.time()
        system.update_euler()
        elapsed = time.time() - start

        # Print FPS
        # if elapsed > 0:
        #     print(f"FPS: {1/elapsed:.0f}")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
