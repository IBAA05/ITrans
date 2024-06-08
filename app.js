const express = require('express');
const route = require('./Routes/station_data')
const app = express();


app.use("/",route)



module.exports = app;
