import os
import uuid
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv

from database import get_connection
from spreadsheet import read_spreadsheet
from mapping import DATABASE_FIELDS, REQUIRED_FIELDS, validate_mapping


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_DIR = PROJECT_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            return render_template(
                "index.html", error="Please select an Excel file."
            )

        if not file.filename.lower().endswith(".xlsx"):
            return render_template(
                "index.html", error="Only .xlsx files are supported."
            )

        try:
            df = read_spreadsheet(file)

            # Require distinct column names for unambiguous mapping
            if not df.columns.is_unique:
                raise ValueError("Spreadsheet column names must be unique.")

            # Remove any previous upload from this session
            previous_id = session.get("upload_id")
            if previous_id:
                (UPLOAD_DIR / f"{previous_id}.xlsx").unlink(missing_ok=True)

            upload_id = uuid.uuid4().hex
            file.stream.seek(0)
            file.save(UPLOAD_DIR / f"{upload_id}.xlsx")
            session["upload_id"] = upload_id
            session.pop("column_mapping", None)

            columns = df.columns.astype(str).tolist()
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
                error="Unable to read the spreadsheet. Check the file and column headers."
            )

    return render_template("index.html")


@app.route("/mapping", methods=["GET", "POST"])
def mapping():
    upload_id = session.get("upload_id")

    if not upload_id:
        return redirect(url_for("index"))

    file_path = UPLOAD_DIR / f"{upload_id}.xlsx"

    if not file_path.exists():
        session.pop("upload_id", None)
        return redirect(url_for("index"))

    df = read_spreadsheet(file_path)
    excel_columns = df.columns.astype(str).tolist()

    # Automatically suggest matching names where possible
    suggested_mapping = {
        field: field if field in excel_columns else ""
        for field in DATABASE_FIELDS
    }

    if request.method == "POST":
        selected_mapping = {
            field: request.form.get(field, "")
            for field in DATABASE_FIELDS
        }

        errors = validate_mapping(selected_mapping, excel_columns)

        if errors:
            return render_template(
                "mapping.html",
                excel_columns=excel_columns,
                database_fields=DATABASE_FIELDS,
                required_fields=REQUIRED_FIELDS,
                selected_mapping=selected_mapping,
                errors=errors
            )

        session["column_mapping"] = selected_mapping

        return render_template(
            "mapping.html",
            excel_columns=excel_columns,
            database_fields=DATABASE_FIELDS,
            required_fields=REQUIRED_FIELDS,
            selected_mapping=selected_mapping,
            success=True
        )

    return render_template(
        "mapping.html",
        excel_columns=excel_columns,
        database_fields=DATABASE_FIELDS,
        required_fields=REQUIRED_FIELDS,
        selected_mapping=suggested_mapping
    )


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
        return "Database connection failed. Check the Flask terminal.", 500


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    return render_template(
        "index.html",
        error="File is too large. Maximum upload size is 5 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
