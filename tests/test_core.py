"""
Unit tests for tiny_pysics.core module.

Tests Vector and Force classes including:
- Creation and property access
- Arithmetic operators
- Vector operations (magnitude, normalize, dot, cross)
- Force-specific functionality
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '..')

from tiny_pysics.core import Vector, Force


class TestVector:
    """Tests for the Vector class."""

    def test_creation(self):
        """Test vector creation with coordinates."""
        v = Vector(3, 4)
        assert v.x == 3
        assert v.y == 4

    def test_default_creation(self):
        """Test vector creation with default values."""
        v = Vector()
        assert v.x == 0
        assert v.y == 0

    def test_from_array(self):
        """Test vector creation from numpy array."""
        arr = np.array([5, 6])
        v = Vector.from_array(arr)
        assert v.x == 5
        assert v.y == 6

    def test_from_polar(self):
        """Test vector creation from polar coordinates."""
        v = Vector.from_polar(5, 0)  # Along x-axis
        assert abs(v.x - 5) < 1e-10
        assert abs(v.y) < 1e-10

        v2 = Vector.from_polar(1, np.pi / 2)  # Along y-axis
        assert abs(v2.x) < 1e-10
        assert abs(v2.y - 1) < 1e-10

    def test_magnitude(self):
        """Test magnitude calculation (3-4-5 triangle)."""
        v = Vector(3, 4)
        assert v.magnitude() == pytest.approx(5.0)

    def test_magnitude_squared(self):
        """Test squared magnitude calculation."""
        v = Vector(3, 4)
        assert v.magnitude_squared() == pytest.approx(25.0)

    def test_normalized(self):
        """Test vector normalization."""
        v = Vector(3, 4)
        n = v.normalized()
        assert n.magnitude() == pytest.approx(1.0)
        assert n.x == pytest.approx(0.6)
        assert n.y == pytest.approx(0.8)

    def test_normalized_zero(self):
        """Test normalization of zero vector."""
        v = Vector(0, 0)
        n = v.normalized()
        assert n.x == 0
        assert n.y == 0

    def test_dot_product(self):
        """Test dot product calculation."""
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        assert v1.dot(v2) == pytest.approx(11.0)  # 1*3 + 2*4

    def test_dot_product_perpendicular(self):
        """Test that perpendicular vectors have zero dot product."""
        v1 = Vector(1, 0)
        v2 = Vector(0, 1)
        assert v1.dot(v2) == pytest.approx(0.0)

    def test_cross_product(self):
        """Test 2D cross product."""
        v1 = Vector(1, 0)
        v2 = Vector(0, 1)
        assert v1.cross(v2) == pytest.approx(1.0)  # Right-hand rule

    def test_addition(self):
        """Test vector addition."""
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        result = v1 + v2
        assert result.x == 4
        assert result.y == 6

    def test_subtraction(self):
        """Test vector subtraction."""
        v1 = Vector(3, 4)
        v2 = Vector(1, 2)
        result = v1 - v2
        assert result.x == 2
        assert result.y == 2

    def test_scalar_multiplication(self):
        """Test scalar multiplication."""
        v = Vector(2, 3)
        result = v * 2
        assert result.x == 4
        assert result.y == 6

    def test_scalar_rmul(self):
        """Test reverse scalar multiplication."""
        v = Vector(2, 3)
        result = 2 * v
        assert result.x == 4
        assert result.y == 6

    def test_division(self):
        """Test scalar division."""
        v = Vector(4, 6)
        result = v / 2
        assert result.x == 2
        assert result.y == 3

    def test_negation(self):
        """Test vector negation."""
        v = Vector(3, -4)
        result = -v
        assert result.x == -3
        assert result.y == 4

    def test_equality(self):
        """Test vector equality."""
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        v3 = Vector(1, 3)
        assert v1 == v2
        assert v1 != v3

    def test_copy(self):
        """Test vector copying."""
        v1 = Vector(3, 4)
        v2 = v1.copy()
        v2.x = 10
        assert v1.x == 3  # Original unchanged

    def test_set(self):
        """Test setting both coordinates."""
        v = Vector(1, 2)
        v.set(5, 6)
        assert v.x == 5
        assert v.y == 6

    def test_angle(self):
        """Test angle calculation."""
        v = Vector(1, 0)
        assert v.angle() == pytest.approx(0.0)

        v2 = Vector(0, 1)
        assert v2.angle() == pytest.approx(np.pi / 2)

    def test_rotate(self):
        """Test vector rotation."""
        v = Vector(1, 0)
        rotated = v.rotate(np.pi / 2)  # 90 degrees
        assert abs(rotated.x) < 1e-10
        assert rotated.y == pytest.approx(1.0)

    def test_distance_to(self):
        """Test distance calculation."""
        v1 = Vector(0, 0)
        v2 = Vector(3, 4)
        assert v1.distance_to(v2) == pytest.approx(5.0)


class TestForce:
    """Tests for the Force class."""

    def test_creation(self):
        """Test force creation."""
        f = Force(10, 20)
        assert f.x == 10
        assert f.y == 20

    def test_lever_arm(self):
        """Test lever arm attribute."""
        f = Force(10, 0, lever_arm=5.0)
        assert f.lever_arm == 5.0

    def test_dynamic_flag(self):
        """Test dynamic force flag."""
        f1 = Force(10, 0, dynamic=False)
        f2 = Force(10, 0, dynamic=True)
        assert not f1.dynamic
        assert f2.dynamic

    def test_reset(self):
        """Test force reset."""
        f = Force(10, 20)
        f.reset()
        assert f.x == 0
        assert f.y == 0

    def test_direction_between(self):
        """Test direction calculation between points."""
        f = Force(0, 0)
        f._magnitude = 10
        f.direction_between((0, 0), (3, 4))  # Unit vector * 10
        assert f.x == pytest.approx(6.0)  # 10 * 3/5
        assert f.y == pytest.approx(8.0)  # 10 * 4/5

    def test_torque(self):
        """Test torque calculation."""
        f = Force(10, 0, lever_arm=2.0)
        f._magnitude = 10
        assert f.torque() == pytest.approx(20.0)

    def test_copy(self):
        """Test force copying."""
        f1 = Force(10, 20, lever_arm=5.0, dynamic=True)
        f1.id = "test"
        f2 = f1.copy()
        assert f2.x == 10
        assert f2.y == 20
        assert f2.lever_arm == 5.0
        assert f2.dynamic
        assert f2.id == "test"

    def test_inherits_vector(self):
        """Test that Force inherits Vector operations."""
        f1 = Force(1, 2)
        f2 = Force(3, 4)
        result = f1 + f2  # Should work via Vector
        assert result.x == 4
        assert result.y == 6
