const station = require('express').Router() // create a router to get the data .
const { load_data } = require('./../modules/load_database')


station.
    route('/ligne')
    .get(load_data)  

module.exports = station;