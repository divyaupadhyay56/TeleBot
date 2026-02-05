import pandas as pd

from app import create_app
from app.database.db import db
from app.database.models import JanaushadhiKendra

app = create_app()

def import_xlsx(file_path):
    df = pd.read_excel(file_path)

    with app.app_context():
        for _, row in df.iterrows():
            kendra_code = str(row["Kendra  Code"]).strip()

            exists = JanaushadhiKendra.query.filter_by(
                kendra_code=kendra_code
            ).first()

            if exists:
                continue  # avoid duplicates

            kendra = JanaushadhiKendra(
                sr_no=int(row["Sr.No"]),
                kendra_code=kendra_code,
                name=str(row["Name"]).strip(),
                state_name=str(row["State Name"]).strip(),
                district_name=str(row["District Name"]).strip(),
                pin_code=str(row["Pin Code"]).strip(),
                address=str(row["Address"]).strip()
            )

            db.session.add(kendra)

        db.session.commit()
        print("✅ Jan Aushadhi Kendras imported successfully")
