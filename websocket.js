const WebSocket = require('ws');
const db = require('./modules/load_database'); // Adjust the path as needed
const server = require('./server'); // Ensure this points to the correct path

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (socket) => {

  console.log('Client connected');

  // Send latitude and longitude to the client upon connection
  const initialLatitude = 23.0;
  const initialLongitude = 11.0;
  const initialData = JSON.stringify({ latitude: initialLatitude, longitude: initialLongitude });
  
  console.log(typeof initialData);
  socket.send(initialData, err => {

    if (err) {
      console.log("cannot send the data to the client");
    } else { 
      console.log(`Sent: latitude = ${initialLatitude}, longitude = ${initialLongitude}`);  
    }

  });

  socket.on('message', (data) => {
     console.log('Received from client:', data.toString());

    try {
      // const { latitude, longitude } = JSON.parse(data);
      // console.log(`Received: latitude = ${latitude}, longitude = ${longitude}`);
  
      // const station = db.findStation(latitude, longitude); // Uncomment and implement this line as needed
      const station = ""; // Placeholder for the station logic

      if (station) {

        console.log('Station detected');
        socket.send(JSON.stringify({ status: 'success', message: 'Station detected', station }));
       }else{
        console.log('Station not found');
        socket.send(JSON.stringify({ status: 'error', message: 'Station not found' }));
     
      }
      
    } catch (error) {
      console.error('Error processing message:', error);
      socket.send(JSON.stringify({ status: 'error', message: 'Invalid data format' }));
    }
  });

  socket.on('close', () => {
    console.log('Client disconnected');
  });
});

module.exports = function handleUpgrade(request, socket, head) {
  const pathname = new URL(request.url, `http://${request.headers.host}`).pathname;

  if (pathname === '/ws') {
    console.log('Upgrading to WebSocket');
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
};
