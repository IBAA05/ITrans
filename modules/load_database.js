const http = require('http');
const sqlite3 = require('sqlite3').verbose();

exports.load_data = async (req, res, next) => {
    const apiUrl = "http://41.111.178.14:8080/infra/line/2"; // Replace with actual API URL

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

    const jsonData = response;
    res.status(200).json({
        message: "successful",
        data: jsonData
    });

    // Open the database for reading and writing. Create it if it doesn't exist.
    let db = new sqlite3.Database('./stations.db', (err) => {
        if (err) {
            console.error(`Error opening the database: ${err.message}`);
        } else {
            console.log("Connected to the database");
        }
    });

    const runQuery = async (query, params = []) => {
        return new Promise((resolve, reject) => {
            db.run(query, params, function (err) {
                if (err) {
                    return reject(err);
                }
                resolve(this);
            });
        });
    };

    try {
        await runQuery(`DROP TABLE IF EXISTS direction1`);
        await runQuery(`
            CREATE TABLE direction1 (
                nameAR TEXT,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lang DECIMAL NOT NULL,
                lat DECIMAL NOT NULL
            )
        `);

        await runQuery(`DROP TABLE IF EXISTS direction2`);
        await runQuery(`
            CREATE TABLE direction2 (
                nameAR TEXT,
                nameEN TEXT NOT NULL,
                nameFR TEXT NOT NULL,
                lang DECIMAL NOT NULL,
                lat DECIMAL NOT NULL
            )
        `);

        await fillTables(db, jsonData);

    } catch (error) {
        console.error(`Error creating tables: ${error.message}`);
    }

    next();

};

const fillTables = async (db, data) => {
    const runQuery = async (query, params = []) => {
        return new Promise((resolve, reject) => {
            db.run(query, params, function (err) {
                if (err) {
                    return reject(err);
                }
                resolve(this);
            });
        });
    };

    let nb = 1; 

    for (const element of data.lineStations) {
        const going = element.station.goingGeopoint;
        const returning = element.station.returningGeopoint;

        if ( nb <= 13) {
            const goingData = [element.station.nameAR, element.station.nameEN, element.station.nameFR, going.lng, going.lat];
            await runQuery('INSERT INTO direction1 (nameAR, nameEN, nameFR, lang, lat) VALUES ( ?, ?, ?, ?, ?)', goingData);
        }
        if (  nb > 13) {
            const returningData = [ element.station.nameAR, element.station.nameEN, element.station.nameFR, returning.lng, returning.lat];
            await runQuery('INSERT INTO direction2 (nameAR, nameEN, nameFR, lang, lat) VALUES (?, ?, ?, ?, ?)', returningData);
        }
        nb +=1 
    }
};
