#!/usr/bin/env python3
"""
TinyPysics Multiplayer Game Server (Experimental)

WARNING: This server is experimental and not actively maintained.
It is included for educational purposes to demonstrate networked
physics simulations.

This HTTP server provides a simple multiplayer physics game where
clients can create ships, apply thrust, and query positions.

Usage:
    python server.py

The server listens on port 8080 and accepts POST requests with
space-separated commands.

Commands:
    newship x y id     - Create new ship at position with ID
    getall             - Get all object positions
    newclient id       - Register new client
    delclient id       - Remove client and their objects
    boost id           - Apply forward thrust to ship
    noboost id         - Stop thrust
    boostrev id        - Apply reverse thrust
    rotateleft id      - Rotate ship left
    rotateright id     - Rotate ship right
"""

import warnings
warnings.warn(
    "The multiplayer server is experimental and not actively maintained.",
    DeprecationWarning,
    stacklevel=2
)

import math
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

import sys
sys.path.insert(0, '..')

from tiny_pysics import Force
from tiny_pysics.game import Universe, Ship, coordinates_to_string

# Server configuration
PORT = 8080
BOOST_FORCE = 2

# Global state
system = None
client_list = []


class Client:
    """Simple client representation."""

    def __init__(self, client_id: str):
        self.id = client_id


class UpdateThread(threading.Thread):
    """Background thread for physics updates."""

    def __init__(self, game_system: Universe):
        super().__init__(daemon=True)
        self.system = game_system

    def run(self):
        while True:
            time.sleep(0.01)
            self.system.update_euler()


class GameRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for game commands."""

    def do_POST(self):
        """Handle POST requests with game commands."""
        content_length = int(self.headers.get('content-length', 0))
        data_string = self.rfile.read(content_length).decode('utf-8')
        print(f"Received: {data_string}")

        response = process_command(data_string)

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


def process_command(command_string: str) -> str:
    """
    Process a game command and return response.

    Args:
        command_string: Space-separated command string

    Returns:
        Response string
    """
    global system, client_list

    parts = command_string.split()
    if not parts:
        return "error: empty command"

    command = parts[0]

    if command == "newship":
        if len(parts) < 4:
            return "error: newship requires x y id"
        x, y = int(parts[1]), int(parts[2])
        ship_id = parts[3]
        ship = Ship(x, y, 100, ship_id)
        print(f"Created ship: {ship.id}")
        system.add_object(ship)
        return "ok"

    elif command == "getall":
        coords = system.get_all_coordinates()
        return coordinates_to_string(coords)

    elif command == "newclient":
        if len(parts) < 2:
            return "error: newclient requires id"
        client = Client(parts[1])
        client_list.append(client)
        return "client created"

    elif command == "delclient":
        if len(parts) < 2:
            return "error: delclient requires id"
        client_id = parts[1]
        client_list = [c for c in client_list if c.id != client_id]
        # Remove client's ships
        for ship in system.select_by_id(client_id):
            system.remove_object(ship)
        return "client deleted"

    elif command == "boost":
        if len(parts) < 2:
            return "error: boost requires id"
        ship_id = parts[1]
        for ship in system.select_by_id(ship_id):
            boost = Force(
                BOOST_FORCE * math.cos(ship.theta),
                BOOST_FORCE * math.sin(ship.theta)
            )
            boost.id = 'boost'
            ship.add_force(boost)
        return "boost applied"

    elif command == "noboost":
        if len(parts) < 2:
            return "error: noboost requires id"
        ship_id = parts[1]
        for ship in system.select_by_id(ship_id):
            ship.static_forces = [f for f in ship.static_forces if f.id != 'boost']
        return "boost removed"

    elif command == "boostrev":
        if len(parts) < 2:
            return "error: boostrev requires id"
        ship_id = parts[1]
        for ship in system.select_by_id(ship_id):
            boost = Force(
                -BOOST_FORCE * math.cos(ship.theta),
                -BOOST_FORCE * math.sin(ship.theta)
            )
            boost.id = 'boost'
            ship.add_force(boost)
        return "reverse boost applied"

    elif command == "rotateleft":
        if len(parts) < 2:
            return "error: rotateleft requires id"
        ship_id = parts[1]
        for ship in system.select_by_id(ship_id):
            ship.omega -= 1
        return "rotating left"

    elif command == "rotateright":
        if len(parts) < 2:
            return "error: rotateright requires id"
        ship_id = parts[1]
        for ship in system.select_by_id(ship_id):
            ship.omega += 1
        return "rotating right"

    else:
        return f"error: unknown command '{command}'"


def start_server():
    """Start the HTTP server."""
    server_address = ("", PORT)
    server = HTTPServer(server_address, GameRequestHandler)
    print(f"Server starting on port {PORT}...")
    server.serve_forever()


if __name__ == "__main__":
    # Initialize game world
    system = Universe(100, 100)

    # Create test ships
    ship_a = Ship(20, 20, 20, "a")
    ship_b = Ship(100, 100, 20, "b")
    system.add_object(ship_a)
    system.add_object(ship_b)

    ship_a.omega = 1
    ship_a.vx = 0
    ship_b.vy = 0.1

    # Set up gravity
    system.setup_gravity()

    # Start physics update thread
    update_thread = UpdateThread(system)
    update_thread.start()

    # Start HTTP server
    start_server()
