from flask import Flask, render_template
from pathlib import Path
from dotenv import load_dotenv
from database import get_connection

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test-db")
def test_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM customers")
                count = cur.fetchone()[0]

        return f"Database connected successfully! Customers: {count}"

    except Exception as e:
        app.logger.exception("Database connection test failed")
        return "Database connection failed. Check the Flask terminal for details.", 500


if __name__ == "__main__":
    app.run(debug=True)
