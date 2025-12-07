"""
Core physics simulation classes.

This module provides PhysObject for simulating physical bodies and
System for managing collections of objects with global physics.
"""

from __future__ import annotations
import threading
import numpy as np
from numpy.typing import NDArray
from typing import TYPE_CHECKING

from .core import Vector, Force

if TYPE_CHECKING:
    from .forces import CentralForce


class PhysObject:
    """
    A physical object with position, velocity, mass, and forces.

    Supports both Verlet and Euler integration methods for updating
    position based on applied forces.

    Attributes:
        x, y: Current position
        vx, vy: Current velocity
        ax, ay: Current acceleration
        mass: Object mass
        size: Collision radius
        omega: Angular velocity (radians/second)
        theta: Current rotation angle (radians)

    Example:
        >>> ball = PhysObject(100, 200, mass=1.0)
        >>> ball.set_velocity(10, 0)
        >>> ball.tick()  # Advance one timestep
    """

    _instance_count: int = 0

    def __init__(self, x: float, y: float, mass: float):
        """
        Initialize a physical object.

        Args:
            x: Initial x position
            y: Initial y position
            mass: Object mass (must be positive)
        """
        # Position (current and previous for Verlet integration)
        self._position = np.array([x, y], dtype=np.float64)
        self._prev_position = self._position.copy()

        # Velocity and acceleration
        self._velocity = np.zeros(2, dtype=np.float64)
        self._acceleration = np.zeros(2, dtype=np.float64)

        # Physical properties
        self.mass = mass
        self.size = 1.0

        # Rotation
        self.omega = 0.0  # Angular velocity
        self.theta = 0.0  # Rotation angle

        # Time step
        self._dt = 0.01
        self._dt_squared = self._dt ** 2

        # Forces
        self.static_forces: list[Force] = []
        self.dynamic_forces: list[Force] = []
        self._sum_forces = Force(0, 0)

        # Enable gravity by default
        self.gravity_enabled = True

        PhysObject._instance_count += 1

    # Position properties
    @property
    def x(self) -> float:
        """Current x position."""
        return float(self._position[0])

    @x.setter
    def x(self, value: float) -> None:
        self._position[0] = value

    @property
    def y(self) -> float:
        """Current y position."""
        return float(self._position[1])

    @y.setter
    def y(self, value: float) -> None:
        self._position[1] = value

    @property
    def position(self) -> NDArray[np.float64]:
        """Position as NumPy array [x, y]."""
        return self._position

    # Velocity properties
    @property
    def vx(self) -> float:
        """Current x velocity."""
        return float(self._velocity[0])

    @vx.setter
    def vx(self, value: float) -> None:
        self._velocity[0] = value

    @property
    def vy(self) -> float:
        """Current y velocity."""
        return float(self._velocity[1])

    @vy.setter
    def vy(self, value: float) -> None:
        self._velocity[1] = value

    @property
    def velocity(self) -> NDArray[np.float64]:
        """Velocity as NumPy array [vx, vy]."""
        return self._velocity

    # Acceleration properties
    @property
    def ax(self) -> float:
        """Current x acceleration."""
        return float(self._acceleration[0])

    @ax.setter
    def ax(self, value: float) -> None:
        self._acceleration[0] = value

    @property
    def ay(self) -> float:
        """Current y acceleration."""
        return float(self._acceleration[1])

    @ay.setter
    def ay(self, value: float) -> None:
        self._acceleration[1] = value

    @property
    def acceleration(self) -> NDArray[np.float64]:
        """Acceleration as NumPy array [ax, ay]."""
        return self._acceleration

    @property
    def dt(self) -> float:
        """Current timestep."""
        return self._dt

    # Setters
    def set_position(self, x: float, y: float) -> None:
        """Set object position."""
        self._position[0] = x
        self._position[1] = y

    def set_velocity(self, vx: float, vy: float) -> None:
        """Set object velocity."""
        self._velocity[0] = vx
        self._velocity[1] = vy

    def set_velocity_vector(self, vector: Vector) -> None:
        """Set velocity from a Vector."""
        self._velocity[0] = vector.x
        self._velocity[1] = vector.y

    def set_acceleration(self, ax: float, ay: float) -> None:
        """Set object acceleration."""
        self._acceleration[0] = ax
        self._acceleration[1] = ay

    def set_acceleration_vector(self, vector: Vector) -> None:
        """Set acceleration from a Vector."""
        self._acceleration[0] = vector.x
        self._acceleration[1] = vector.y

    def set_timestep(self, dt: float) -> None:
        """
        Set the simulation timestep.

        Args:
            dt: New timestep in seconds
        """
        self._dt = dt
        self._dt_squared = dt ** 2

    # Force management
    def add_force(self, force: Force, dynamic: bool = False) -> None:
        """
        Add a force to this object.

        Args:
            force: Force to add
            dynamic: If True, force is recalculated each step
        """
        if dynamic:
            self.dynamic_forces.append(force)
        else:
            self.static_forces.append(force)

    def add_force_xy(
        self,
        x: float,
        y: float,
        dynamic: bool = False,
        lever_arm: float = 0.0
    ) -> Force:
        """
        Create and add a force from components.

        Args:
            x: Force x component
            y: Force y component
            dynamic: If True, force updates each step
            lever_arm: Lever arm for torque calculation

        Returns:
            The created Force object
        """
        force = Force(x, y, lever_arm, dynamic)
        self.add_force(force, dynamic)
        return force

    def add_central_force(self, target: PhysObject, magnitude: float) -> None:
        """
        Add a central force toward another object.

        Args:
            target: Object to attract toward
            magnitude: Force magnitude in Newtons
        """
        from .forces import CentralForce
        force = CentralForce(self, target, magnitude)
        self.dynamic_forces.append(force)

    def sum_forces(self) -> None:
        """Calculate the sum of all forces acting on this object."""
        self._sum_forces.reset()

        # Add static forces
        for force in self.static_forces:
            self._sum_forces._data += force._data

        # Update and add dynamic forces
        for force in self.dynamic_forces:
            force.update()
            self._sum_forces._data += force._data

    # Distance calculations
    def distance(self, other: PhysObject) -> float:
        """
        Calculate Euclidean distance to another object.

        Args:
            other: Target object

        Returns:
            Distance in world units
        """
        return float(np.linalg.norm(self._position - other._position))

    def distance_squared(self, other: PhysObject) -> float:
        """
        Calculate squared distance to another object.

        More efficient than distance() when only comparing distances.

        Args:
            other: Target object

        Returns:
            Squared distance
        """
        diff = self._position - other._position
        return float(np.dot(diff, diff))

    # Physics integration
    def rotate(self) -> None:
        """Update rotation angle based on angular velocity."""
        self.theta += self._dt * self.omega

    def euler_step(self) -> None:
        """
        Perform one Euler integration step.

        Updates velocity from acceleration, then position from velocity.
        Simple but less stable than Verlet for oscillatory systems.
        """
        self._velocity += self._dt * self._acceleration
        self._position += self._dt * self._velocity

    def verlet_step(self) -> None:
        """
        Perform one Verlet integration step.

        More stable than Euler for oscillatory systems like orbits
        and springs. Uses current and previous position.
        """
        new_position = (
            2 * self._position
            - self._prev_position
            + self._acceleration * self._dt_squared
        )
        self._prev_position = self._position.copy()
        self._position = new_position

        # Update velocity estimate (for friction/damping forces)
        self._velocity = (self._position - self._prev_position) / self._dt

    def apply_newton_second_law(self) -> None:
        """
        Apply Newton's second law: a = F/m.

        Sums all forces and calculates resulting acceleration.
        """
        self.sum_forces()
        self._acceleration = self._sum_forces._data / self.mass

    def tick(self) -> None:
        """
        Advance simulation by one timestep using Verlet integration.

        Calculates forces, updates acceleration, integrates position,
        and updates rotation.
        """
        self.apply_newton_second_law()
        self.verlet_step()
        self.rotate()

    def tick_euler(self) -> None:
        """
        Advance simulation by one timestep using Euler integration.

        Calculates forces, updates acceleration, integrates position,
        and updates rotation.
        """
        self.apply_newton_second_law()
        self.euler_step()
        self.rotate()

    def __repr__(self) -> str:
        return f"PhysObject(x={self.x:.2f}, y={self.y:.2f}, mass={self.mass})"


class System:
    """
    Container for managing multiple physics objects.

    Handles global gravity setup, collision detection and response,
    and coordinated physics updates.

    Attributes:
        objects: List of PhysObject instances in the system
        dt: Global timestep
        gravity_enabled: Whether gravitational forces are active
        collisions_enabled: Whether collision detection is active

    Example:
        >>> system = System()
        >>> system.add_object(planet1)
        >>> system.add_object(planet2)
        >>> system.setup_gravity()
        >>> system.update()  # Advance all objects
    """

    def __init__(self):
        """Initialize an empty physics system."""
        self.objects: list[PhysObject] = []
        self.dt = 0.1
        self.gravity_enabled = False
        self.threading_enabled = False
        self.collisions_enabled = False
        self.bounce_enabled = False
        self._split_objects: list[list[PhysObject]] = []

    def add_object(self, obj: PhysObject) -> None:
        """
        Add an object to the system.

        Args:
            obj: PhysObject to add
        """
        self.objects.append(obj)

    def remove_object(self, obj: PhysObject) -> None:
        """
        Remove an object from the system.

        Args:
            obj: PhysObject to remove
        """
        if obj in self.objects:
            self.objects.remove(obj)

    def setup_gravity(self) -> None:
        """
        Enable gravitational attraction between all objects.

        Adds gravitational forces between every pair of objects.
        Complexity: O(n^2) where n is the number of objects.
        """
        from .forces import GravitationalForce

        self.gravity_enabled = True
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1:]:
                # Add mutual gravitational attraction
                grav1 = GravitationalForce(obj1, obj2)
                grav2 = GravitationalForce(obj2, obj1)
                obj1.add_force(grav1, dynamic=True)
                obj2.add_force(grav2, dynamic=True)

    def check_collisions(self) -> list[tuple[PhysObject, PhysObject]]:
        """
        Detect all colliding pairs of objects.

        Uses simple circle-circle collision based on object sizes.

        Returns:
            List of (object1, object2) tuples for colliding pairs
        """
        collisions = []
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1:]:
                min_dist_squared = (obj1.size + obj2.size) ** 2
                if obj1.distance_squared(obj2) < min_dist_squared:
                    collisions.append((obj1, obj2))
        return collisions

    def apply_collisions(self) -> None:
        """
        Apply elastic collision response to all colliding pairs.

        Uses center-of-mass frame for elastic collision calculation.
        """
        for obj1, obj2 in self.check_collisions():
            m1, m2 = obj1.mass, obj2.mass
            total_mass = m1 + m2

            # Calculate center of mass velocity
            v_cm = (m1 * obj1._velocity + m2 * obj2._velocity) / total_mass

            # Elastic collision in CM frame
            obj1._velocity = 2 * v_cm - obj1._velocity
            obj2._velocity = 2 * v_cm - obj2._velocity

    def split_for_threading(self, num_threads: int = 2) -> None:
        """
        Split object list for parallel processing.

        Args:
            num_threads: Number of chunks to create
        """
        from .utils import split_sequence
        self._split_objects = split_sequence(self.objects, num_threads)

    def join_from_threading(self) -> None:
        """Recombine split object list after parallel processing."""
        self.objects = []
        for chunk in self._split_objects:
            self.objects.extend(chunk)

    def update(self) -> None:
        """Update all objects using Verlet integration."""
        for obj in self.objects:
            obj.tick()

    def update_euler(self) -> None:
        """Update all objects using Euler integration."""
        for obj in self.objects:
            obj.tick_euler()

        if self.collisions_enabled:
            self.apply_collisions()

    def update_threaded(self) -> None:
        """Update objects using multiple threads."""
        threads = []
        for chunk in self._split_objects:
            thread = UpdateThread(chunk)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def set_timestep(self, dt: float) -> None:
        """
        Set timestep for all objects in the system.

        Args:
            dt: New timestep in seconds
        """
        self.dt = dt
        for obj in self.objects:
            obj.set_timestep(dt)

    def __len__(self) -> int:
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)


class UpdateThread(threading.Thread):
    """
    Worker thread for parallel physics updates.

    Used by System.update_threaded() to update subsets of objects
    in parallel.
    """

    def __init__(self, objects: list[PhysObject]):
        """
        Initialize update thread.

        Args:
            objects: List of objects to update
        """
        super().__init__()
        self.objects = objects

    def run(self) -> None:
        """Execute physics tick on all assigned objects."""
        for obj in self.objects:
            obj.tick()


def center_of_mass(objects: list[PhysObject]) -> tuple[float, float, float]:
    """
    Calculate the center of mass of a list of objects.

    Args:
        objects: List of PhysObject instances

    Returns:
        Tuple of (x_cm, y_cm, total_mass)

    Example:
        >>> x, y, mass = center_of_mass([planet1, planet2])
    """
    if not objects:
        return (0.0, 0.0, 0.0)

    total_mass = 0.0
    weighted_x = 0.0
    weighted_y = 0.0

    for obj in objects:
        total_mass += obj.mass
        weighted_x += obj.mass * obj.x
        weighted_y += obj.mass * obj.y

    if total_mass == 0:
        return (0.0, 0.0, 0.0)

    return (weighted_x / total_mass, weighted_y / total_mass, total_mass)
