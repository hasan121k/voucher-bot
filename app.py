from flask import Flask, request, redirect
from database import *
from config import WEB_ADMIN_USER, WEB_ADMIN_PASS

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["u"] == WEB_ADMIN_USER and
            request.form["p"] == WEB_ADMIN_PASS
        ):
            return redirect("/dashboard")

    return """
    <h3>Admin Login</h3>
    <form method='post'>
    Username: <input name='u'><br>
    Password: <input name='p'><br>
    <button>Login</button>
    </form>
    """

@app.route("/dashboard")
def dashboard():
    t, a, p, u = analytics()
    return f"""
    <h3>Analytics</h3>
    Total: {t}<br>
    Active: {a}<br>
    Paused: {p}<br>
    Users: {u}<br>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
