"""
Unit tests for tiny_pysics.forces module.

Tests specialized force classes:
- Friction
- CentralForce
- GravitationalForce
- ElasticForce
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '..')

from tiny_pysics.physics import PhysObject
from tiny_pysics.forces import Friction, CentralForce, GravitationalForce, ElasticForce, G


class TestFriction:
    """Tests for the Friction class."""

    def test_creation(self):
        """Test friction force creation."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(10, 0)
        friction = Friction(obj, k=0.5, power=1)
        assert friction.k == 0.5
        assert friction.power == 1

    def test_opposes_velocity(self):
        """Test that friction opposes velocity direction."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(10, 0)
        friction = Friction(obj, k=1.0, power=1)
        friction.update()
        # Force should be negative (opposing positive velocity)
        assert friction.x < 0

    def test_linear_friction(self):
        """Test linear friction (power=1)."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(10, 0)
        friction = Friction(obj, k=0.5, power=1)
        friction.update()
        assert friction.x == pytest.approx(-5.0)  # -0.5 * 10

    def test_zero_velocity(self):
        """Test friction with zero velocity."""
        obj = PhysObject(0, 0, 1)
        obj.set_velocity(0, 0)
        friction = Friction(obj, k=0.5, power=1)
        friction.update()
        assert friction.x == 0
        assert friction.y == 0


class TestCentralForce:
    """Tests for the CentralForce class."""

    def test_creation(self):
        """Test central force creation."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(10, 0, 1)
        force = CentralForce(obj1, obj2, magnitude=100)
        assert force._magnitude == 100

    def test_direction_toward_target(self):
        """Test that force points toward target object."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(10, 0, 1)  # To the right
        force = CentralForce(obj1, obj2, magnitude=100)
        force.update()
        # Force should point in positive x direction
        assert force.x > 0
        assert abs(force.y) < 1e-10

    def test_set_objects(self):
        """Test changing force objects."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(10, 0, 1)
        obj3 = PhysObject(0, 10, 1)
        force = CentralForce(obj1, obj2, magnitude=100)
        force.set_objects(obj1, obj3)
        force.update()
        # Force should now point in positive y direction
        assert abs(force.x) < 1e-10
        assert force.y > 0


class TestGravitationalForce:
    """Tests for the GravitationalForce class."""

    def test_creation(self):
        """Test gravitational force creation."""
        obj1 = PhysObject(0, 0, 1000)
        obj2 = PhysObject(10, 0, 1000)
        grav = GravitationalForce(obj1, obj2)
        # Should have non-zero magnitude
        assert grav._magnitude > 0

    def test_inverse_square_law(self):
        """Test that force follows inverse square law."""
        obj1 = PhysObject(0, 0, 1000)
        obj2 = PhysObject(10, 0, 1000)
        grav1 = GravitationalForce(obj1, obj2)
        mag1 = grav1._magnitude

        # Double the distance
        obj3 = PhysObject(20, 0, 1000)
        grav2 = GravitationalForce(obj1, obj3)
        mag2 = grav2._magnitude

        # Force should be 1/4 at double distance
        assert mag2 == pytest.approx(mag1 / 4, rel=0.01)

    def test_mass_dependence(self):
        """Test that force scales with mass product."""
        obj1 = PhysObject(0, 0, 1000)
        obj2 = PhysObject(10, 0, 1000)
        grav1 = GravitationalForce(obj1, obj2)
        mag1 = grav1._magnitude

        # Double one mass
        obj3 = PhysObject(0, 0, 2000)
        grav2 = GravitationalForce(obj3, obj2)
        mag2 = grav2._magnitude

        # Force should double
        assert mag2 == pytest.approx(mag1 * 2, rel=0.01)

    def test_update(self):
        """Test that gravitational force updates with position."""
        obj1 = PhysObject(0, 0, 1000)
        obj2 = PhysObject(10, 0, 1000)
        grav = GravitationalForce(obj1, obj2)
        initial_mag = grav._magnitude

        # Move object closer
        obj2.set_position(5, 0)
        grav.update()

        # Force should be stronger (4x at half distance)
        assert grav._magnitude > initial_mag


class TestElasticForce:
    """Tests for the ElasticForce class."""

    def test_creation(self):
        """Test elastic force creation."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(100, 0, 1)
        spring = ElasticForce(obj1, obj2, rest_length=50, k=10)
        assert spring.rest_length == 50
        assert spring.k == 10

    def test_stretched_spring(self):
        """Test spring force when stretched."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(100, 0, 1)  # 100 units apart
        spring = ElasticForce(obj1, obj2, rest_length=50, k=1)
        spring.update()
        # Stretched 50 units, k=1, so magnitude should be 50
        assert spring._magnitude == pytest.approx(50.0)
        # Force should pull obj1 toward obj2 (positive x)
        assert spring.x > 0

    def test_compressed_spring(self):
        """Test spring force when compressed."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(30, 0, 1)  # 30 units apart
        spring = ElasticForce(obj1, obj2, rest_length=50, k=1)
        spring.update()
        # Compressed 20 units, magnitude should be -20
        assert spring._magnitude == pytest.approx(-20.0)
        # Force should push obj1 away from obj2 (negative x)
        assert spring.x < 0

    def test_at_rest_length(self):
        """Test spring at rest length has zero force."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(50, 0, 1)
        spring = ElasticForce(obj1, obj2, rest_length=50, k=10)
        spring.update()
        assert spring._magnitude == pytest.approx(0.0)

    def test_spring_constant(self):
        """Test that force scales with spring constant."""
        obj1 = PhysObject(0, 0, 1)
        obj2 = PhysObject(100, 0, 1)

        spring1 = ElasticForce(obj1, obj2, rest_length=50, k=1)
        spring2 = ElasticForce(obj1, obj2, rest_length=50, k=2)

        spring1.update()
        spring2.update()

        assert spring2._magnitude == pytest.approx(spring1._magnitude * 2)
