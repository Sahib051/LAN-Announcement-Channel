# LAN Announcements (Flask + Socket.IO)

LAN‑based **announcement board** built with Flask and Flask‑SocketIO.

- Clients join with a **name** (no password).
- Admin joins with **name + admin password**.
- Only the **admin** can send announcements.
- All users see announcements in real time.
- Only the **admin** sees the list of connected users and join/leave events.

This is designed for small LANs or classroom/local lab environments where one person broadcasts information to all connected devices.

---

## Features

- **Roles**
  - Client: view‑only, sees announcements in real time.
  - Admin: can send announcements and see connected users.

- **Real‑time communication**
  - Built on Flask‑SocketIO and Socket.IO.
  - Works across devices on the same Wi‑Fi/hotspot.

- **Simple login flow**
  - Choose role (Client/Admin).
  - Enter name.
  - If Admin, also enter password.

---

## Tech Stack

- Python 3
- Flask
- Flask‑SocketIO
- Socket.IO JavaScript client (served from `static/socket.io.min.js`)
- HTML, CSS, JavaScript (vanilla)

---

## Project Structure

```text
project-root/
├─ server.py
├─ requirements.txt        (optional)
├─ static/
│   └─ socket.io.min.js    # Socket.IO client JS
└─ templates/
    └─ index.html          # Frontend UI
```

- `server.py` – Flask app + Socket.IO server, role handling, announcements.
- `templates/index.html` – client/admin UI.
- `static/socket.io.min.js` – Socket.IO browser client.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

2. **(Optional) Create and activate a virtual environment**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install flask flask-socketio
```

If you want to keep dependencies in a file:

```bash
pip freeze > requirements.txt
```

---

## Socket.IO Client (static file)

This project uses a **local** Socket.IO client so it works even without internet.

Download a compatible client (example: 4.7.5) and place it in the `static` folder as `socket.io.min.js`:

- From jsDelivr:  
  https://cdn.jsdelivr.net/npm/socket.io-client@4.7.5/dist/socket.io.min.js

Save it as:

```text
static/socket.io.min.js
```

---

## Configuration

In `server.py`, you’ll see:

```python
ADMIN_PASSWORD = "admin123"
```

Change this to whatever password you want for the admin role:

```python
ADMIN_PASSWORD = "your-strong-password"
```

Commit `server.py` **without** your real production password if the repo is public.

---

## Running the Server

From the project root:

```bash
python server.py
```

You should see output similar to:

```text
🌐  LAN Announcements Server (Admin & Clients)
Local access  : http://localhost:5001
Network access: http://192.168.x.x:5001
Admin password: admin123
```

- On the same machine: open `http://localhost:5001`.
- On other devices on the same LAN/hotspot: open `http://<network-ip>:5001`  
  (the IP shown as “Network access”).

---

## Using the App

1. **Open the URL** (e.g. `http://localhost:5001`).

2. **Choose role**
   - Client: select **Client**, enter name, click **Join**.
   - Admin: select **Admin**, enter name and **admin password**, click **Join**.

3. **Client experience**
   - Sees all announcements in the main panel.
   - Sees no connected‑user list.
   - Cannot send any messages.

4. **Admin experience**
   - Sees the same announcement stream as clients.
   - Sees a **user list** with names and roles.
   - Can type announcements in the admin panel at the bottom and broadcast to everyone.

The server ensures only sockets registered as `admin` can send announcements.

---

## How It Works (High Level)

- When a browser connects, the server:
  - Joins it to an `announcements` room.
  - Sends existing announcement history.

- The browser then sends a `register_user` event with:
  - `name`
  - `role` (`admin` or `client`)
  - `admin_password` (for admin only)

- Server stores users in memory:

```python
users[sid] = {"name": name, "role": role}
```

- Admin only:
  - Can emit `send_announcement`.
  - Server verifies `users[sid]["role"] == "admin"` before broadcasting.

- System join/leave messages:
  - Emitted only to admin sockets, not to clients.

---

## Notes / Limitations

- User list and sessions are stored **in memory**:
  - If the server restarts, connected users and history are reset (unless you add persistence).
- This is designed for **trusted LAN environments**, not for open internet use.
- There is no authentication beyond a shared admin password and names:
  - For stronger security, integrate a proper auth system.

---

## Ideas for Future Improvements

- Persist announcement history to a file or database.
- Add multiple announcement “rooms” or groups.
- Add basic authentication (username/password or one‑time codes).
- Add timestamp and IP details to the admin user list.
- Add mobile‑friendly tweaks to the UI.

---

## License

Add your preferred license here (e.g. MIT):

```text
MIT License

Copyright (c) 2026 <Your Name>
...
```
