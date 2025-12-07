"""
Utility functions for physics simulations.

This module provides helper functions for angle conversions,
sequence operations, and other common utilities.
"""

from __future__ import annotations
import numpy as np
from typing import TypeVar, Sequence

T = TypeVar('T')


def deg_to_rad(degrees: float) -> float:
    """
    Convert degrees to radians.

    Args:
        degrees: Angle in degrees

    Returns:
        Angle in radians

    Example:
        >>> deg_to_rad(180)
        3.141592653589793
    """
    return float(np.radians(degrees))


def rad_to_deg(radians: float) -> float:
    """
    Convert radians to degrees.

    Args:
        radians: Angle in radians

    Returns:
        Angle in degrees

    Example:
        >>> rad_to_deg(np.pi)
        180.0
    """
    return float(np.degrees(radians))


def toggle(value: bool) -> bool:
    """
    Toggle a boolean value.

    Args:
        value: Boolean to toggle

    Returns:
        Negated boolean

    Example:
        >>> toggle(True)
        False
    """
    return not value


def split_sequence(seq: Sequence[T], chunks: int) -> list[list[T]]:
    """
    Split a sequence into roughly equal chunks.

    Args:
        seq: Sequence to split
        chunks: Number of chunks to create

    Returns:
        List of lists, each containing a portion of the sequence

    Example:
        >>> split_sequence([1, 2, 3, 4, 5], 2)
        [[1, 2, 3], [4, 5]]
    """
    if chunks <= 0:
        raise ValueError("chunks must be positive")

    seq_list = list(seq)
    n = len(seq_list)

    if chunks >= n:
        return [[item] for item in seq_list]

    result = []
    chunk_size = n / chunks

    for i in range(chunks):
        start = int(round(i * chunk_size))
        end = int(round((i + 1) * chunk_size))
        result.append(seq_list[start:end])

    return result


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value to a range.

    Args:
        value: Value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Value clamped to [min_val, max_val]

    Example:
        >>> clamp(15, 0, 10)
        10
    """
    return max(min_val, min(value, max_val))


def lerp(a: float, b: float, t: float) -> float:
    """
    Linear interpolation between two values.

    Args:
        a: Start value
        b: End value
        t: Interpolation factor (0 = a, 1 = b)

    Returns:
        Interpolated value

    Example:
        >>> lerp(0, 100, 0.5)
        50.0
    """
    return a + (b - a) * t


def normalize_angle(angle: float) -> float:
    """
    Normalize an angle to the range [-pi, pi].

    Args:
        angle: Angle in radians

    Returns:
        Equivalent angle in [-pi, pi]

    Example:
        >>> normalize_angle(3 * np.pi)  # 540 degrees
        -3.141592653589793
    """
    while angle > np.pi:
        angle -= 2 * np.pi
    while angle < -np.pi:
        angle += 2 * np.pi
    return angle
