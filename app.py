from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from database import get_db
from datetime import datetime
import uuid
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
             SELECT * FROM users 
            WHERE username=%s AND password=%s AND status='approved'
            """, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        status = "approved" if role == "user" else "pending"

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, password, role, status)
                VALUES (%s, %s, %s, %s)
            """, (username, password, role, status))
            conn.commit()
        except:
            conn.close()
            return render_template(
                "register.html",
                error="Username already exists"
            )

        conn.close()

        if role == "admin":
            return render_template(
                "register.html",
                success="Admin request submitted. Await approval."
            )

        return redirect("/login")

    return render_template("register.html")

@app.route("/admin/approvals")
def admin_approvals():
    if session.get("role") != "admin":
        return "Unauthorized", 403

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, username, role 
        FROM users 
        WHERE status='pending'
    """)
    pending_users = cursor.fetchall()
    conn.close()

    return render_template(
        "admin_approvals.html",
        users=pending_users
    )


@app.route("/admin/approve/<int:user_id>")
def approve_user(user_id):
    if session.get("role") != "admin":
        return "Unauthorized", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
                   
        UPDATE users SET status='approved'
        WHERE id=%s
    """, (user_id,))
    conn.commit()
    conn.close()

    return redirect("/admin/approvals")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- PAYMENT ----------------
@app.route("/")
def payment():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("payment.html")


@app.route("/process_payment", methods=["POST"])
def process_payment():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    txn_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (
            transaction_id, patient_name, patient_id, visit_id,
            services, amount, payment_method, remarks, timestamp, user_id
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        txn_id,
        data["patient_name"],
        data["patient_id"],
        data["visit_id"],
        ", ".join(data["services"]),
        data["amount"],
        data["payment_method"],
        data["remarks"],
        timestamp,
        session["user_id"]
    ))
    conn.commit()
    conn.close()

    return jsonify({"transaction_id": txn_id})


# ---------------- TRANSACTIONS ----------------
@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    if session["role"] == "admin":
        cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    else:
        cursor.execute(
            "SELECT * FROM transactions WHERE user_id=%s ORDER BY id DESC",
            (session["user_id"],)
        )

    rows = cursor.fetchall()
    conn.close()
    return render_template("transactions.html", rows=rows)


# ---------------- PDF RECEIPT ----------------
@app.route("/receipt/<txn_id>")
def receipt(txn_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM transactions WHERE transaction_id=%s",
        (txn_id,)
    )
    txn = cursor.fetchone()
    conn.close()

    if not txn:
        return "Not found", 404

    if session["role"] != "admin" and txn["user_id"] != session["user_id"]:
        return "Forbidden", 403

    file_name = f"receipt_{txn_id}.pdf"
    pdf = canvas.Canvas(file_name)
    y = 800
    pdf.drawString(50, y, "Hospital Payment Receipt")
    y -= 40

    for k, v in txn.items():
        pdf.drawString(50, y, f"{k}: {v}")
        y -= 20

    pdf.save()
    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
