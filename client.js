const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8080/ws');

ws.on('open', () => {
    console.log('Connected to server');

    // Send a test message
    const message = JSON.stringify({ latitude: 40.7128, longitude: -74.0060 }); // Example coordinates
    ws.send(message);
});

ws.on('message', (data) => {
    console.log('Received from server:', data.toString());
});

ws.on('close', () => {
    console.log('Disconnected from server');
});

ws.on('error', (error) => {
    console.error('WebSocket error:', error);
});
// """
// SELECT * FROM direction1

// where nameEN = ? 
//     LIMIT 1 
// OFFSET 1
// """