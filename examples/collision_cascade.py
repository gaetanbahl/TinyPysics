#!/usr/bin/env python3
"""
Collision Cascade Demo

Physics concepts demonstrated:
- Multiple body collisions
- Momentum transfer chains
- Friction and energy dissipation
- Newton's cradle effect

This simulation shows one fast-moving object colliding with a
row of stationary objects, creating a cascade of collisions.
Friction gradually brings the system to rest.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate chain momentum transfer
- Show energy loss due to friction
- Visualize Newton's cradle physics
- Explore inelastic effects in real systems
"""

import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, System, center_of_mass
from tiny_pysics.forces import Friction
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
    # Red dot - Objects
    pygame.draw.circle(screen, (128, 0, 0), (15, y + 6), 5)
    text = font.render("Colliding objects", True, (0, 0, 0))
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

    # Create the impactor (fast-moving)
    impactor = PhysObject(200, 250, 15000)
    impactor.vx = 250
    impactor.vy = 0
    system.add_object(impactor)

    # Create target objects (stationary)
    prev = 400
    for i in range(5):
        target = PhysObject(random.randint(prev, prev + 50), 250, 15000)
        system.add_object(target)
        prev = target.x + 20

    # Add friction to all objects
    # for obj in system.objects:
    #     friction = Friction(obj, k=7, power=3)  # Cubic friction
    #     obj.add_force(friction, dynamic=True)

    # Enable collision detection
    system.collisions_enabled = True

    # Set collision radii
    for obj in system.objects:
        obj.size = 10

    # Set timestep
    system.set_timestep(0.01)

    return system


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Collision Cascade - Chain Momentum Transfer")
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

        # Draw all objects
        for obj in system.objects:
            pygame.draw.circle(screen, (128, 0, 0), (int(obj.x), int(obj.y)), 10)

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
