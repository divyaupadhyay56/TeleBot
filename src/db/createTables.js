import db from "./index.js";
import createUserTable from "../models/user.model.js";
import createPrescriptionTable from "../models/perescription.model.js";
import createMedicalRecordTable from "../models/medical.record.js";


async function createTables() {
    try{
        await db.query(createUserTable);
        await db.query(createPrescriptionTable);
        await db.query(createMedicalRecordTable);

        console.log("All tables created successfully");
    }
    catch(error){
        console.log("Tables creation failed: ", error);
        process.exit(1);
    }
}

export default createTables;
