from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = "db.sqlite3"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    conn = get_conn()
    ranking = conn.execute("""
        SELECT character_name, COUNT(*) AS cnt
        FROM search_logs
        WHERE searched_at >= datetime('now', '-1 day')
        GROUP BY character_name
        ORDER BY cnt DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return render_template("index.html", ranking=ranking)

@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name", "").strip()

    if not name:
        return render_template("result.html", found=False, query=name)

    conn = get_conn()

    conn.execute(
        "INSERT INTO search_logs (character_name) VALUES (?)",
        (name,)
    )
    conn.commit()

    character = conn.execute("""
        SELECT *
        FROM characters
        WHERE character_name = ?
    """, (name,)).fetchone()

    if not character:
        conn.close()
        return render_template("result.html", found=False, query=name)

    linked_chars = conn.execute("""
        SELECT character_name, job, level
        FROM characters
        WHERE unique_code = ?
        ORDER BY level DESC, character_name ASC
    """, (character["unique_code"],)).fetchall()

    reports = conn.execute("""
        SELECT category, summary, evidence, report_date
        FROM reports
        WHERE unique_code = ?
        ORDER BY report_date DESC
    """, (character["unique_code"],)).fetchall()

    report_count = len(reports)
    evidence_count = sum(1 for r in reports if r["evidence"] == 1)

    conn.close()

    return render_template(
        "result.html",
        found=True,
        character=character,
        linked_chars=linked_chars,
        reports=reports,
        report_count=report_count,
        evidence_count=evidence_count,
        query=name
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
