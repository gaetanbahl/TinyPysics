/**
 * TinyPysics Game Client
 *
 * Canvas-based game client for the TinyPysics multiplayer server.
 * Renders ships as triangular shapes with rotation.
 */

// Drawing function for ship shapes
function drawShape(context, x, y, size, rotation) {
    x = Math.round(x);
    y = Math.round(y);

    context.save();
    context.translate(x, y);
    context.scale(size, size);
    context.rotate(rotation);
    context.beginPath();
    context.lineWidth = 0.3;
    context.lineJoin = "miter";
    context.moveTo(-1, -1);
    context.lineTo(+1, 0);
    context.lineTo(-1, +1);
    context.lineTo(-0.5, 0);
    context.lineTo(-1, -1);
    context.closePath();
    context.strokeStyle = '#0F0';
    context.stroke();
    context.restore();
}

// Configuration
const FPS = 30;
const FRAME_TIME = 1000 / FPS;

let canvas;
let context;
let width;
let height;
let serverData = "";

// Initialize on page load
window.onload = function() {
    canvas = document.getElementById('canvas');
    if (!canvas) {
        alert("Could not load canvas element");
        return;
    }

    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    context = canvas.getContext('2d');
    if (!context) {
        alert("Could not get 2D context");
        return;
    }

    // Start game loop
    setInterval(gameLoop, FRAME_TIME);
};

// Main game loop
function gameLoop() {
    // Request data from server
    fetchPositions();

    // Clear canvas
    context.fillStyle = "black";
    context.fillRect(0, 0, width, height);

    // Draw objects if we have data
    if (serverData !== "") {
        const lines = serverData.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const parts = lines[i].split(' ');
            if (parts.length >= 3) {
                const x = parseFloat(parts[0]);
                const y = parseFloat(parts[1]);
                const rot = parseFloat(parts[2]);
                drawShape(context, x + width / 2, y + height / 2, 20, rot);
            }
        }
    }
}

// Fetch positions from server
function fetchPositions() {
    fetch('/', {
        method: 'POST',
        body: 'getall'
    })
    .then(response => response.text())
    .then(data => {
        serverData = data;
    })
    .catch(error => {
        console.error('Error fetching positions:', error);
    });
}
