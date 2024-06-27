const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const config = require('./../gps/config.json');
const axios = require('axios');


const connect = async function() {
    return new Promise((resolve, reject) => {
        let db = new sqlite3.Database('./stations.db', (err) => {
            if (err) {
                console.error(`Error opening the database: ${err.message}`);
                reject(err);
            } else {
                console.log("Connected to the database");
                resolve(db);
            }
        });
    });
};

exports.runQuery = async (db, query, params) => {
    return new Promise((resolve, reject) => {
        db.run(query, params, function (err) {
            if (err) {
                return reject(err);
            }
            resolve(this);
        });
    });
};



const fillTables = async (db, data) => {


    for (let element of data.lineStations) {

        const going = element.station.goingGeopoint;
        const retour = element.station.returningGeopoint;
        if (element.direction == 'GOING') {
            const goingData = [element.station.id,element.station.nameAR, element.station.nameEN, element.station.nameFR,going.lng, going.lat,data.lineType,element.order];
            await exports.runQuery(db, 'INSERT INTO going (id,nameAR, nameEN, nameFR, long, lat,line,ord) VALUES (?,?, ?, ?, ?, ?,?,?)', goingData);
        } else {
            const returningData = [element.station.id,element.station.nameAR, element.station.nameEN, element.station.nameFR, retour.lat, retour.lat,data.lineType,element.order];
            await exports.runQuery(db, 'INSERT INTO back (id,nameAR, nameEN, nameFR, long, lat,line,ord) VALUES (?,?, ?, ?, ?, ?,?,?)', returningData);
        }
    }
};

const selectAllData = async (db, table_name) => {
    return new Promise((resolve, reject) => {
        db.all('SELECT * FROM ' + table_name, (err, rows) => {
            if (err) {
                console.error('Error selecting data:', err.message);
                reject(err); // Reject the promise on error
            } else {
                resolve(rows); // Resolve the promise with rows on success
            }
        });
    });
};
   


const fillInterstations = async (db) => {
    const data = await selectAllData(db, "going");

    for (let i = 0; i < data.length - 1; i++) {
        const currentStation = data[i];
        const nextStation = data[i + 1];
    
        console.log(currentStation.id, nextStation.id);
        const interstations = await load_interstations(currentStation.id, nextStation.id);
            
        
        const stmt = db.prepare(`INSERT INTO interstation1 (id, lat, long, from_station, to_station) VALUES (?, ?, ?, ?, ?)`);

        // Insert each data object into the table
        data.forEach((item) => {
            stmt.run(item.id, item.lat, item.lng, item.from_station, item.to_station, (err) => {
                if (err) {
                    console.error('Error inserting row:', err.message);
                } else {
                    console.log(`Row inserted with ID: ${item.id}`);
                }
            });
        }); 
    }
};


const load_interstations = async (from, to) => {
  
    const apiUrl = config.hOST_IP_ADRESS + ":" + config.SERVER_PORT + "/infra/interstation" ;

    const params = {
        "from": from,
        "to":to
    };

    axios.get(apiUrl, { params })
        .then(response => { 
            console.log(response.data);
            return response.data; 
        })
        .catch(error => {
            console.error('Error making GET request:', error);
        });
}


const load_stations = async () => {

    const apiUrl = config.hOST_IP_ADRESS + ":" + config.SERVER_PORT + "/infra/line/2";

    try {

        const response = await new Promise((resolve, reject) => {
            http.get(apiUrl, (response) => {
                let data = '';
                response.on('data', (chunk) => {
                    data += chunk;
                });

                response.on('end', () => {
                    try {
                        resolve(JSON.parse(data));
                    } catch (error) {
                        reject(error);
                    }
                });

                response.on('error', (error) => {
                    reject(error);
                });
            });
        });


        const db = await connect();
        await exports.runQuery(db, 'DROP TABLE IF EXISTS going');
        await exports.runQuery(db, `
            CREATE TABLE going (
                id INTEGER PRIMARY KEY ,
                nameAR TEXT NOT NULL,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lat DECIMAL NOT NULL,
                long DECIMAL NOT NULL,
                line INT NOT NULL ,
                ord INT NOT NULL
            )
        `);
        await exports.runQuery(db, 'DROP TABLE IF EXISTS back');
        await exports.runQuery(db, `
            CREATE TABLE back (
                id INTEGER PRIMARY KEY ,
                nameAR TEXT NOT NULL,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lat DECIMAL NOT NULL,
                long DECIMAL NOT NULL ,
                line INT NOT NULL ,
                ord INT NOT NULL
            )
        `);

        await exports.runQuery(db, "Drop TABLE IF EXISTS interstation1");
        await exports.runQuery(db, `
            CREATE TABLE interstation1(
               id INTEGER PRIMARY KEY ,
               lat DECIMAL NOT NULL ,
               long DECIMAL NOT NULL ,
               from_station INT NOT NULL ,
               to_station INT NOT NULL 
            )
        `);
        await exports.runQuery(db, "Drop TABLE IF EXISTS interstation2");
        await exports.runQuery(db, `
            CREATE TABLE interstation2(
               id INTEGER PRIMARY KEY ,
               lat DECIMAL NOT NULL ,
               long DECIMAL NOT NULL , 
               from_station INT NOT NULL ,
               to_station INT NOT NULL  
            )

        `);

        await fillTables(db, response);
        await fillInterstations(db);
        
        db.close((err) => {
            if (err) {
                console.error(`Error closing the database: ${err.message}`);
            } else {
                console.log("Closed the database connection");
            }
        }); 

    } catch (error) {
        console.error(`Error when loading data: ${error.message}`);
    }

};
load_stations();

//load_interstations();
// (async () => {
//     const db = await connect();
//     select_all_data(db, "going");
// })();



module.exports = connect; 