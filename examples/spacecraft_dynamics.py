#!/usr/bin/env python3
"""
Spacecraft Dynamics Demo

Physics concepts demonstrated:
- Rotational dynamics
- Directional thrust relative to orientation
- Orbital mechanics with active control
- Sprite-based visualization

This simulation shows a spacecraft orbiting a planet with full
rotational control and thrust capability. The ship sprite rotates
to show orientation.

Controls:
    UP      - Apply forward thrust
    DOWN    - Apply reverse thrust
    LEFT    - Rotate counterclockwise
    RIGHT   - Rotate clockwise

Teaching applications:
- Demonstrate rocket equation basics
- Show orbital maneuvering
- Explore attitude control systems
- Visualize spacecraft navigation

Note: Requires triangle.png sprite in assets folder.
      If not found, uses a simple circle.
"""

import math
import os
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_r

import sys
sys.path.insert(0, '..')

from tiny_pysics import PhysObject, Force
from tiny_pysics.forces import GravitationalForce

# Physical constants
GRAVITY = 9.81
THRUST_FORCE = 2000

# Window setup
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 560
FPS = 60


def draw_legend(screen, font):
    """Draw legend in top-left corner."""
    y = 10
    # Black large dot - Planet
    pygame.draw.circle(screen, (0, 0, 0), (15, y + 6), 7)
    text = font.render("Planet", True, (0, 0, 0))
    screen.blit(text, (25, y))
    y += 20
    # Triangle - Ship
    pygame.draw.polygon(screen, (0, 0, 0), [(15, y), (10, y + 12), (20, y + 12)])
    text = font.render("Spacecraft", True, (0, 0, 0))
    screen.blit(text, (25, y))
    # Keybinds
    y += 30
    text = font.render("Arrows - Thrust/rotate", True, (100, 100, 100))
    screen.blit(text, (10, y))
    y += 18
    text = font.render("R - Reset", True, (100, 100, 100))
    screen.blit(text, (10, y))


def create_simulation():
    """Create and return simulation objects."""
    ship = PhysObject(400, 100, 600)
    planet = PhysObject(400, 250, 5000)

    # Set initial velocity
    ship.vx = 10
    ship.vy = 0
    ship.set_timestep(0.1)

    # Create gravitational force
    gravity = GravitationalForce(ship, planet)

    # Create controllable thrust
    thrust = Force(0, 0)

    # Apply forces
    ship.add_force(thrust)
    ship.add_force(gravity, dynamic=True)

    return ship, planet, thrust


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Spacecraft Dynamics - Orbital Control")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Try to load ship sprite, fall back to None if not found
    sprite_path = os.path.join(os.path.dirname(__file__), 'assets', 'rocket.png')
    try:
        ship_sprite = pygame.image.load(sprite_path).convert_alpha()
        ship_sprite = pygame.transform.scale(ship_sprite, (50, 50))
        ship_sprite = pygame.transform.rotate(ship_sprite, 45)
        use_sprite = True
    except (FileNotFoundError, pygame.error):
        print(f"Note: Ship sprite not found at {sprite_path}")
        print("Using simple triangle for ship visualization.")
        ship_sprite = None
        use_sprite = False

    # Enable key repeat for smooth control
    pygame.key.set_repeat(30, 30)

    # Create simulation
    ship, planet, thrust = create_simulation()

    # Main loop
    loop = True

    while loop:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False

            if event.type == KEYDOWN:
                theta_rad = math.pi * ship.theta / 180

                if event.key == K_UP:
                    thrust.x = THRUST_FORCE * math.sin(theta_rad)
                    thrust.y = -THRUST_FORCE * math.cos(theta_rad)
                elif event.key == K_DOWN:
                    thrust.x = -THRUST_FORCE * math.sin(theta_rad)
                    thrust.y = THRUST_FORCE * math.cos(theta_rad)
                elif event.key == K_RIGHT:
                    ship.omega += 1
                elif event.key == K_LEFT:
                    ship.omega -= 1
                elif event.key == K_r:
                    ship, planet, thrust = create_simulation()
                    screen.fill((255, 255, 255))

            if event.type == KEYUP:
                if event.key in (K_UP, K_DOWN):
                    thrust.x = 0
                    thrust.y = 0

        # Update physics
        ship.tick_euler()

        # Rendering
        screen.fill((255, 255, 255))

        # Draw planet
        pygame.draw.circle(screen, (0, 0, 0), (int(planet.x), int(planet.y)), 10)

        # Draw ship (sprite or circle)
        if use_sprite:
            rotated = pygame.transform.rotate(ship_sprite, -ship.theta)
            rect = rotated.get_rect(center=(int(ship.x), int(ship.y)))
            screen.blit(rotated, rect)
        else:
            # Draw a simple triangle to show orientation
            theta_rad = math.radians(ship.theta)
            size = 15

            # Triangle vertices
            front = (
                ship.x + size * math.sin(theta_rad),
                ship.y - size * math.cos(theta_rad)
            )
            back_left = (
                ship.x - size * 0.5 * math.sin(theta_rad) - size * 0.5 * math.cos(theta_rad),
                ship.y + size * 0.5 * math.cos(theta_rad) - size * 0.5 * math.sin(theta_rad)
            )
            back_right = (
                ship.x - size * 0.5 * math.sin(theta_rad) + size * 0.5 * math.cos(theta_rad),
                ship.y + size * 0.5 * math.cos(theta_rad) + size * 0.5 * math.sin(theta_rad)
            )

            pygame.draw.polygon(screen, (0, 0, 0), [front, back_left, back_right])

        # Draw legend
        draw_legend(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
