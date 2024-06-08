const app = require('./app');
const handleUpgrade = require('./websocket')

app.get('/ws', (req, res) => {
    res.send('Ready to upgrade to WebSocket');
});

const server = app.listen(8080, _ => {
    console.log("starting the server ");
})

server.on('upgrade', handleUpgrade);

module.exports = server