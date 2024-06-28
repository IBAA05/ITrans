const axios = require('axios');
const ConfigDao = require('./../daos/configDao.js');


let msServerPort;
let msServerIp;
let msServerProtocol;
let url; 


async function initializeConfig() {

    const configDao = new ConfigDao();
    msServerPort = await configDao.getValueByKey('msServerPort');
    msServerIp = await configDao.getValueByKey('msServerIp');
    msServerProtocol = await configDao.getValueByKey('msServerProtocol');
}

 



const getStations = async () => {
    
    await initializeConfig();
    const LINE_NUMBER = 2; 
    const url = msServerProtocol + '://' + msServerIp + ":" + msServerPort;
   
    const stationUrl = url + '/infra/line/' + LINE_NUMBER;
    console.log(stationUrl);

    try {

        const response = await axios.get(stationUrl);
        console.log('Data fetched successfully:', response.data);

    } catch (error) {

        console.error('Error fetching data:', error.message);
    }
}


const getInterStations = async () => {

    const LINE_NUMBER = 2; 
  
    const interstationUrl = url +   '/infra/interstation/line/' + LINE_NUMBER ;

    try {

        const response = await axios.get(interstationUrl);
        console.log('Data fetched successfully:', response.data);

    } catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

getStations();
getInterStations();

module.exports = { getStations, getInterStations };