from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

Database_name = "clients.db"

def create_db():
    conn = sqlite3.connect(Database_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_num TEXT,
            company TEXT,
            subject TEXT NOT NULL,
            method TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()

@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        f_name = data.get("firstName")
        l_name = data.get("lastName")
        email = data.get("email")
        phone_no = data.get("phone")
        company = data.get("company")
        subject = data.get("subject")
        method = data.get("contactMethod")
        message = data.get("message")
        
        conn = sqlite3.connect(Database_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clients(first_name, last_name, email, phone_num, company, subject, method, message)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (f_name, l_name, email, phone_no, company, subject, method, message))

        conn.commit()
        conn.close()

        return render_template("success.html", name=f_name)
    
    return render_template("index.html")

@app.route("/clients")
def all_clients():
    conn = sqlite3.connect(Database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    all_clients = cursor.fetchall()
    conn.close()
    return render_template("clients.html", clients=all_clients)

if __name__ == "__main__":
    app.run(debug=True)