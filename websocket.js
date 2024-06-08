const WebSocket = require('ws');
const db = require('./modules/load_database'); // Adjust the path as needed
const server = require('./server')

const wss = new WebSocket.Server({ noServer : true});



wss.on('connection', (socket) => {
    console.log('Client connected');

  socket.on('message', (data) => {

      try {
        console.log('def')
        const { latitude, longitude } = JSON.parse(data);
        console.log("latitude = " + latitude , "longitude=" + longitude ) ;
    //   const station = db.findStation(latitude, longitude);
        const station = "" 
        
      if (station) {
        console.log("Station is detected");
        socket.send(JSON.stringify({ status: 'success', message: 'Station detected', station }));
      
      } else {
        console.log("Station is not found");
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
    console.log('de')
    const pathname = new URL(request.url, `http://${request.headers.host}`).pathname;

    if (pathname === '/ws') {
        console.log('Upgrading to WebSocket');
        wss.handleUpgrade(request, socket, head, (ws) => {
            wss.emit('connection', ws, request);
        });
    } else {
        socket.destroy();
    }
}



