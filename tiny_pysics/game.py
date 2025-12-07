"""
Game-specific physics extensions.

This module provides classes for building simple physics-based games,
with features like object selection by ID/type and coordinate serialization.
"""

from __future__ import annotations
from typing import Optional

from .physics import PhysObject, System
from .forces import GravitationalForce


class Universe(System):
    """
    Game world extending the physics System.

    Adds bounds, object selection by ID/type, and coordinate
    serialization for networking or display.

    Attributes:
        width: World width
        height: World height

    Example:
        >>> universe = Universe(800, 600)
        >>> ship = Ship(100, 100, 10, "player1")
        >>> universe.add_object(ship)
    """

    def __init__(self, width: float, height: float):
        """
        Initialize a game universe.

        Args:
            width: World width in units
            height: World height in units
        """
        super().__init__()
        self.width = width
        self.height = height

    def select_by_id(self, obj_id: str) -> list[PhysObject]:
        """
        Get all objects matching an ID.

        Args:
            obj_id: ID string to match

        Returns:
            List of matching objects
        """
        return [
            obj for obj in self.objects
            if hasattr(obj, 'id') and obj.id == obj_id
        ]

    def select_by_type(self, obj_type: str) -> list[PhysObject]:
        """
        Get all objects matching a type.

        Args:
            obj_type: Type string to match

        Returns:
            List of matching objects
        """
        return [
            obj for obj in self.objects
            if hasattr(obj, 'type') and obj.type == obj_type
        ]

    def setup_gravity(self) -> None:
        """
        Set up gravity between ships and planets.

        Unlike the base System, this only creates gravitational
        forces between ships and planets, not between all objects.
        """
        self.gravity_enabled = True

        ships = self.select_by_type("ship")
        planets = self.select_by_type("planet")

        for ship in ships:
            for planet in planets:
                if ship != planet:
                    grav = GravitationalForce(ship, planet)
                    ship.add_force(grav, dynamic=True)

    def get_all_coordinates(self) -> list[tuple[float, float, float, str]]:
        """
        Get position and rotation of all objects.

        Returns:
            List of (x, y, theta, id) tuples
        """
        result = []
        for obj in self.objects:
            obj_id = getattr(obj, 'id', '')
            result.append((obj.x, obj.y, obj.theta, obj_id))
        return result


class Ship(PhysObject):
    """
    Game entity representing a spacecraft or vehicle.

    Extends PhysObject with ID and type attributes for
    game logic and networking.

    Attributes:
        id: Unique identifier string
        type: Object type (default "ship")

    Example:
        >>> player = Ship(100, 200, mass=50, obj_id="player1")
        >>> player.type = "ship"
    """

    def __init__(
        self,
        x: float,
        y: float,
        mass: float,
        obj_id: str,
        obj_type: str = "ship"
    ):
        """
        Initialize a ship.

        Args:
            x: Initial x position
            y: Initial y position
            mass: Ship mass
            obj_id: Unique identifier
            obj_type: Object type (default "ship")
        """
        super().__init__(x, y, mass)
        self.id = obj_id
        self.type = obj_type

    def __repr__(self) -> str:
        return f"Ship(id={self.id!r}, x={self.x:.2f}, y={self.y:.2f})"


def coordinates_to_string(coordinates: list[tuple]) -> str:
    """
    Serialize coordinates to a string format.

    Useful for network transmission or file I/O.

    Args:
        coordinates: List of (x, y, theta, id) tuples

    Returns:
        Space-separated, newline-delimited string

    Example:
        >>> coords = [(100, 200, 1.5, "ship1")]
        >>> coordinates_to_string(coords)
        '100 200 1.5 ship1\\n'
    """
    lines = []
    for coord in coordinates:
        line = " ".join(str(x) for x in coord)
        lines.append(line)
    return "\n".join(lines) + "\n" if lines else ""
