
# 📡 FreePBX Realtime Dashboard & CDR Viewer

A powerful web dashboard for real-time monitoring of active channels and call history (CDRs) on **FreePBX/Asterisk-based PBX systems**. Built with Flask + SocketIO + BeautifulSoup for secure, browser-based access.

---

## ⚙️ Key Features

✅ **Live Channel Status**  
Monitor active calls with real-time data fetched from `core show channels verbose`.

📑 **Call Detail Records (CDR)**  
Fetch and parse historical call records using POST form scraping and BeautifulSoup.

🔐 **Admin Authentication**  
Simple built-in login system using Flask sessions.

💾 **Session Cookie Handling**  
Automatically logs in and stores PHPSESSID cookie for future requests.

🧠 **Modular Architecture**  
Clean code separation for login, stats fetching, cookie handling, and HTML parsing.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ashrafiabir01/freepbx-monitor.git
cd freepbx-monitor
````

### 2. Install Requirements

```bash
pip install flask flask-socketio flask-session requests beautifulsoup4
```

### 3. Configuration Files

* `host.txt`
  → Add your FreePBX host/IP (e.g., `192.168.0.100`)

* `usernamepass.txt`
  → Format: `admin:yourFreePBXpassword`

These are used for automatic login and cookie/session handling.

---

## 🖥️ Running the App

```bash
python app.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

## 📂 File Structure

```
├── app.py                 # Main Flask + SocketIO app
├── host.txt               # Stores FreePBX host/IP
├── usernamepass.txt       # Login credentials (username:password)
├── cookie.txt             # Saved PHP session cookie
├── templates/
│   ├── index.html         # Login page
│   └── stats.html         # Dashboard page
```

---

## 🧪 Core Functions Explained

### `login_pbx()`

* Logs into FreePBX admin interface
* Extracts and stores `PHPSESSID` for future API usage

### `get_stats()`

* Uses Asterisk CLI via AJAX (`core show channels verbose`)
* Returns live channel info (used in WebSocket updates)

### `get_cdr()`

* Sends a POST request to the CDR page
* Parses HTML using BeautifulSoup to extract call records
* Cleans output to remove audio-player and empty rows

---

## 🔐 Security Note

This project is intended for **internal/admin use only**. Please:

* Deploy behind a firewall or VPN
* Change the login credentials (`app.py`)
* Avoid exposing this on public networks

---

## 📚 Future Ideas

* Dynamic date range picker for CDR queries
* Downloadable CSV for call logs
* User roles & access control
* Filter/search by number or disposition

---

## 👨‍💻 Author

**Ashrafi Khandaker Abir**
🔗 [https://devabir.com](https://devabir.com)

---

## 📜 License

This project is open-source and free to use under the MIT License.

---

> Monitor your PBX like a pro — no SSH or terminal needed.

```

---

Let me know if you want:

- GitHub badge section (e.g. build passing, python version)
- Docker support instructions
- HTML templates (`index.html`, `stats.html`)
- Live hosted preview badge (via ngrok or render)

I can tailor it for anything you need.
```
