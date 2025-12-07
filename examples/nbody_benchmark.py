#!/usr/bin/env python3
"""
N-Body Benchmark Demo

Physics concepts demonstrated:
- N-body gravitational simulation
- Computational complexity (O(n²) for pairwise forces)
- Emergent behavior in many-body systems
- Gravitational clustering

This simulation creates 60 randomly placed bodies with mutual
gravitational attraction. It serves as a benchmark for physics
engine performance and demonstrates emergent clustering behavior.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate N-body simulation concepts
- Discuss computational complexity in physics
- Show emergent gravitational structures
- Compare with galaxy formation
"""

import random
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

# Number of bodies
NUM_BODIES = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Green dot - Center of mass
    pygame.draw.circle(screen, (0, 128, 0), (15, y + 6), 5)
    text = font.render("Center of mass", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black dot - Bodies
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 2)
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

    # Create random bodies
    for _ in range(NUM_BODIES):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        mass = random.randint(5000, 30000)
        body = PhysObject(x, y, mass)
        system.add_object(body)

    # Set up mutual gravitational attraction (O(n²) forces)
    system.setup_gravity()

    return system


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"N-Body Benchmark - {NUM_BODIES} Bodies")
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

        # Draw bodies
        for obj in system.objects:
            pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), 1)

        # Draw center of mass (green)
        cm_x, cm_y, _ = center_of_mass(system.objects)
        pygame.draw.circle(screen, (0, 128, 0), (int(cm_x), int(cm_y)), 5)

        # Draw legend
        draw_legend(screen, font)

        # Update physics
        if running:
            start = time.time()
            system.update()
            elapsed = time.time() - start
            print(f"Frame time: {elapsed:.4f}s")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
