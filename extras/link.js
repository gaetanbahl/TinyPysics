/**
 * TinyPysics Server Communication
 *
 * Simple utilities for communicating with the TinyPysics server.
 */

let serverResponse = "";

/**
 * Send a command to the server.
 * @param {string} command - The command to send
 * @param {function} callback - Callback function receiving the response
 */
function sendCommand(command, callback) {
    fetch('/', {
        method: 'POST',
        body: command,
        headers: {
            'Content-Type': 'text/plain'
        }
    })
    .then(response => response.text())
    .then(data => {
        if (callback) {
            callback(data);
        }
    })
    .catch(error => {
        console.error('Server error:', error);
        if (callback) {
            callback(null, error);
        }
    });
}

/**
 * Get all object positions from the server.
 */
function getAllPositions() {
    sendCommand('getall', function(data) {
        serverResponse = data || "";
    });
}

/**
 * Create a new ship on the server.
 * @param {number} x - X position
 * @param {number} y - Y position
 * @param {string} id - Ship identifier
 */
function createShip(x, y, id) {
    sendCommand(`newship ${x} ${y} ${id}`);
}

/**
 * Apply thrust to a ship.
 * @param {string} id - Ship identifier
 */
function applyBoost(id) {
    sendCommand(`boost ${id}`);
}

/**
 * Stop thrust on a ship.
 * @param {string} id - Ship identifier
 */
function stopBoost(id) {
    sendCommand(`noboost ${id}`);
}

/**
 * Rotate a ship left.
 * @param {string} id - Ship identifier
 */
function rotateLeft(id) {
    sendCommand(`rotateleft ${id}`);
}

/**
 * Rotate a ship right.
 * @param {string} id - Ship identifier
 */
function rotateRight(id) {
    sendCommand(`rotateright ${id}`);
}
