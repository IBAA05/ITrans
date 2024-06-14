const {selectQuery,connect} = require('./load_database')

exports.getGoingStations = async (req, res, next) => {

    try {

        const db = await connect();
        const results = await selectQuery(db, "SELECT * FROM direction1");
        
        res.status(200).json({
            status: "success",
            data: results
        });
        db.close((err) => { 
            if (err) {
                console.error(`Error closing the database: ${err.message}`);
            } else {
                console.log("Closed the database connection");
            }
        }); 

    } catch (err) {
        res.status(404).send({
            message : "Table doesnt exist"
        })
    }
}


exports.getReturningStations = async (req, res, next) => {

    try {

        const db = await connect();
        const results = await selectQuery(db, "SELECT * FROM direction2");
        
        res.status(200).json({
            status: "success",
            data: results
        })

    db.close((err) => {
        if (err) {
            console.error(`Error closing the database: ${err.message}`);
        } else {
            console.log("Closed the database connection");
        }
    });

    } catch (err) {
        res.status(404).send({
            message: "Tables doesnt exist"
        })
    } 
} 