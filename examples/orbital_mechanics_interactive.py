#!/usr/bin/env python3
"""
Orbital Mechanics Interactive Demo

Physics concepts demonstrated:
- Two-body gravitational problem
- Kepler's laws of planetary motion
- Conservation of momentum and energy
- Center of mass (barycenter) of a system
- Thrust and spacecraft control

This simulation shows two bodies in mutual gravitational attraction.
The smaller body can be controlled with thrust, demonstrating how
spacecraft navigate in orbital mechanics.

Controls:
    SPACE   - Start/stop simulation
    T       - Toggle motion trail
    UP      - Apply forward thrust
    DOWN    - Apply reverse thrust
    LEFT    - Rotate counterclockwise
    RIGHT   - Rotate clockwise

Teaching applications:
- Demonstrate elliptical orbits and Kepler's laws
- Show how thrust affects orbital trajectories
- Visualize the center of mass of a two-body system
- Explore concepts like orbital insertion and escape velocity
"""

import math
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_t, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, Force, center_of_mass
from tiny_pysics.forces import GravitationalForce
from tiny_pysics.utils import deg_to_rad, toggle

# Physical constants for the simulation
SMALL_MASS = 1800
LARGE_MASS = 19000
THRUST_FORCE = 300

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
    # Black large dot - Planet
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 5)
    text = font.render("Planet", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Black small dot - Satellite
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 2)
    text = font.render("Satellite", True, (0, 0, 0))
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
    y += 18
    text = font.render("Arrows - Thrust/rotate", True, (100, 100, 100))
    screen.blit(text, (10, y))


def create_simulation():
    """Create and return simulation objects."""
    satellite = PhysObject(800, 100, SMALL_MASS)
    planet = PhysObject(800, 250, LARGE_MASS)

    planet.set_timestep(0.02)
    satellite.set_timestep(0.02)

    # Set initial velocities for orbital motion
    satellite.vx = 25
    # Set previous positions for Verlet integration
    satellite._prev_position[0] = 799.8
    planet._prev_position[0] = 800.11

    # Create gravitational forces (mutual attraction)
    gravity_on_satellite = GravitationalForce(satellite, planet)
    gravity_on_planet = GravitationalForce(planet, satellite)

    # Create thrust force (controllable)
    thrust = Force(0, 0)

    # Apply forces
    satellite.add_force(thrust)
    satellite.add_force(gravity_on_satellite, dynamic=True)
    planet.add_force(gravity_on_planet, dynamic=True)

    return satellite, planet, thrust


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Orbital Mechanics - Two Body Problem")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Create simulation
    satellite, planet, thrust = create_simulation()

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
                angle_rad = deg_to_rad(satellite.theta)

                if event.key == K_UP:
                    # Thrust in direction of rotation
                    thrust.x = THRUST_FORCE * math.sin(angle_rad)
                    thrust.y = -THRUST_FORCE * math.cos(angle_rad)
                elif event.key == K_DOWN:
                    # Reverse thrust
                    thrust.x = -THRUST_FORCE * math.sin(angle_rad)
                    thrust.y = THRUST_FORCE * math.cos(angle_rad)
                elif event.key == K_RIGHT:
                    satellite.omega += 2
                elif event.key == K_LEFT:
                    satellite.omega -= 2
                elif event.key == K_SPACE:
                    running = toggle(running)
                elif event.key == K_t:
                    trace_mode = toggle(trace_mode)
                elif event.key == K_r:
                    satellite, planet, thrust = create_simulation()
                    running = False
                    trace_mode = False
                    screen.fill((255, 255, 255))

            if event.type == KEYUP:
                if event.key in (K_UP, K_DOWN):
                    thrust.x = 0
                    thrust.y = 0

        # Update physics
        if running:
            satellite.tick()
            planet.tick()

        # Calculate center of mass
        cm_x, cm_y, _ = center_of_mass([planet, satellite])

        # Rendering
        if not trace_mode:
            screen.fill((255, 255, 255))

        # Draw center of mass (green)
        pygame.draw.circle(screen, (0, 128, 0), (int(cm_x), int(cm_y)), 5)

        # Draw planet (black, larger)
        pygame.draw.circle(screen, (0, 0, 0), (int(planet.x), int(planet.y)), 5)

        # Draw satellite (black, smaller)
        pygame.draw.circle(screen, (0, 0, 0), (int(satellite.x), int(satellite.y)), 2)

        # Draw legend
        draw_legend(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
