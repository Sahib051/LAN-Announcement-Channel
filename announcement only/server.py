"""
LAN Announcements Server with roles:

- Client:
    - Chooses name only (no password).
    - Sees announcements and system messages.
    - Cannot send messages.

- Admin:
    - Chooses name + admin password.
    - Sees announcements + system messages.
    - Sees list of connected users.
    - Can send announcements.

Run:
    python server.py

Open:
    http://localhost:5001
    http://<local-ip>:5001
"""

import socket
import datetime

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

# ── Config ──────────────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = "lan_messenger_secret_2024"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

MAX_HISTORY = 500
announce_history = []      # announcements
users = {}                 # sid -> {"name": str, "role": "admin"|"client"}

ADMIN_PASSWORD = "admin123"   # CHANGE this


def now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_trimmed(lst, msg):
    lst.append(msg)
    if len(lst) > MAX_HISTORY:
        del lst[:-MAX_HISTORY]


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def broadcast_user_list():
    """Send current connected user list to all admins only."""
    user_list = [
        {"name": info["name"], "role": info["role"]}
        for info in users.values()
    ]
    # We send an event that clients also receive, but clients will ignore it in the UI.
    socketio.emit("user_list", user_list, room="announcements")


def emit_to_admins(event, data):
    """Emit an event only to sockets that are admins."""
    for sid, info in users.items():
        if info["role"] == "admin":
            socketio.emit(event, data, to=sid)

# ── Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── Socket.IO events ────────────────────────────────────────────────────

@socketio.on("connect")
def on_connect():
    sid = request.sid
    ip = request.remote_addr or "unknown"
    print(f"[+] Socket connected: {sid} ({ip})")

    join_room("announcements")

    # Send announcements history
    emit("history", {
        "announcements": announce_history,
    })


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    ip = request.remote_addr or "unknown"
    print(f"[-] Socket disconnected: {sid} ({ip})")

    if sid in users:
        left_name = users[sid]["name"]
        del users[sid]
        emit_to_admins("system_message", {
            "text": f"{left_name} left.",
            "timestamp": now_str()
        })
    broadcast_user_list()


@socketio.on("register_user")
def on_register_user(data):
    """
    Client or admin registers:
        data = { "name": "...", "role": "admin"|"client", "admin_password": "..." }
    """
    sid = request.sid
    name = (data.get("name") or "").strip()
    role = data.get("role") or "client"
    password = data.get("admin_password") or ""

    if not name:
        emit("error_message", {"text": "Name is required."})
        return

    if role == "admin":
        if password != ADMIN_PASSWORD:
            emit("error_message", {"text": "Invalid admin password."})
            return

    users[sid] = {"name": name, "role": role}

    emit_to_admins("system_message", {
        "text": f"{name} joined as {role}.",
        "timestamp": now_str()
})

    broadcast_user_list()

    broadcast_user_list()

    # Let this socket know what role it has (for UI decisions)
    emit("role_confirmed", {"role": role})


@socketio.on("send_announcement")
def on_send_announcement(data):
    """
    Admin-only announcement. The server checks the role from 'users'.
    data = { "text": "..." }
    """
    sid = request.sid
    if sid not in users or users[sid]["role"] != "admin":
        emit("error_message", {"text": "Only admin can send announcements."})
        return

    text = (data.get("text") or "").strip()
    sender = users[sid]["name"] if sid in users else "Admin"

    if not text:
        return

    msg = {
        "type": "announcement",
        "sender": f"📢 {sender}",
        "text": text,
        "timestamp": now_str(),
    }
    add_trimmed(announce_history, msg)

    socketio.emit("announcement_message", msg, room="announcements")
    print(f"[ANNOUNCEMENT] {sender}: {text}")


# ── Entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 60)
    print("  🌐  LAN Announcements Server (Admin & Clients)")
    print("=" * 60)
    print("  Local access  : http://localhost:5001")
    print(f"  Network access: http://{local_ip}:5001")
    print(f"  Admin password: {ADMIN_PASSWORD}")
    print("=" * 60)
    print("  Press Ctrl+C to stop\n")

    socketio.run(app, host="0.0.0.0", port=5001, debug=False)