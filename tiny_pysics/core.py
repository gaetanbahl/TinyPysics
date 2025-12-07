"""
Core vector and force classes for physics simulations.

This module provides the fundamental Vector and Force classes that form
the basis of all physics calculations in tiny_pysics.
"""

from __future__ import annotations
import numpy as np
from numpy.typing import NDArray
from typing import Union


class Vector:
    """
    2D vector with NumPy backend for efficient physics calculations.

    Provides both property-based access (.x, .y) for convenience and
    direct array access (._data) for efficient NumPy operations.

    Attributes:
        x: X component of the vector
        y: Y component of the vector

    Example:
        >>> v1 = Vector(3, 4)
        >>> v1.magnitude()
        5.0
        >>> v2 = Vector(1, 0)
        >>> v1 + v2
        Vector(4.0, 4.0)
    """

    __slots__ = ('_data',)

    def __init__(self, x: float = 0.0, y: float = 0.0):
        """
        Initialize a 2D vector.

        Args:
            x: X component (default 0.0)
            y: Y component (default 0.0)
        """
        self._data: NDArray[np.float64] = np.array([x, y], dtype=np.float64)

    @classmethod
    def from_array(cls, arr: NDArray) -> Vector:
        """
        Create a Vector from a NumPy array.

        Args:
            arr: NumPy array with at least 2 elements

        Returns:
            New Vector instance
        """
        v = cls.__new__(cls)
        v._data = np.asarray(arr[:2], dtype=np.float64).copy()
        return v

    @classmethod
    def from_polar(cls, magnitude: float, angle: float) -> Vector:
        """
        Create a Vector from polar coordinates.

        Args:
            magnitude: Length of the vector
            angle: Angle in radians (0 = positive x-axis)

        Returns:
            New Vector instance
        """
        return cls(magnitude * np.cos(angle), magnitude * np.sin(angle))

    @property
    def x(self) -> float:
        """X component of the vector."""
        return float(self._data[0])

    @x.setter
    def x(self, value: float) -> None:
        self._data[0] = value

    @property
    def y(self) -> float:
        """Y component of the vector."""
        return float(self._data[1])

    @y.setter
    def y(self, value: float) -> None:
        self._data[1] = value

    def set(self, x: float, y: float) -> None:
        """
        Set both components of the vector.

        Args:
            x: New X component
            y: New Y component
        """
        self._data[0] = x
        self._data[1] = y

    def copy(self) -> Vector:
        """Create a copy of this vector."""
        return Vector.from_array(self._data)

    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        Returns:
            The Euclidean length of the vector
        """
        return float(np.linalg.norm(self._data))

    def magnitude_squared(self) -> float:
        """
        Calculate the squared magnitude of the vector.

        More efficient than magnitude() when only comparing lengths.

        Returns:
            The squared length of the vector
        """
        return float(np.dot(self._data, self._data))

    def normalized(self) -> Vector:
        """
        Return a unit vector in the same direction.

        Returns:
            New Vector with magnitude 1, or zero vector if magnitude is 0
        """
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return Vector.from_array(self._data / mag)

    def normalize(self) -> None:
        """Normalize this vector in place to unit length."""
        mag = self.magnitude()
        if mag != 0:
            self._data /= mag

    def dot(self, other: Vector) -> float:
        """
        Calculate the dot product with another vector.

        Args:
            other: Vector to dot with

        Returns:
            Scalar dot product
        """
        return float(np.dot(self._data, other._data))

    def cross(self, other: Vector) -> float:
        """
        Calculate the 2D cross product (z-component of 3D cross product).

        Args:
            other: Vector to cross with

        Returns:
            Scalar representing the z-component
        """
        return float(self._data[0] * other._data[1] - self._data[1] * other._data[0])

    def angle(self) -> float:
        """
        Calculate the angle of this vector from the positive x-axis.

        Returns:
            Angle in radians (-pi to pi)
        """
        return float(np.arctan2(self._data[1], self._data[0]))

    def angle_to(self, other: Vector) -> float:
        """
        Calculate the angle from this vector to another.

        Args:
            other: Target vector

        Returns:
            Angle in radians
        """
        return float(np.arctan2(
            self.cross(other),
            self.dot(other)
        ))

    def rotate(self, angle: float) -> Vector:
        """
        Return a rotated copy of this vector.

        Args:
            angle: Rotation angle in radians (counterclockwise)

        Returns:
            New rotated Vector
        """
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        return Vector(
            self._data[0] * cos_a - self._data[1] * sin_a,
            self._data[0] * sin_a + self._data[1] * cos_a
        )

    def distance_to(self, other: Vector) -> float:
        """
        Calculate the distance to another vector (as a point).

        Args:
            other: Target vector/point

        Returns:
            Euclidean distance
        """
        return float(np.linalg.norm(self._data - other._data))

    # Arithmetic operators
    def __add__(self, other: Vector) -> Vector:
        """Add two vectors."""
        return Vector.from_array(self._data + other._data)

    def __iadd__(self, other: Vector) -> Vector:
        """Add another vector in place."""
        self._data += other._data
        return self

    def __sub__(self, other: Vector) -> Vector:
        """Subtract two vectors."""
        return Vector.from_array(self._data - other._data)

    def __isub__(self, other: Vector) -> Vector:
        """Subtract another vector in place."""
        self._data -= other._data
        return self

    def __mul__(self, scalar: float) -> Vector:
        """Multiply vector by a scalar."""
        return Vector.from_array(self._data * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        """Multiply vector by a scalar (reversed)."""
        return Vector.from_array(self._data * scalar)

    def __imul__(self, scalar: float) -> Vector:
        """Multiply by a scalar in place."""
        self._data *= scalar
        return self

    def __truediv__(self, scalar: float) -> Vector:
        """Divide vector by a scalar."""
        return Vector.from_array(self._data / scalar)

    def __itruediv__(self, scalar: float) -> Vector:
        """Divide by a scalar in place."""
        self._data /= scalar
        return self

    def __neg__(self) -> Vector:
        """Negate the vector."""
        return Vector.from_array(-self._data)

    def __pos__(self) -> Vector:
        """Return a copy of the vector."""
        return self.copy()

    # Comparison operators
    def __eq__(self, other: object) -> bool:
        """Check if two vectors are equal."""
        if not isinstance(other, Vector):
            return NotImplemented
        return np.allclose(self._data, other._data)

    def __ne__(self, other: object) -> bool:
        """Check if two vectors are not equal."""
        if not isinstance(other, Vector):
            return NotImplemented
        return not np.allclose(self._data, other._data)

    # String representations
    def __repr__(self) -> str:
        return f"Vector({self._data[0]:.6g}, {self._data[1]:.6g})"

    def __str__(self) -> str:
        return f"({self._data[0]:.4g}, {self._data[1]:.4g})"


class Force(Vector):
    """
    A force vector with additional properties for physics simulations.

    Extends Vector with magnitude tracking, lever arm for torque calculations,
    and support for dynamic updates.

    Attributes:
        x: X component of the force
        y: Y component of the force
        lever_arm: Distance from rotation axis for torque calculations
        dynamic: Whether this force updates each simulation step
        id: Optional identifier for the force

    Example:
        >>> gravity = Force(0, -9.81 * mass)
        >>> spring = Force(0, 0, dynamic=True)
    """

    __slots__ = ('lever_arm', 'dynamic', 'id', '_magnitude')

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        lever_arm: float = 0.0,
        dynamic: bool = False
    ):
        """
        Initialize a force vector.

        Args:
            x: X component of force (Newtons)
            y: Y component of force (Newtons)
            lever_arm: Distance from rotation axis for torque
            dynamic: If True, force updates each simulation step
        """
        super().__init__(x, y)
        self.lever_arm = lever_arm
        self.dynamic = dynamic
        self.id: str = ""
        self._magnitude = self.magnitude()

    @property
    def newtons(self) -> float:
        """Get the magnitude of the force in Newtons."""
        return self._magnitude

    @newtons.setter
    def newtons(self, value: float) -> None:
        """Set the magnitude while preserving direction."""
        self._magnitude = value

    def direction_between(self, point_a: tuple, point_b: tuple) -> None:
        """
        Set force direction from point A toward point B.

        The force magnitude is preserved, only direction changes.

        Args:
            point_a: Starting point (x, y)
            point_b: Target point (x, y)
        """
        xa, ya = point_a
        xb, yb = point_b
        dx = xb - xa
        dy = yb - ya
        distance = np.sqrt(dx * dx + dy * dy)
        if distance > 0:
            self._data[0] = self._magnitude * (dx / distance)
            self._data[1] = self._magnitude * (dy / distance)

    def reset(self) -> None:
        """Reset the force to zero."""
        self._data[0] = 0
        self._data[1] = 0

    def update(self) -> None:
        """
        Update the force for dynamic forces.

        Override this method in subclasses for forces that change
        based on object positions or velocities.
        """
        pass

    def torque(self) -> float:
        """
        Calculate the torque produced by this force.

        Returns:
            Torque magnitude (force magnitude * lever arm)
        """
        return self._magnitude * self.lever_arm

    def copy(self) -> Force:
        """Create a copy of this force."""
        f = Force(self.x, self.y, self.lever_arm, self.dynamic)
        f.id = self.id
        f._magnitude = self._magnitude
        return f

    def __repr__(self) -> str:
        return f"Force({self._data[0]:.6g}, {self._data[1]:.6g})"
