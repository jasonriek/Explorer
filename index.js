const express = require('express');
const http = require('http');
const { spawn } = require('child_process');
const WebSocket = require('ws');
const axios = require('axios');
const path = require('path');

const app = express();
const server = http.createServer(app);

// Set up WebSocket server
const wss = new WebSocket.Server({ 
    server,
    maxPayload: 1048576  // Increase the maximum payload size to handle large frames (1 MB)
});

// Set EJS as the view engine
app.set('view engine', 'ejs');

// Serve static files (for HTML, CSS, JS)
app.use(express.static('public'));

// Home route
app.get('/', (req, res) => {
    res.render('index'); // Render index.ejs from the views folder
});

// API to control motors using GET
app.get('/motor/:direction', async (req, res) => {
    const direction = req.params.direction;

    try {
        // Send POST request to Flask server with the direction
        const response = await axios.post('http://localhost:5000/motor', { direction });
        res.send(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error controlling motor');
    }
});

// Endpoint to control the LED (for the headlight and tactical red light)
app.post('/control-led/:light/:action', (req, res) => {
    const light = req.params.light;
    const action = req.params.action.toLowerCase();

    let pin;

    // Map light names to GPIO pins
    if (light === 'headlight') {
        pin = 6;
    } else if (light === 'redlight') {
        pin = 26;
    } else {
        return res.status(400).send('Invalid light');
    }

    // Validate the action (either "on" or "off")
    if (action !== 'on' && action !== 'off') {
        return res.status(400).send('Invalid action');
    }

    // Path to the Python script in the 'drivers' directory
    const pythonScript = path.join(__dirname, 'drivers', 'lights.py');

    // Run the Python script to control the LED
    const pythonProcess = spawn('python3', [pythonScript, pin, action]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.send(`LED ${light} turned ${action}`);
        } else {
            res.status(500).send('Error controlling LED');
        }
    });
});

// Start libcamera-vid to stream MJPEG over WebSocket
const cameraProcess = spawn('libcamera-vid', [
    '--inline',
    '-t', '0',
    '--width', '640',
    '--height', '480',
    '--framerate', '30',
    '--codec', 'mjpeg',
    '--flush',            // Force flushing after every frame
    '--vflip',
    '--hflip',
    '-o', '-'
]);


// Handle WebSocket connections
wss.on('connection', (ws) => {
    console.log('New WebSocket connection');

    // Pipe video data to WebSocket clients
    cameraProcess.stdout.on('data', (data) => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(data, { binary: true });
        }
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed');
    });
});

// Handle libcamera-vid errors
cameraProcess.stderr.on('data', (data) => {
    console.error(`libcamera-vid stderr: ${data}`);
});

cameraProcess.on('close', (code) => {
    console.log(`libcamera-vid process exited with code ${code}`);
});

// Start the server
server.listen(3000, () => {
    console.log('Server is running on port 3000');
});