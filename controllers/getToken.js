require('dotenv').config({ path: './token.env' });
const fs = require('fs') 

async function getToken(url, data) {

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error(error); // Handle errors
    }
}

const apiUrl = 'http://127.0.0.1:4000/login';

const mydata = {
    username: process.env.USER_NAME,
    password: process.env.PASSWORD
};


(async () => {
    const data = await getToken(apiUrl, mydata);
    console.log(data); // Handle successful response
    // process.env.AUTH_TOKEN = data['token'] 
})(); 
