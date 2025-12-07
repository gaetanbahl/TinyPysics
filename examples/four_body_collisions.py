#!/usr/bin/env python3
"""
Four Body Collisions Demo

Physics concepts demonstrated:
- N-body gravitational dynamics
- Gravitational collapse
- Collision physics in gravitating systems
- Center of mass conservation

This simulation shows four gravitating bodies that can also collide.
It demonstrates how gravitational systems can lead to close encounters
and collisions.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate gravitational clustering
- Show how stars form through collapse
- Explore planetary collision scenarios
- Visualize gravitational three-body interactions
"""

import time
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, System, center_of_mass
from tiny_pysics.utils import toggle

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Green dot - Center of mass
    pygame.draw.circle(screen, (0, 128, 0), (15, y + 6), 5)
    text = font.render("Center of mass", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black dot - Bodies
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 5)
    text = font.render("Gravitating bodies", True, (0, 0, 0))
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
    system = System()

    # Create four bodies with different masses
    body1 = PhysObject(60, 500, 15000)
    body2 = PhysObject(600, 150, 19000)
    body3 = PhysObject(300, 250, 22000)
    body4 = PhysObject(200, 450, 19000)

    system.add_object(body1)
    system.add_object(body2)
    system.add_object(body3)
    system.add_object(body4)

    # Set up mutual gravitational attraction
    system.setup_gravity()

    # Enable collision detection
    system.collisions_enabled = True

    # Set collision radii (proportional to mass)
    for obj in system.objects:
        obj.size = 10

    return system


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Four Body Collisions - Gravitational Dynamics")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create simulation
    system = create_simulation()

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
                    system = create_simulation()
                    running = False
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Draw bodies (size proportional to mass)
        for obj in system.objects:
            radius = int(obj.mass / 2000)
            pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), max(radius, 2))

        # Draw center of mass (green)
        cm_x, cm_y, _ = center_of_mass(system.objects)
        pygame.draw.circle(screen, (0, 128, 0), (int(cm_x), int(cm_y)), 5)

        # Draw legend
        draw_legend(screen, font)

        # Update physics
        if running:
            start = time.time()
            system.update_euler()
            elapsed = time.time() - start

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
