# LAN Announcements App

This is a simple **LAN announcement board**.

- One person is **Admin** (can send announcements and see who is connected).
- Everyone else is a **Client** (can only read announcements).
- Works on a local network or mobile hotspot.

---

## 1. What you need

- Python 3 installed
- A web browser (Chrome, Edge, etc.)

---

## 2. Download the project

1. Click the green **Code** button on this GitHub page.
2. Choose **Download ZIP**.
3. Unzip the file.
4. Open a terminal / PowerShell inside the project folder.

---

## 3. Install Python packages

In the project folder, run:

```bash
pip install flask flask-socketio
```

---

## 4. Add Socket.IO client file

The browser needs a Socket.IO client JS file.

1. Download this file:  
   https://cdn.jsdelivr.net/npm/socket.io-client@4.7.5/dist/socket.io.min.js [web:46]

2. Save it as:

```text
static/socket.io.min.js
```

Your folder should look like:

```text
project-folder/
├─ server.py
├─ static/
│   └─ socket.io.min.js
└─ templates/
    └─ index.html
```

---

## 5. Set admin password (optional)

Open `server.py` and find:

```python
ADMIN_PASSWORD = "admin123"
```

Change `"admin123"` to any password you want.

---

## 6. Run the server

In the project folder, run:

```bash
python server.py
```

You will see something like:

```text
Local access  : http://localhost:5001
Network access: http://192.168.x.x:5001
Admin password: admin123
```

- On the same PC: open `http://localhost:5001`.
- On another device on the same Wi‑Fi / hotspot: open the **Network access** URL.

---

## 7. How to use (Client vs Admin)

### Client

1. In the page header:
   - Role: **Client**
   - Enter your **name**
   - Leave password empty
   - Click **Join**
2. You will see all announcements from the admin.
3. You **cannot** send messages.

### Admin

1. In the page header:
   - Role: **Admin**
   - Enter your **name**
   - Enter the **admin password** (from `server.py`)
   - Click **Join**
2. At the bottom:
   - You will see an **Admin panel** to type announcements.
   - You will see a **Connected users** list.
3. Type an announcement and click **Send announcement**.
4. All clients see it instantly.

---

## 8. Stopping the app

- In the terminal where `server.py` is running, press `Ctrl + C`.

That’s it. Anyone can download the repo, install packages, add `socket.io.min.js`, run `server.py`, and use the app as admin or client.
