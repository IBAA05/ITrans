const http = require('http');
const sqlite3 = require('sqlite3').verbose();


exports.connect = async function() {
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

        if (element.direction ==  'GOING') {
            const goingData = [ element.station.nameAR, element.station.nameEN, element.station.nameFR, going.lng, going.lat,data.lineType,element.order];
            await exports.runQuery(db, 'INSERT INTO going (nameAR, nameEN, nameFR, long, lat,line,ord) VALUES ( ?, ?, ?, ?, ?,?,?)', goingData);
        } else {
            const returningData = [ element.station.nameAR, element.station.nameEN, element.station.nameFR, retour.lng, retour.lat,data.lineType,element.order];
            await exports.runQuery(db, 'INSERT INTO back (nameAR, nameEN, nameFR, long, lat,line,ord) VALUES (?, ?, ?, ?, ?,?,?)', returningData);
        }
    }
};

const load_data = async () => {

    const apiUrl = "http://41.111.178.14:8080/infra/line/2"; // Replace with actual API URL

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


        const db = await exports.connect();
        await exports.runQuery(db, 'DROP TABLE IF EXISTS going');
        await exports.runQuery(db, `
            CREATE TABLE going (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               lat DECIMAL NOT NULL ,
               lang DECIMAL NOT NULL ,
               sta_id INT NOT NULL 
            )

        `);
        await exports.runQuery(db, "Drop TABLE IF EXISTS interstation2");
        await exports.runQuery(db, `
            CREATE TABLE interstation2(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               lat DECIMAL NOT NULL ,
               lang DECIMAL NOT NULL , 
               sta_id INT NOT NULL 
            )

        `);

        await fillTables(db, response);

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
load_data();


