import requests
from task.checkin import Checkin


class Sockboom(Checkin):
    BASE_URL = "https://sockboom.com"

    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.common_headers = {
            "Origin": Sockboom.BASE_URL,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.session = requests.session()

    def _login(self):
        login_url = f"{self.BASE_URL}/auth/login"
        headers = {"Referer": f"{self.BASE_URL}/auth/login", **self.common_headers}
        data = {"email": self.email, "passwd": self.passwd, "code": ""}

        login_response = self.session.post(login_url, headers=headers, data=data)
        login_response_body = login_response.json()

        return login_response_body['user']

    def _logout(self):
        checkin_url = f"{self.BASE_URL}/user/logout"
        headers = {"Referer": f"{self.BASE_URL}/user", **self.common_headers}
        self.session.get(checkin_url, headers=headers)

    def _checkin(self):
        checkin_url = f"{self.BASE_URL}/user/checkin"
        headers = {"Referer": f"{self.BASE_URL}/user", **self.common_headers}

        login_response = self.session.post(checkin_url, headers=headers)
        login_response_body = login_response.json()
        return login_response_body['msg']

    def checkin(self):
        print("sockboom 签到开始...")

        username = self._login()
        msg = self._checkin()
        self._logout()

        print("sockboom 签到成功")

        return f"sockboom[{self.BASE_URL}]: {username} {msg}"
