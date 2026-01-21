import express from "express";
import initDB from "./db/initdb.js";
import createTables from "./db/createTables.js";
import {app} from "./app.js";

async function startServer() {
    await initDB();
    await createTables()
    app.listen(process.env.PORT|| 8000, () => {
        console.log(`Server is running on port  http://localhost:${process.env.PORT}`);
    });
}

startServer();