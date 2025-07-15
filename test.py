import requests


def login_pbx():
    url = "http://20.227.162.30:80/admin/config.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://20.227.162.30/admin/config.php",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://20.227.162.30",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # Send a GET request to retrieve the PHPSESSID cookie
        response = requests.get(url, headers=headers)
        cookies = response.cookies

        # Add the PHPSESSID cookie to the headers
        headers["Cookie"] = "PHPSESSID=" + cookies["PHPSESSID"]

        # Form data to be sent in the POST request
        username = open('usernamepass.txt').read().replace(
            "\n", '').split(":")[0]
        password = open('usernamepass.txt').read().replace(
            "\n", '').split(":")[1]
        data = {
            "username": f"{username}",
            "password": f"{password}"
        }

        # Send the POST request with the form data and headers
        response = requests.post(url, headers=headers, data=data)
        if "Welcome to FreePBX" in response.text:
            print("Login success")
            print(cookies["PHPSESSID"])
            with open("cookie.txt", 'w') as w:
                w.write(str(cookies["PHPSESSID"]))
                w.close()

        else:
            print("Login Failed")

    except Exception as e:
        print("An error occurred:", e)


login_pbx()
