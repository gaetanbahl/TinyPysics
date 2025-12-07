"""
Force classes for physics simulations.

This module provides specialized force classes for common physical
interactions: friction, gravity, springs, and general central forces.
"""

from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING

from .core import Force

if TYPE_CHECKING:
    from .physics import PhysObject


# Gravitational constant (scaled for simulation, not SI units)
G = 6.67


class Friction(Force):
    """
    Velocity-dependent friction/damping force.

    Applies a force opposing the object's velocity, proportional to
    velocity raised to a power.

    Formula: F = -k * v^power

    Attributes:
        obj: Object experiencing friction
        k: Friction coefficient
        power: Velocity exponent (1 for linear, 2 for quadratic)

    Example:
        >>> # Linear damping
        >>> friction = Friction(ball, k=0.1, power=1)
        >>> ball.add_force(friction, dynamic=True)
    """

    def __init__(self, obj: PhysObject, k: float, power: float = 1):
        """
        Initialize friction force.

        Args:
            obj: Object to apply friction to
            k: Friction coefficient
            power: Velocity exponent (default 1 for linear damping)
        """
        self.obj = obj
        self.k = k
        self.power = power

        # Calculate initial force
        fx = -k * (obj.vx ** power) if obj.vx >= 0 else k * ((-obj.vx) ** power)
        fy = -k * (obj.vy ** power) if obj.vy >= 0 else k * ((-obj.vy) ** power)

        super().__init__(fx, fy, dynamic=True)

    def update(self) -> None:
        """Recalculate friction based on current velocity."""
        vx, vy = self.obj.vx, self.obj.vy

        # Handle sign correctly for odd powers
        if self.power % 2 == 1:  # Odd power
            self._data[0] = -self.k * (abs(vx) ** self.power) * np.sign(vx)
            self._data[1] = -self.k * (abs(vy) ** self.power) * np.sign(vy)
        else:  # Even power
            self._data[0] = -self.k * (vx ** self.power)
            self._data[1] = -self.k * (vy ** self.power)


class CentralForce(Force):
    """
    Force directed between two objects.

    A central force always points from one object toward another,
    with magnitude that can be constant or updated dynamically.

    Attributes:
        obj1: Object experiencing the force
        obj2: Object the force is directed toward
        magnitude: Force magnitude in Newtons

    Example:
        >>> # Constant attraction
        >>> attraction = CentralForce(ship, planet, magnitude=100)
        >>> ship.add_force(attraction, dynamic=True)
    """

    def __init__(self, obj1: PhysObject, obj2: PhysObject, magnitude: float):
        """
        Initialize central force.

        Args:
            obj1: Object experiencing the force
            obj2: Target object (force points toward this)
            magnitude: Force magnitude in Newtons
        """
        super().__init__(0, 0, dynamic=True)
        self.obj1 = obj1
        self.obj2 = obj2
        self._magnitude = magnitude
        self.update()

    def set_objects(self, obj1: PhysObject, obj2: PhysObject) -> None:
        """
        Change which objects the force acts between.

        Args:
            obj1: New source object
            obj2: New target object
        """
        self.obj1 = obj1
        self.obj2 = obj2

    def update_magnitude(self) -> None:
        """
        Recalculate force magnitude.

        Override in subclasses for distance-dependent forces.
        """
        pass

    def update_direction(self) -> None:
        """Update force direction to point from obj1 toward obj2."""
        point_a = (self.obj1.x, self.obj1.y)
        point_b = (self.obj2.x, self.obj2.y)
        self.update_magnitude()
        self.direction_between(point_a, point_b)

    def update(self) -> None:
        """Update both magnitude and direction."""
        self.update_direction()


class GravitationalForce(CentralForce):
    """
    Gravitational attraction between two objects.

    Implements Newton's law of universal gravitation:
    F = G * m1 * m2 / r^2

    Note: Uses a scaled gravitational constant (G = 6.67) suitable
    for simulation, not the SI value (6.674e-11).

    Attributes:
        obj1: Object experiencing the force
        obj2: Object attracting obj1

    Example:
        >>> grav = GravitationalForce(planet, star)
        >>> planet.add_force(grav, dynamic=True)
    """

    def __init__(self, obj1: PhysObject, obj2: PhysObject):
        """
        Initialize gravitational force.

        Args:
            obj1: Object experiencing gravitational pull
            obj2: Object providing gravitational attraction
        """
        # Calculate initial magnitude
        distance_sq = obj1.distance_squared(obj2)
        if distance_sq < 1e-10:
            distance_sq = 1e-10  # Prevent division by zero

        magnitude = (G * obj1.mass * obj2.mass) / distance_sq
        super().__init__(obj1, obj2, magnitude)

    def update_magnitude(self) -> None:
        """Recalculate gravitational force based on current distance."""
        distance_sq = self.obj1.distance_squared(self.obj2)
        if distance_sq < 1e-10:
            distance_sq = 1e-10  # Prevent division by zero

        self._magnitude = (G * self.obj1.mass * self.obj2.mass) / distance_sq

    def update(self) -> None:
        """Update gravitational force magnitude and direction."""
        self.update_magnitude()
        self.update_direction()


class ElasticForce(CentralForce):
    """
    Elastic/spring force between two objects.

    Implements Hooke's law: F = k * (distance - rest_length)

    The force is attractive when stretched beyond rest length
    and repulsive when compressed below rest length.

    Attributes:
        obj1: Object experiencing the force
        obj2: Object connected via spring
        rest_length: Natural length of the spring
        k: Spring constant (stiffness)

    Example:
        >>> spring = ElasticForce(ball1, ball2, rest_length=50, k=10)
        >>> ball1.add_force(spring, dynamic=True)
    """

    def __init__(
        self,
        obj1: PhysObject,
        obj2: PhysObject,
        rest_length: float,
        k: float
    ):
        """
        Initialize elastic/spring force.

        Args:
            obj1: Object experiencing the force
            obj2: Object connected to
            rest_length: Natural length of the spring
            k: Spring constant (Newtons per unit length)
        """
        self.rest_length = rest_length
        self.k = k

        # Calculate initial magnitude
        displacement = obj1.distance(obj2) - rest_length
        magnitude = k * displacement

        super().__init__(obj1, obj2, magnitude)

    def update_magnitude(self) -> None:
        """Recalculate spring force based on current stretch."""
        displacement = self.obj1.distance(self.obj2) - self.rest_length
        self._magnitude = self.k * displacement

    def update(self) -> None:
        """Update spring force magnitude and direction."""
        self.update_magnitude()
        self.update_direction()
