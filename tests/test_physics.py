"""
Unit tests for tiny_pysics.physics module.

Tests PhysObject and System classes including:
- Object creation and properties
- Force management
- Integration methods
- Distance calculations
- System updates and gravity
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '..')

from tiny_pysics.physics import PhysObject, System, center_of_mass
from tiny_pysics.core import Force, Vector


class TestPhysObject:
    """Tests for the PhysObject class."""

    def test_creation(self):
        """Test object creation."""
        obj = PhysObject(100, 200, 50)
        assert obj.x == 100
        assert obj.y == 200
        assert obj.mass == 50

    def test_initial_velocity(self):
        """Test that initial velocity is zero."""
        obj = PhysObject(0, 0, 1)
        assert obj.vx == 0
        assert obj.vy == 0

    def test_initial_acceleration(self):
        """Test that initial acceleration is zero."""
        obj = PhysObject(0, 0, 1)
        assert obj.ax == 0
        assert obj.ay == 0

    def test_set_position(self):
        """Test position setting."""
        obj = PhysObject(0, 0, 1)
        obj.set_position(10, 20)
        assert obj.x == 10
        assert obj.y == 20

    def test_set_velocity(self):
        """Test velocity setting."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(5, 10)
        assert obj.vx == 5
        assert obj.vy == 10

    def test_set_velocity_vector(self):
        """Test setting velocity from vector."""
        obj = PhysObject(0, 0, 1)
        v = Vector(3, 4)
        obj.set_velocity_vector(v)
        assert obj.vx == 3
        assert obj.vy == 4

    def test_set_timestep(self):
        """Test timestep setting."""
        obj = PhysObject(0, 0, 1)
        obj.set_timestep(0.05)
        assert obj.dt == 0.05
        assert obj._dt_squared == pytest.approx(0.0025)

    def test_distance(self):
        """Test distance calculation."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(3, 4, 1)
        assert obj1.distance(obj2) == pytest.approx(5.0)

    def test_distance_squared(self):
        """Test squared distance calculation."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(3, 4, 1)
        assert obj1.distance_squared(obj2) == pytest.approx(25.0)

    def test_add_force(self):
        """Test adding forces."""
        obj = PhysObject(0, 0, 1)
        f = Force(10, 0)
        obj.add_force(f)
        assert len(obj.static_forces) == 1
        assert len(obj.dynamic_forces) == 0

    def test_add_dynamic_force(self):
        """Test adding dynamic forces."""
        obj = PhysObject(0, 0, 1)
        f = Force(10, 0, dynamic=True)
        obj.add_force(f, dynamic=True)
        assert len(obj.static_forces) == 0
        assert len(obj.dynamic_forces) == 1

    def test_euler_step_constant_velocity(self):
        """Test Euler integration with constant velocity."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(10, 0)
        obj.set_timestep(0.1)
        obj.euler_step()
        assert obj.x == pytest.approx(1.0)  # 0 + 0.1 * 10

    def test_euler_step_with_acceleration(self):
        """Test Euler integration with acceleration."""
        obj = PhysObject(0, 0, 1)
        obj.set_acceleration(10, 0)
        obj.set_timestep(0.1)
        obj.euler_step()
        assert obj.vx == pytest.approx(1.0)  # 0 + 0.1 * 10

    def test_newton_second_law(self):
        """Test F = ma calculation."""
        obj = PhysObject(0, 0, 2)  # mass = 2
        f = Force(10, 0)
        obj.add_force(f)
        obj.apply_newton_second_law()
        assert obj.ax == pytest.approx(5.0)  # 10 / 2

    def test_rotation(self):
        """Test angular motion."""
        obj = PhysObject(0, 0, 1)
        obj.omega = 10  # Angular velocity
        obj.set_timestep(0.1)
        obj.rotate()
        assert obj.theta == pytest.approx(1.0)  # 0.1 * 10


class TestSystem:
    """Tests for the System class."""

    def test_creation(self):
        """Test system creation."""
        system = System()
        assert len(system.objects) == 0

    def test_add_object(self):
        """Test adding objects."""
        system = System()
        obj = PhysObject(0, 0, 1)
        system.add_object(obj)
        assert len(system.objects) == 1

    def test_remove_object(self):
        """Test removing objects."""
        system = System()
        obj = PhysObject(0, 0, 1)
        system.add_object(obj)
        system.remove_object(obj)
        assert len(system.objects) == 0

    def test_set_timestep(self):
        """Test setting timestep for all objects."""
        system = System()
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(10, 10, 1)
        system.add_object(obj1)
        system.add_object(obj2)
        system.set_timestep(0.05)
        assert obj1.dt == 0.05
        assert obj2.dt == 0.05

    def test_collision_detection(self):
        """Test collision detection."""
        system = System()
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(1, 0, 1)  # Very close
        obj1.size = 1
        obj2.size = 1
        system.add_object(obj1)
        system.add_object(obj2)

        collisions = system.check_collisions()
        assert len(collisions) == 1

    def test_no_collision_far_apart(self):
        """Test no collision when objects are far apart."""
        system = System()
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(100, 0, 1)
        obj1.size = 1
        obj2.size = 1
        system.add_object(obj1)
        system.add_object(obj2)

        collisions = system.check_collisions()
        assert len(collisions) == 0

    def test_iteration(self):
        """Test iterating over system objects."""
        system = System()
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(10, 10, 1)
        system.add_object(obj1)
        system.add_object(obj2)

        objects = list(system)
        assert len(objects) == 2

    def test_len(self):
        """Test system length."""
        system = System()
        system.add_object(PhysObject(0, 0, 1))
        system.add_object(PhysObject(10, 10, 1))
        assert len(system) == 2


class TestCenterOfMass:
    """Tests for center_of_mass function."""

    def test_single_object(self):
        """Test center of mass with one object."""
        obj = PhysObject(10, 20, 5)
        x, y, mass = center_of_mass([obj])
        assert x == 10
        assert y == 20
        assert mass == 5

    def test_two_equal_masses(self):
        """Test center of mass with two equal masses."""
        obj1 = PhysObject(0, 0, 10)
        obj2 = PhysObject(10, 0, 10)
        x, y, mass = center_of_mass([obj1, obj2])
        assert x == pytest.approx(5.0)
        assert y == pytest.approx(0.0)
        assert mass == 20

    def test_unequal_masses(self):
        """Test center of mass with unequal masses."""
        obj1 = PhysObject(0, 0, 10)
        obj2 = PhysObject(10, 0, 30)  # 3x heavier
        x, y, mass = center_of_mass([obj1, obj2])
        # CM should be 3/4 of the way toward obj2
        assert x == pytest.approx(7.5)
        assert mass == 40

    def test_empty_list(self):
        """Test center of mass with empty list."""
        x, y, mass = center_of_mass([])
        assert x == 0
        assert y == 0
        assert mass == 0
