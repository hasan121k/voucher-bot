import sqlite3, time, random

db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS vouchers(
 code TEXT PRIMARY KEY,
 expire INTEGER,
 max_use INTEGER,
 used INTEGER,
 active INTEGER,
 paused INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
 uid INTEGER,
 code TEXT,
 time INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS settings(
 key TEXT PRIMARY KEY,
 value TEXT
)
""")

db.commit()

def create_voucher(minutes, max_use):
    code = str(random.randint(10000,999999))
    exp = int(time.time()) + minutes*60
    cur.execute("INSERT INTO vouchers VALUES(?,?,?,?,1,0)",
                (code, exp, max_use, 0))
    db.commit()
    return code

def get_voucher(code):
    return cur.execute(
        "SELECT * FROM vouchers WHERE code=?", (code,)
    ).fetchone()

def use_voucher(uid, code):
    cur.execute("UPDATE vouchers SET used=used+1 WHERE code=?", (code,))
    cur.execute("INSERT INTO users VALUES(?,?,?)",
                (uid, code, int(time.time())))
    db.commit()

def pause_voucher(code):
    cur.execute("UPDATE vouchers SET paused=1 WHERE code=?", (code,))
    db.commit()

def resume_voucher(code):
    cur.execute("UPDATE vouchers SET paused=0 WHERE code=?", (code,))
    db.commit()

def delete_voucher(code):
    cur.execute("DELETE FROM vouchers WHERE code=?", (code,))
    db.commit()

def list_vouchers():
    return cur.execute("SELECT * FROM vouchers").fetchall()

def set_setting(k, v):
    cur.execute("REPLACE INTO settings VALUES(?,?)", (k, v))
    db.commit()

def get_setting(k):
    r = cur.execute(
        "SELECT value FROM settings WHERE key=?", (k,)
    ).fetchone()
    return r[0] if r else None

def analytics():
    total = cur.execute("SELECT COUNT(*) FROM vouchers").fetchone()[0]
    active = cur.execute(
        "SELECT COUNT(*) FROM vouchers WHERE active=1 AND paused=0"
    ).fetchone()[0]
    paused = cur.execute(
        "SELECT COUNT(*) FROM vouchers WHERE paused=1"
    ).fetchone()[0]
    users = cur.execute(
        "SELECT COUNT(DISTINCT uid) FROM users"
    ).fetchone()[0]
    return total, active, paused, users
