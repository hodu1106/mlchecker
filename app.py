from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
import psycopg2.extras
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)


def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def ensure_schema():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            character_name TEXT NOT NULL UNIQUE,
            unique_code TEXT NOT NULL,
            job TEXT,
            level INTEGER,
            world TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id SERIAL PRIMARY KEY,
            character_name TEXT NOT NULL,
            unique_code TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            evidence INTEGER NOT NULL DEFAULT 0,
            report_date DATE NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_logs (
            id SERIAL PRIMARY KEY,
            character_name TEXT NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/", methods=["GET"])
def index():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT character_name, COUNT(*) AS cnt
        FROM search_logs
        WHERE searched_at >= NOW() - INTERVAL '1 day'
        GROUP BY character_name
        ORDER BY cnt DESC
        LIMIT 10
    """)
    ranking = cur.fetchall()

    cur.execute("""
        SELECT character_name, category, report_date
        FROM reports
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_reports = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        ranking=ranking,
        recent_reports=recent_reports
    )


@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name", "").strip()
    reported = request.args.get("reported", "").strip()

    if not name:
        return render_template(
            "result.html",
            found=False,
            query=name,
            reported=reported
        )

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "INSERT INTO search_logs (character_name) VALUES (%s)",
        (name,)
    )
    conn.commit()

    cur.execute("""
        SELECT *
        FROM characters
        WHERE character_name = %s
    """, (name,))
    character = cur.fetchone()

    if not character:
        cur.close()
        conn.close()
        return render_template(
            "result.html",
            found=False,
            query=name,
            reported=reported
        )

    cur.execute("""
        SELECT character_name, job, level
        FROM characters
        WHERE unique_code = %s
        ORDER BY level DESC NULLS LAST, character_name ASC
    """, (character["unique_code"],))
    linked_chars = cur.fetchall()

    cur.execute("""
        SELECT category, summary, evidence, report_date, image_url
        FROM reports
        WHERE unique_code = %s
        ORDER BY report_date DESC, id DESC
    """, (character["unique_code"],))
    reports = cur.fetchall()

    report_count = len(reports)
    evidence_count = sum(1 for r in reports if r["evidence"] == 1)

    cur.close()
    conn.close()

    return render_template(
        "result.html",
        found=True,
        character=character,
        linked_chars=linked_chars,
        reports=reports,
        report_count=report_count,
        evidence_count=evidence_count,
        query=name,
        reported=reported
    )


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form.get("character_name", "").strip()
        code = request.form.get("unique_code", "").strip()
        job = request.form.get("job", "").strip()
        level_raw = request.form.get("level", "").strip()
        category = request.form.get("category", "").strip()
        summary = request.form.get("summary", "").strip()
        evidence = 1 if request.form.get("evidence") == "on" else 0

        if not name or not code or not category or not summary:
            return "입력값이 부족합니다."

        level = 0
        if level_raw.isdigit():
            level = int(level_raw)

        image_url = None
        uploaded_file = request.files.get("image")

        if uploaded_file and uploaded_file.filename:
            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                folder="mlchecker_reports"
            )
            image_url = upload_result.get("secure_url")

        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            SELECT *
            FROM characters
            WHERE character_name = %s
        """, (name,))
        existing_character = cur.fetchone()

        if not existing_character:
            cur.execute("""
                INSERT INTO characters (
                    character_name,
                    unique_code,
                    job,
                    level,
                    world
                )
                VALUES (%s, %s, %s, %s, '메이플랜드')
            """, (name, code, job, level))
        else:
            cur.execute("""
                UPDATE characters
                SET
                    unique_code = %s,
                    job = CASE
                        WHEN %s != '' THEN %s
                        ELSE job
                    END,
                    level = CASE
                        WHEN %s > 0 THEN %s
                        ELSE level
                    END,
                    world = '메이플랜드'
                WHERE character_name = %s
            """, (code, job, job, level, level, name))

        cur.execute("""
            INSERT INTO reports (
                character_name,
                unique_code,
                category,
                summary,
                evidence,
                report_date,
                image_url
            )
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, %s)
        """, (name, code, category, summary, evidence, image_url))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("search", name=name, reported=1))

    return render_template("report.html")


ensure_schema()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
