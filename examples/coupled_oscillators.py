#!/usr/bin/env python3
"""
Coupled Oscillators Demo

Physics concepts demonstrated:
- Coupled harmonic motion
- Normal modes of oscillation
- Energy transfer between oscillators
- Center of mass conservation

This simulation shows two masses connected by a spring. The center
of mass remains stationary while the masses oscillate about it.
This is a fundamental model for molecular vibrations and waves.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail

Teaching applications:
- Demonstrate coupled oscillator dynamics
- Show normal modes (in-phase and out-of-phase)
- Visualize molecular vibration models
- Explore energy exchange in coupled systems
"""

import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, center_of_mass
from tiny_pysics.forces import ElasticForce
from tiny_pysics.utils import toggle

# Physical constants
MASS_1 = 5
MASS_2 = 10
REST_LENGTH = 100
SPRING_CONSTANT = 0.5
TIMESTEP = 0.05

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Green dot - Center of mass
    pygame.draw.circle(screen, (0, 100, 0), (15, y + 6), 2)
    text = font.render("Center of mass", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black dots - Masses
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 5)
    text = font.render("Masses (size = mass)", True, (0, 0, 0))
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
    mass1 = PhysObject(600, 250, MASS_1)
    mass2 = PhysObject(500, 250, MASS_2)
    mass1.set_timestep(TIMESTEP)
    mass2.set_timestep(TIMESTEP)

    # Create symmetric spring forces
    spring1 = ElasticForce(mass1, mass2, REST_LENGTH, SPRING_CONSTANT)
    spring2 = ElasticForce(mass2, mass1, REST_LENGTH, SPRING_CONSTANT)

    # Apply forces
    mass1.add_force(spring1, dynamic=True)
    mass2.add_force(spring2, dynamic=True)

    # Give initial displacement (via Verlet previous position)
    mass1._prev_position[0] = 601

    return mass1, mass2


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Coupled Oscillators - Spring Connection")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    screen.fill((255, 255, 255))

    # Create simulation
    mass1, mass2 = create_simulation()

    # Initial center of mass (should remain constant)
    cm_x, cm_y, _ = center_of_mass([mass1, mass2])

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
                    mass1, mass2 = create_simulation()
                    cm_x, cm_y, _ = center_of_mass([mass1, mass2])
                    running = False
                    trace_mode = False
                    screen.fill((255, 255, 255))

        # Update physics
        if running:
            mass1.tick()
            mass2.tick()
            cm_x, cm_y, _ = center_of_mass([mass1, mass2])

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Calculate spring stretch for color coding
        distance = mass1.distance(mass2)
        stretch_factor = 1 - math.exp(-distance / 160)
        spring_color = (int(254 * stretch_factor), 0, 0)

        # Draw spring line
        pygame.draw.line(
            screen,
            spring_color,
            (int(mass2.x), int(mass2.y)),
            (int(mass1.x), int(mass1.y))
        )

        # Draw masses (size proportional to mass)
        pygame.draw.circle(screen, (0, 0, 0), (int(mass2.x), int(mass2.y)), int(mass2.mass))
        pygame.draw.circle(screen, (0, 0, 0), (int(mass1.x), int(mass1.y)), int(mass1.mass))

        # Draw center of mass (green, should stay fixed)
        pygame.draw.circle(screen, (0, 100, 0), (int(cm_x), int(cm_y)), 2)

        # Draw legend
        draw_legend(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
