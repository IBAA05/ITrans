const station = require('express').Router() // create a router to get the data .
const { load_data } = require('./../modules/load_database')
const {getGoingStations,getReturningStations} = require("./../modules/station_data")

station.
    route('/line')
    .get(load_data)  

station.
    route('/going')
    .get(getGoingStations)

station.
    route('/returning')
    .get(getReturningStations)

module.exports = station;