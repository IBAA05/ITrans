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
    let nb = 1;


    for (let element of data.lineStations) {
        const going = element.station.goingGeopoint;
        const returning = element.station.returningGeopoint;

        if (nb <= 13) {
            const goingData = [ element.station.nameAR, element.station.nameEN, element.station.nameFR, going.lng, going.lat,data.lineType];
            await exports.runQuery(db, 'INSERT INTO direction1 (nameAR, nameEN, nameFR, lang, lat,line) VALUES ( ?, ?, ?, ?, ?,?)', goingData);
        

        } else {
            const returningData = [ element.station.nameAR, element.station.nameEN, element.station.nameFR, returning.lng, returning.lat,data.lineType];
            await exports.runQuery(db, 'INSERT INTO direction2 (nameAR, nameEN, nameFR, lang, lat,line) VALUES (?, ?, ?, ?, ?,?)', returningData);
        }
        nb += 1;
    }

   




};

exports.load_data = async (req, res, next) => {
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

        // const jsonData = response;
        // res.status(200).json({
        //     message: "successful",
        //     data: jsonData
        // });

        const db = await exports.connect();
        await exports.runQuery(db, 'DROP TABLE IF EXISTS direction1');
        await exports.runQuery(db, `
            CREATE TABLE direction1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nameAR TEXT,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lat DECIMAL NOT NULL,
                long DECIMAL NOT NULL,
                line INT NOT NULL 
            )
        `);

        await exports.runQuery(db, 'DROP TABLE IF EXISTS direction2');
        await exports.runQuery(db, `
            CREATE TABLE direction2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nameAR TEXT,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lat DECIMAL NOT NULL,
                lang DECIMAL NOT NULL ,
                line INT NOT NULL 
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

        await fillTables(db, jsonData);

        db.close((err) => {
            if (err) {
                console.error(`Error closing the database: ${err.message}`);
            } else {
                console.log("Closed the database connection");
            }
        }); 

    } catch (error) {
        console.error(`Error when loading data: ${error}`);
        res.status(500).json({ error: 'Internal Server Error' });
    }

    next();
};
