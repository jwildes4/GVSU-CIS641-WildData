from flask import Flask, render_template, request
from pathlib import Path
from dotenv import load_dotenv
from werkzeug.exceptions import RequestEntityTooLarge

from database import get_connection
from spreadsheet import read_spreadsheet

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = Flask(__name__)

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            return render_template(
                "index.html",
                error="Please select an Excel file."
            )

        if not file.filename.lower().endswith(".xlsx"):
            return render_template(
                "index.html",
                error="Only .xlsx files are supported."
            )

        try:
            df = read_spreadsheet(file)

            columns = df.columns.astype(str).tolist()

            # Convert missing values to empty strings for display
            preview = df.head(5).fillna("").astype(str).values.tolist()

            return render_template(
                "index.html",
                columns=columns,
                preview=preview,
                filename=file.filename
            )

        except Exception:
            app.logger.exception("Spreadsheet upload failed")
            return render_template(
                "index.html",
                error="Unable to read the Excel file. Check that it is a valid, nonempty .xlsx spreadsheet."
            )

    return render_template("index.html")


@app.route("/test-db")
def test_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM customers")
                count = cur.fetchone()[0]

        return f"Database connected successfully! Customers: {count}"

    except Exception:
        app.logger.exception("Database connection test failed")
        return "Database connection failed. Check the Flask terminal for details.", 500


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    return render_template(
        "index.html",
        error="File is too large. Maximum upload size is 5 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
