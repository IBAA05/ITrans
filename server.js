const app = require('./app');
const handleUpgrade = require('./websocket')
const { load_data } = require('./modules/load_database');

app.get('/ws', (req, res) => {
    res.send('Ready to upgrade to WebSocket');
});


const server = app.listen(3000, _ => {
    console.log("starting the server ");
})

server.on('upgrade', handleUpgrade);

module.exports = server