const express = require('express');
const route = require('./Routes/station_data')
const app = express();
const cors = require('cors')



app.use(cors({
    origin: 'http://localhost:65414', // Replace with your app's domain
    methods: 'GET,POST', // Allowed methods
    allowedHeaders: ['Content-Type', 'Authorization'] // Allowed headers
  }));
app.use("/",route)



module.exports = app;
