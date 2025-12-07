#!/usr/bin/env python3
"""
Elastic Collision Demo

Physics concepts demonstrated:
- Conservation of momentum
- Conservation of kinetic energy
- Elastic collision mechanics
- Center of mass reference frame

This simulation shows two objects colliding elastically. The center
of mass velocity is preserved, and both momentum and kinetic energy
are conserved.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate momentum conservation (p1 + p2 = constant)
- Show kinetic energy conservation in elastic collisions
- Visualize center of mass frame transformations
- Compare masses and resulting velocities after collision
"""

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
    # Red dot - Object 1
    pygame.draw.circle(screen, (128, 0, 0), (15, y + 6), 5)
    text = font.render("Object 1 (fast)", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Blue dot - Object 2
    pygame.draw.circle(screen, (0, 0, 128), (15, y + 6), 5)
    text = font.render("Object 2 (slow)", True, (0, 0, 0))
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

    # Create two objects with equal masses
    object1 = PhysObject(900, WINDOW_HEIGHT//2, 15000)  # Moving left
    object2 = PhysObject(600, WINDOW_HEIGHT//2, 15000)  # Moving left slowly

    system.add_object(object1)
    system.add_object(object2)

    # Set initial velocities
    object1.vx = -50  # Fast, moving left
    object2.vx = -5   # Slow, moving left

    # Enable collision detection
    system.collisions_enabled = True

    # Set collision radii
    for obj in system.objects:
        obj.size = 20

    # Set timestep
    system.set_timestep(0.1)

    return system, object1, object2


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Elastic Collision - Momentum Conservation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create simulation
    system, object1, object2 = create_simulation()

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
                    system, object1, object2 = create_simulation()
                    running = False
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Draw objects with different colors
        pygame.draw.circle(screen, (128, 0, 0), (int(object1.x), int(object1.y)), 10)
        pygame.draw.circle(screen, (0, 0, 128), (int(object2.x), int(object2.y)), 10)

        # Draw center of mass (green)
        cm_x, cm_y, _ = center_of_mass(system.objects)
        pygame.draw.circle(screen, (0, 128, 0), (int(cm_x), int(cm_y)), 5)

        # Draw legend
        draw_legend(screen, font)

        # Update physics
        if running:
            system.update_euler()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
