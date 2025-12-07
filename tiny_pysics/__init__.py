"""
TinyPysics - A 2D Physics Simulation Engine

A Python physics simulation library for educational purposes,
demonstrating orbital mechanics, collisions, springs, and more.
"""

__version__ = "2.0.0"
__author__ = "Gaetan Bahl"

from .core import Vector, Force
from .physics import PhysObject, System, center_of_mass
from .forces import (
    Friction,
    CentralForce,
    GravitationalForce,
    ElasticForce,
)
from .game import Universe, Ship
from .utils import deg_to_rad, rad_to_deg, split_sequence

__all__ = [
    "Vector",
    "Force",
    "PhysObject",
    "System",
    "center_of_mass",
    "Friction",
    "CentralForce",
    "GravitationalForce",
    "ElasticForce",
    "Universe",
    "Ship",
    "deg_to_rad",
    "rad_to_deg",
    "split_sequence",
]
