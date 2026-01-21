import db from "./index.js";


async function initDB(){
    try{
        await db.query(`CREATE DATABASE IF NOT EXISTS telebot`);
        console.log("Database checked/created");
         
    }
    catch(error){
        console.log("database Initialization failed: ", error);
        process.exit(1);
        
    }
}

export default initDB;