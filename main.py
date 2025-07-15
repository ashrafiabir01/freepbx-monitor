from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import json
import time
from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, emit
import requests
import json
import time
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "my_ca_secret_key_1234"
socketio = SocketIO(app)
from bs4 import BeautifulSoup
import requests


def read_cookie():
    with open("cookie.txt", "r") as f:
        cookie = f.read().strip()
        f.close()
    return cookie


def read_host():
    with open("host.txt", "r") as f:
        host = f.read().strip()
        f.close()
    return host


def get_cdr():
    try:
        host = read_host()
        cookie = read_cookie()

        burp0_url = f"http://{host}/admin/config.php?display=cdr"
        burp0_cookies = {
            "lang": "en_US",
            "searchHide": "1",
            "PHPSESSID": f"{cookie}",
        }
        burp0_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://20.227.162.30/admin/config.php?display=cdr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://20.227.162.30",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
        }
        burp0_data = {
            "order": "calldate",
            "startday": "01",
            "startmonth": "02",
            "startyear": "2023",
            "starthour": "00",
            "startmin": "00",
            "endday": "31",
            "endmonth": "02",
            "endyear": "2023",
            "endhour": "23",
            "endmin": "59",
            "need_html": "true",
            "limit": "100",
            "cnum": "",
            "cnum_mod": "begins_with",
            "cnam": "",
            "cnam_mod": "begins_with",
            "outbound_cnum": "",
            "outbound_cnum_mod": "begins_with",
            "did": "",
            "did_mod": "begins_with",
            "dst": "",
            "dst_mod": "begins_with",
            "dst_cnam": "",
            "dst_cnam_mod": "begins_with",
            "userfield": "",
            "userfield_mod": "begins_with",
            "accountcode": "",
            "accountcode_mod": "begins_with",
            "dur_min": "",
            "dur_max": "",
            "disposition": "all",
            "sort": "DESC",
            "group": "day",
        }

        data_text = requests.post(
            burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
        ).text

        soup = BeautifulSoup(data_text, "html.parser")

        # Find the table element
        table = soup.find("table", {"id": "cdr_table"})

        # Find all rows in the table
        rows = table.find_all("tr")

        # Extract the data from the rows
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            if len(cols) != 0:
                data.append(cols)

        # Print the extracted data
        data_list_all = []
        for i in data:
            if r"You are missing support for playback in this browser." not in str(i):

                data_list = [s for s in list(i) if s]
                data_list_all.append(data_list)
        return data_list_all
    except Exception as e:
        print(e)
        pass


def read_host():
    with open("host.txt", "r") as f:
        host = f.read().strip()
        f.close()
    return host


def login_pbx():
    host = read_host()
    url = f"http://{host}/admin/config.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"http://{host}/admin/config.php",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{host}",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # Send a GET request to retrieve the PHPSESSID cookie
        response = requests.get(url, headers=headers)
        cookies = response.cookies

        # Add the PHPSESSID cookie to the headers
        headers["Cookie"] = "PHPSESSID=" + cookies["PHPSESSID"]

        # Form data to be sent in the POST request
        username = open("usernamepass.txt").read().replace("\n", "").split(":")[0]
        password = open("usernamepass.txt").read().replace("\n", "").split(":")[1]
        data = {"username": f"{username}", "password": f"{password}"}

        # Send the POST request with the form data and headers
        response = requests.post(url, headers=headers, data=data)
        if "Welcome to FreePBX" in response.text:
            print("Login success")
            print(cookies["PHPSESSID"])
            with open("cookie.txt", "w") as w:
                w.write(str(cookies["PHPSESSID"]))
                w.close()

        else:
            print("Login Failed")

    except Exception as e:
        print("An error occurred:", e)


def read_cookie():
    with open("cookie.txt", "r") as f:
        cookie = f.read().strip()
        f.close()
    return cookie


def get_stats():
    host = read_host()
    cookie = read_cookie()
    url = f"http://{host}/admin/ajax.php?module=asterisk-cli&command=clicmd&data=core%20show%20channels%20verbose"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"http://{host}/admin/config.php?display=cli",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "close",
        "Cookie": f"PHPSESSID={cookie}",
    }

    response = requests.get(url, headers=headers)
    message = (response.json())["message"].replace("\\n", "<br>").replace("\\", " \ ")

    return message


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("stats"))
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    if (
        request.form["username"] == "admin"
        and request.form["password"] == "Calltower1!"
    ):
        session["username"] = request.form["username"]
        return redirect(url_for("stats"))
    return "Invalid username/password combination"


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/freepbx/channels")
def stats():
    if "username" not in session:
        return redirect(url_for("index"))
    login_pbx()
    response = get_stats()
    return render_template("stats.html", response=response)


@socketio.on("get_data")
def handle_get_data():
    response = get_stats()
    emit("update_data", response)


if __name__ == "__main__":
    socketio.run(app, debug=True)
