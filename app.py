from flask import Flask, request, redirect, url_for, render_template_string, g
import os
import sqlite3
from datetime import datetime

try:
    import psycopg2
    import psycopg2.extras
except Exception:
    psycopg2 = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
USE_POSTGRES = DATABASE_URL.startswith('postgres') and psycopg2 is not None
SQLITE_PATH = os.environ.get('SQLITE_PATH', 'mlhunt.db')

JOBS = [
    '메지션', '위자드(불,독)', '위자드(썬,콜)', '클레릭', '파이터', '페이지', '스피어맨',
    '헌터', '사수', '시프', '어쌔신', '기타'
]
KILL_TYPES = ['원킬', '투컷', '쓰리컷', '기타']

BASE_CSS = """
:root {
  --bg: #0b1020;
  --panel: rgba(255,255,255,.08);
  --panel-2: rgba(255,255,255,.06);
  --stroke: rgba(255,255,255,.10);
  --text: #eef2ff;
  --muted: #a7b0c8;
  --brand: #7c9cff;
  --brand-2: #67e8f9;
  --good: #34d399;
  --warn: #fbbf24;
  --danger: #fb7185;
  --shadow: 0 16px 50px rgba(0,0,0,.28);
  --radius: 24px;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Inter, Pretendard, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  background:
    radial-gradient(circle at top left, rgba(124,156,255,.18), transparent 30%),
    radial-gradient(circle at top right, rgba(103,232,249,.14), transparent 28%),
    linear-gradient(180deg, #0b1020 0%, #121a33 100%);
  color: var(--text);
  min-height: 100vh;
}
a { color: inherit; text-decoration: none; }
.wrapper { max-width: 1160px; margin: 0 auto; padding: 24px 18px 80px; }
.nav {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 14px 16px; margin-bottom: 18px; position: sticky; top: 0; z-index: 20;
  backdrop-filter: blur(16px); background: rgba(8,12,24,.55); border: 1px solid var(--stroke);
  border-radius: 20px; box-shadow: var(--shadow);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-badge {
  width: 42px; height: 42px; border-radius: 14px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #08101f; font-weight: 900;
}
.brand-title { font-size: 18px; font-weight: 800; }
.brand-sub { color: var(--muted); font-size: 12px; margin-top: 2px; }
.nav-links { display:flex; gap: 10px; flex-wrap: wrap; }
.nav-links a {
  padding: 10px 14px; border-radius: 14px; background: var(--panel-2); border: 1px solid var(--stroke);
  color: var(--muted); font-weight: 700; font-size: 14px;
}
.nav-links a.primary { background: linear-gradient(135deg, var(--brand), #8b5cf6); color: white; }
.hero {
  position: relative; overflow: hidden; border-radius: 32px; padding: 34px;
  background: linear-gradient(135deg, rgba(124,156,255,.15), rgba(255,255,255,.06));
  border: 1px solid var(--stroke); box-shadow: var(--shadow); margin-bottom: 20px;
}
.hero::after {
  content: ''; position: absolute; width: 260px; height: 260px; right: -80px; top: -80px;
  background: radial-gradient(circle, rgba(103,232,249,.35), transparent 65%);
}
.hero h1 { font-size: clamp(32px, 5vw, 52px); margin: 0 0 10px; line-height: 1.04; }
.hero p { margin: 0; max-width: 760px; color: var(--muted); line-height: 1.7; }
.hero-grid {
  display:grid; grid-template-columns: 1.4fr .9fr; gap: 18px; margin-top: 24px;
}
.card, .panel {
  background: var(--panel); border: 1px solid var(--stroke); border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.card { padding: 22px; }
.panel { padding: 22px; }
.section-title { font-size: 20px; font-weight: 900; margin: 0 0 14px; }
.muted { color: var(--muted); line-height: 1.6; }
.grid-3 { display:grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 18px; }
.quick-card {
  padding: 20px; border-radius: 22px; background: var(--panel); border: 1px solid var(--stroke); box-shadow: var(--shadow);
}
.quick-card .emoji { font-size: 22px; margin-bottom: 12px; }
.quick-card h3 { margin: 0 0 6px; font-size: 18px; }
.quick-card p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.6; }
.form-grid { display:grid; grid-template-columns: repeat(12, 1fr); gap: 14px; }
.field { grid-column: span 12; }
.field.half { grid-column: span 6; }
.field.third { grid-column: span 4; }
label { display:block; margin: 0 0 8px; font-size: 13px; font-weight: 800; color: #dbe5ff; }
input, select, textarea {
  width: 100%; padding: 14px 15px; border-radius: 16px; border: 1px solid var(--stroke);
  background: rgba(255,255,255,.06); color: var(--text); outline: none; font-size: 15px;
}
input::placeholder, textarea::placeholder { color: #8f9ab7; }
textarea { min-height: 130px; resize: vertical; }
button, .btn {
  border: none; border-radius: 16px; padding: 14px 18px; font-size: 15px; font-weight: 900; cursor: pointer;
  background: linear-gradient(135deg, var(--brand), #8b5cf6); color: white; box-shadow: var(--shadow);
}
.btn.subtle {
  background: rgba(255,255,255,.08); color: var(--text); border: 1px solid var(--stroke);
}
.search-row { display:flex; gap: 12px; flex-wrap: wrap; }
.search-row input { flex: 1 1 260px; }
.stat-row { display:flex; flex-wrap: wrap; gap: 12px; margin-top: 6px; }
.stat {
  min-width: 150px; padding: 16px; border-radius: 18px; background: rgba(255,255,255,.06); border: 1px solid var(--stroke);
}
.stat .num { font-size: 22px; font-weight: 900; }
.stat .label { color: var(--muted); font-size: 13px; margin-top: 4px; }
.list { display:grid; gap: 12px; }
.item {
  padding: 18px; border-radius: 20px; background: rgba(255,255,255,.05); border: 1px solid var(--stroke);
}
.item-top { display:flex; justify-content: space-between; gap: 12px; align-items: start; }
.badges { display:flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.badge {
  display:inline-flex; align-items:center; gap: 6px; padding: 7px 10px; border-radius: 999px; font-size: 12px; font-weight: 800;
  background: rgba(255,255,255,.08); border: 1px solid var(--stroke); color: #dbe5ff;
}
.badge.good { background: rgba(52,211,153,.12); border-color: rgba(52,211,153,.3); color: #a7f3d0; }
.badge.warn { background: rgba(251,191,36,.12); border-color: rgba(251,191,36,.3); color: #fde68a; }
.empty {
  text-align: center; padding: 36px 18px; border: 1px dashed rgba(255,255,255,.18); border-radius: 22px; color: var(--muted);
}
.notice {
  margin-bottom: 18px; padding: 16px 18px; border-radius: 18px; background: rgba(52,211,153,.12); color: #b7f7d7; border: 1px solid rgba(52,211,153,.28);
}
.footer-note { margin-top: 16px; color: var(--muted); font-size: 13px; line-height: 1.7; }
@media (max-width: 900px) {
  .hero-grid, .grid-3 { grid-template-columns: 1fr; }
  .field.half, .field.third { grid-column: span 12; }
  .nav { position: static; }
}
"""

BASE_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <style>{{ css }}</style>
</head>
<body>
  <div class="wrapper">
    <div class="nav">
      <div class="brand">
        <div class="brand-badge">M</div>
        <div>
          <div class="brand-title">메랜 사냥체커</div>
          <div class="brand-sub">사냥 효율 · 제보 · 계산기</div>
        </div>
      </div>
      <div class="nav-links">
        <a href="{{ url_for('home') }}">홈</a>
        <a href="{{ url_for('search') }}">사냥터 검색</a>
        <a href="{{ url_for('calc') }}">경험치 계산기</a>
        <a class="primary" href="{{ url_for('report') }}">데이터 등록</a>
      </div>
    </div>
    {{ body|safe }}
  </div>
</body>
</html>
"""

HOME_BODY = """
<div class="hero">
  <h1>메이플랜드 사냥 효율을<br>한 번에 체크</h1>
  <p>
    직업·레벨·사냥터 기준으로 유저 제보 데이터를 모아 보고, 경험치 계산기로 레벨업 시간을 바로 계산할 수 있는
    메랜용 툴 사이트다. 박제 대신 <strong>사냥 효율 / 물약값 / 메소 체감</strong> 중심으로 바꿔서 오래 굴릴 수 있게 구성했다.
  </p>

  <div class="hero-grid">
    <div class="panel">
      <div class="section-title">사냥터 검색</div>
      <form action="{{ url_for('search') }}" method="get">
        <div class="search-row">
          <input type="text" name="q" value="{{ q or '' }}" placeholder="예: 사헬2, 아이언뮤테, 불독 44">
          <button type="submit">검색</button>
        </div>
      </form>
      <div class="footer-note">맵 이름, 직업명, 레벨 숫자 아무거나 넣어도 검색되게 해놨다.</div>
    </div>

    <div class="panel">
      <div class="section-title">빠른 이동</div>
      <div class="badges">
        <a class="badge" href="{{ url_for('search', q='사헬2') }}">사헬2</a>
        <a class="badge" href="{{ url_for('search', q='아이언뮤테') }}">아이언뮤테</a>
        <a class="badge" href="{{ url_for('search', q='불독') }}">불독</a>
        <a class="badge" href="{{ url_for('calc') }}">경험치 계산기</a>
      </div>
    </div>
  </div>
</div>

<div class="grid-3">
  <div class="quick-card">
    <div class="emoji">📈</div>
    <h3>사냥 효율 조회</h3>
    <p>직업, 레벨, 사냥터 기준으로 시간당 경험치와 메소 체감을 빠르게 본다.</p>
  </div>
  <div class="quick-card">
    <div class="emoji">🧪</div>
    <h3>유저 제보형 데이터</h3>
    <p>운영자가 직접 고렙일 필요 없이 유저가 데이터를 쌓는 구조로 돌린다.</p>
  </div>
  <div class="quick-card">
    <div class="emoji">⏱️</div>
    <h3>레벨업 시간 계산기</h3>
    <p>현재 경험치, 목표 경험치, 시간당 경험치를 넣으면 예상 시간을 바로 계산한다.</p>
  </div>
</div>

<div class="hero-grid" style="margin-top:18px;">
  <div class="card">
    <div class="section-title">실시간 검색 TOP 10</div>
    {% if ranking %}
      <div class="list">
        {% for row in ranking %}
          <a class="item" href="{{ url_for('search', q=row.q) }}">
            <div class="item-top">
              <strong>{{ loop.index }}. {{ row.q }}</strong>
              <span class="badge">{{ row.cnt }}회</span>
            </div>
          </a>
        {% endfor %}
      </div>
    {% else %}
      <div class="empty">아직 검색 기록이 없다.</div>
    {% endif %}
  </div>

  <div class="card">
    <div class="section-title">최근 등록 데이터</div>
    {% if recent_reports %}
      <div class="list">
        {% for item in recent_reports %}
          <a class="item" href="{{ url_for('search', q=item.map_name) }}">
            <div class="item-top">
              <strong>{{ item.map_name }}</strong>
              <span class="badge">Lv.{{ item.level }}</span>
            </div>
            <div class="muted">{{ item.job }} · {{ item.kill_type }} · {{ item.exp_per_hour }} exp/h</div>
          </a>
        {% endfor %}
      </div>
    {% else %}
      <div class="empty">아직 등록된 사냥 데이터가 없다.</div>
    {% endif %}
  </div>
</div>
"""

SEARCH_BODY = """
<div class="card" style="margin-bottom:18px;">
  <div class="section-title">사냥터 검색</div>
  <form action="{{ url_for('search') }}" method="get">
    <div class="search-row">
      <input type="text" name="q" value="{{ q or '' }}" placeholder="예: 사헬2, 불독, 44">
      <button type="submit">검색</button>
      <a class="btn subtle" href="{{ url_for('report') }}">데이터 등록</a>
    </div>
  </form>
</div>

{% if saved == '1' %}
<div class="notice">등록 완료. 검색 결과에 바로 반영됐다.</div>
{% endif %}

{% if q %}
  <div class="card" style="margin-bottom:18px;">
    <div class="section-title">검색 결과: {{ q }}</div>
    <div class="stat-row">
      <div class="stat"><div class="num">{{ results|length }}</div><div class="label">검색 결과</div></div>
      <div class="stat"><div class="num">{{ avg_exp }}</div><div class="label">평균 exp/h</div></div>
      <div class="stat"><div class="num">{{ popular_kill_type }}</div><div class="label">가장 많은 킬 타입</div></div>
    </div>
  </div>

  <div class="card">
    {% if results %}
      <div class="list">
        {% for r in results %}
          <div class="item">
            <div class="item-top">
              <div>
                <strong style="font-size:18px;">{{ r.map_name }}</strong>
                <div class="muted">{{ r.job }} · Lv.{{ r.level }} · 등록일 {{ r.created_at }}</div>
              </div>
              <div class="badges">
                <span class="badge good">{{ r.exp_per_hour }} exp/h</span>
                <span class="badge">{{ r.kill_type }}</span>
              </div>
            </div>
            <div class="badges">
              {% if r.mesos_per_hour %}<span class="badge">메소 {{ r.mesos_per_hour }}/h</span>{% endif %}
              {% if r.potion_cost %}<span class="badge warn">물약 {{ r.potion_cost }}/h</span>{% endif %}
              {% if r.note_url %}<a class="badge" target="_blank" rel="noopener" href="{{ r.note_url }}">참고 링크</a>{% endif %}
            </div>
            {% if r.memo %}
              <div class="footer-note">{{ r.memo }}</div>
            {% endif %}
          </div>
        {% endfor %}
      </div>
    {% else %}
      <div class="empty">
        검색 결과가 없다.<br>먼저 데이터 하나 등록해보면 된다.
      </div>
    {% endif %}
  </div>
{% else %}
  <div class="card">
    <div class="empty">맵 이름, 직업, 레벨 아무거나 검색해봐라.</div>
  </div>
{% endif %}
"""

REPORT_BODY = """
<div class="hero" style="padding:28px; margin-bottom:18px;">
  <h1 style="font-size:34px;">사냥 데이터 등록</h1>
  <p>직업, 레벨, 사냥터, 시간당 경험치 정도만 넣어도 충분하다. 복잡한 검수 없이 바로 쌓는 MVP용 구조다.</p>
</div>

<div class="card">
  <form method="post">
    <div class="form-grid">
      <div class="field half">
        <label>직업</label>
        <select name="job" required>
          <option value="">선택</option>
          {% for job in jobs %}<option value="{{ job }}">{{ job }}</option>{% endfor %}
        </select>
      </div>
      <div class="field half">
        <label>레벨</label>
        <input type="number" name="level" min="1" max="300" placeholder="예: 44" required>
      </div>
      <div class="field half">
        <label>사냥터</label>
        <input type="text" name="map_name" placeholder="예: 사헬2" required>
      </div>
      <div class="field half">
        <label>킬 타입</label>
        <select name="kill_type" required>
          {% for item in kill_types %}<option value="{{ item }}">{{ item }}</option>{% endfor %}
        </select>
      </div>
      <div class="field third">
        <label>시간당 경험치</label>
        <input type="number" name="exp_per_hour" min="1" placeholder="예: 230000" required>
      </div>
      <div class="field third">
        <label>시간당 메소</label>
        <input type="number" name="mesos_per_hour" min="0" placeholder="선택">
      </div>
      <div class="field third">
        <label>시간당 물약값</label>
        <input type="number" name="potion_cost" min="0" placeholder="선택">
      </div>
      <div class="field">
        <label>메모</label>
        <textarea name="memo" placeholder="예: 사헬2 기준 투컷, 자리 널널하면 체감 괜찮음"></textarea>
      </div>
      <div class="field">
        <label>참고 링크 (선택)</label>
        <input type="text" name="note_url" placeholder="예: 영상/스크린샷 URL">
      </div>
      <div class="field">
        <button type="submit">등록하기</button>
      </div>
    </div>
  </form>
  <div class="footer-note">스팸 방지용으로 서버에서 기본 검증은 걸어뒀다. 너무 긴 입력도 잘라낸다.</div>
</div>
"""

CALC_BODY = """
<div class="hero" style="padding:28px; margin-bottom:18px;">
  <h1 style="font-size:34px;">경험치 계산기</h1>
  <p>현재 경험치, 목표 경험치, 시간당 경험치를 넣으면 예상 소요 시간을 계산한다.</p>
</div>

<div class="hero-grid">
  <div class="card">
    <form method="post">
      <div class="form-grid">
        <div class="field">
          <label>현재 경험치</label>
          <input type="number" name="current_exp" min="0" value="{{ form.current_exp }}" required>
        </div>
        <div class="field">
          <label>목표 경험치</label>
          <input type="number" name="target_exp" min="0" value="{{ form.target_exp }}" required>
        </div>
        <div class="field">
          <label>시간당 경험치</label>
          <input type="number" name="exp_per_hour" min="1" value="{{ form.exp_per_hour }}" required>
        </div>
        <div class="field">
          <button type="submit">계산하기</button>
        </div>
      </div>
    </form>
  </div>

  <div class="card">
    <div class="section-title">계산 결과</div>
    {% if result %}
      <div class="stat-row">
        <div class="stat"><div class="num">{{ result.need_exp }}</div><div class="label">필요 경험치</div></div>
        <div class="stat"><div class="num">{{ result.hours }}</div><div class="label">필요 시간(시간)</div></div>
        <div class="stat"><div class="num">{{ result.days_1h }}</div><div class="label">하루 1시간 기준 일수</div></div>
      </div>
      <div class="footer-note">하루 2시간이면 약 {{ result.days_2h }}일, 하루 3시간이면 약 {{ result.days_3h }}일 정도다.</div>
    {% else %}
      <div class="empty">왼쪽에 숫자 넣고 계산하면 바로 나온다.</div>
    {% endif %}
  </div>
</div>
"""


def get_db():
    if 'db' in g:
        return g.db
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        g.db = conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def query(sql, params=None, fetchone=False, fetchall=False):
    params = params or []
    conn = get_db()
    if USE_POSTGRES:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params)
        if fetchone:
            row = cur.fetchone()
            cur.close()
            return row
        if fetchall:
            rows = cur.fetchall()
            cur.close()
            return rows
        cur.close()
        return None
    else:
        cur = conn.cursor()
        cur.execute(sql, params)
        if fetchone:
            row = cur.fetchone()
            cur.close()
            return row
        if fetchall:
            rows = cur.fetchall()
            cur.close()
            return rows
        cur.close()
        return None


def commit():
    get_db().commit()


def close_db(e=None):
    conn = g.pop('db', None)
    if conn is not None:
        conn.close()


app.teardown_appcontext(close_db)


def init_db():
    conn = get_db()
    if USE_POSTGRES:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS hunt_reports (
                id SERIAL PRIMARY KEY,
                job VARCHAR(50) NOT NULL,
                level INTEGER NOT NULL,
                map_name VARCHAR(100) NOT NULL,
                exp_per_hour INTEGER NOT NULL,
                mesos_per_hour INTEGER NOT NULL DEFAULT 0,
                kill_type VARCHAR(20) NOT NULL,
                potion_cost INTEGER NOT NULL DEFAULT 0,
                memo TEXT,
                note_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS search_logs (
                id SERIAL PRIMARY KEY,
                q VARCHAR(100) NOT NULL,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS hunt_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job TEXT NOT NULL,
                level INTEGER NOT NULL,
                map_name TEXT NOT NULL,
                exp_per_hour INTEGER NOT NULL,
                mesos_per_hour INTEGER NOT NULL DEFAULT 0,
                kill_type TEXT NOT NULL,
                potion_cost INTEGER NOT NULL DEFAULT 0,
                memo TEXT,
                note_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS search_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                q TEXT NOT NULL,
                searched_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()


def seed_if_empty():
    row = query('SELECT COUNT(*) AS cnt FROM hunt_reports', fetchone=True)
    cnt = row['cnt'] if row else 0
    if cnt:
        return
    sample = [
        ('위자드(불,독)', 44, '사헬2', 230000, 90000, '투컷', 35000, '회사에서 돌리기 무난. 자리 좋으면 안정적.', ''),
        ('위자드(불,독)', 45, 'B3 아이언뮤테', 300000, 110000, '투컷', 42000, '투컷 기준이면 체감 효율 꽤 좋음.', ''),
        ('클레릭', 42, '시간의길1', 105000, 50000, '원킬', 22000, '심쩔 or 저강도 사냥용.', ''),
        ('위자드(불,독)', 47, '시길1', 140000, 60000, '쓰리컷', 38000, '지형 익숙하면 할만함.', '')
    ]
    if USE_POSTGRES:
        sql = '''
            INSERT INTO hunt_reports
            (job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
    else:
        sql = '''
            INSERT INTO hunt_reports
            (job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url)
            VALUES (?,?,?,?,?,?,?,?,?)
        '''
    conn = get_db()
    cur = conn.cursor()
    cur.executemany(sql, sample)
    conn.commit()
    cur.close()


def render_page(title, body, **ctx):
    inner = render_template_string(body, **ctx)
    return render_template_string(BASE_HTML, title=title, body=inner, css=BASE_CSS)


@app.before_request
def setup_once():
    init_db()
    seed_if_empty()


@app.route('/')
def home():
    q = request.args.get('q', '').strip()
    if USE_POSTGRES:
        ranking_sql = '''
            SELECT q, COUNT(*) AS cnt
            FROM search_logs
            WHERE searched_at >= NOW() - INTERVAL '1 day'
            GROUP BY q ORDER BY cnt DESC, q ASC LIMIT 10
        '''
        recent_sql = '''
            SELECT map_name, level, job, kill_type, exp_per_hour
            FROM hunt_reports ORDER BY id DESC LIMIT 6
        '''
    else:
        ranking_sql = '''
            SELECT q, COUNT(*) AS cnt
            FROM search_logs
            WHERE searched_at >= datetime('now', '-1 day')
            GROUP BY q ORDER BY cnt DESC, q ASC LIMIT 10
        '''
        recent_sql = '''
            SELECT map_name, level, job, kill_type, exp_per_hour
            FROM hunt_reports ORDER BY id DESC LIMIT 6
        '''
    ranking = query(ranking_sql, fetchall=True)
    recent_reports = query(recent_sql, fetchall=True)
    return render_page('메랜 사냥체커', HOME_BODY, ranking=ranking, recent_reports=recent_reports, q=q)


@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    saved = request.args.get('saved', '').strip()
    results = []
    avg_exp = '-'
    popular_kill_type = '-'

    if q:
        if USE_POSTGRES:
            query('INSERT INTO search_logs (q) VALUES (%s)', [q])
            sql = '''
                SELECT id, job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url,
                       TO_CHAR(created_at, 'YYYY-MM-DD') AS created_at
                FROM hunt_reports
                WHERE map_name ILIKE %s OR job ILIKE %s OR CAST(level AS TEXT) = %s
                ORDER BY exp_per_hour DESC, level ASC, id DESC
            '''
            params = [f'%{q}%', f'%{q}%', q]
        else:
            query('INSERT INTO search_logs (q) VALUES (?)', [q])
            sql = '''
                SELECT id, job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url,
                       substr(created_at, 1, 10) AS created_at
                FROM hunt_reports
                WHERE map_name LIKE ? OR job LIKE ? OR CAST(level AS TEXT) = ?
                ORDER BY exp_per_hour DESC, level ASC, id DESC
            '''
            params = [f'%{q}%', f'%{q}%', q]
        commit()
        results = query(sql, params, fetchall=True)
        if results:
            exps = [int(r['exp_per_hour']) for r in results]
            avg_exp = f"{sum(exps)//len(exps):,}"
            freq = {}
            for r in results:
                freq[r['kill_type']] = freq.get(r['kill_type'], 0) + 1
            popular_kill_type = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[0][0]

    return render_page('사냥터 검색', SEARCH_BODY, q=q, results=results, avg_exp=avg_exp, popular_kill_type=popular_kill_type, saved=saved)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        job = request.form.get('job', '').strip()[:50]
        map_name = request.form.get('map_name', '').strip()[:100]
        kill_type = request.form.get('kill_type', '').strip()[:20]
        memo = request.form.get('memo', '').strip()[:1000]
        note_url = request.form.get('note_url', '').strip()[:500]

        try:
            level = int(request.form.get('level', '0'))
            exp_per_hour = int(request.form.get('exp_per_hour', '0'))
            mesos_per_hour = int(request.form.get('mesos_per_hour') or 0)
            potion_cost = int(request.form.get('potion_cost') or 0)
        except ValueError:
            return '숫자 입력값이 잘못됐다.', 400

        if not job or job not in JOBS or not map_name or kill_type not in KILL_TYPES:
            return '입력값이 올바르지 않다.', 400
        if level < 1 or level > 300 or exp_per_hour < 1:
            return '레벨 또는 경험치 값이 올바르지 않다.', 400
        if note_url and not (note_url.startswith('http://') or note_url.startswith('https://')):
            return '참고 링크는 http:// 또는 https://로 시작해야 한다.', 400

        if USE_POSTGRES:
            sql = '''
                INSERT INTO hunt_reports
                (job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        else:
            sql = '''
                INSERT INTO hunt_reports
                (job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url)
                VALUES (?,?,?,?,?,?,?,?,?)
            '''
        query(sql, [job, level, map_name, exp_per_hour, mesos_per_hour, kill_type, potion_cost, memo, note_url])
        commit()
        return redirect(url_for('search', q=map_name, saved=1))

    return render_page('사냥 데이터 등록', REPORT_BODY, jobs=JOBS, kill_types=KILL_TYPES)


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    form = {'current_exp': '', 'target_exp': '', 'exp_per_hour': ''}
    if request.method == 'POST':
        form = {
            'current_exp': request.form.get('current_exp', '').strip(),
            'target_exp': request.form.get('target_exp', '').strip(),
            'exp_per_hour': request.form.get('exp_per_hour', '').strip(),
        }
        try:
            current_exp = int(form['current_exp'])
            target_exp = int(form['target_exp'])
            exp_per_hour = int(form['exp_per_hour'])
        except ValueError:
            return '숫자를 제대로 입력해라.', 400
        if target_exp <= current_exp or exp_per_hour <= 0:
            return '목표 경험치는 현재보다 커야 하고 시간당 경험치는 1 이상이어야 한다.', 400

        need_exp = target_exp - current_exp
        hours = round(need_exp / exp_per_hour, 2)
        result = {
            'need_exp': f'{need_exp:,}',
            'hours': hours,
            'days_1h': round(hours / 1, 1),
            'days_2h': round(hours / 2, 1),
            'days_3h': round(hours / 3, 1),
        }

    return render_page('경험치 계산기', CALC_BODY, result=result, form=form)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
