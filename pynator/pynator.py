import requests
import urllib.parse

from typing import List, Dict


class _Message:
    def __init__(self, message_id: str, author: str, text: str, time: str):
        self.message_id = message_id
        self.author = author
        self._text = text
        self.time = time

    def __str__(self) -> str:
        return f"{self.author} - {self._text} - {self.time}"

    def __repr__(self) -> str:
        return f"{self.author} - {self._text} - {self.time}"


class Email(_Message):
    def __init__(self, message_id: str, author: str, subject: str, time: str):
        super().__init__(message_id, author, subject, time)
        self.subject = subject


class SMS(_Message):
    def __init__(self, message_id: str, author: str, message: str, time: str):
        super().__init__(message_id, author, message, time)
        self.message = message


class _Nator:
    def __init__(self, base_url: str, inbox_type: str):
        self.url = base_url
        self.inbox_type = inbox_type

        self.session = requests.Session()
        response = self.session.get(self.url)
        response.raise_for_status()
        self.session.headers.update(
            {
                "x-xsrf-token": urllib.parse.unquote(
                    self.session.cookies.get_dict()["XSRF-TOKEN"]
                )
            }
        )

    def _request(self, endpoint: str, json_data: Dict) -> Dict:
        response = self.session.post(
            self.url + endpoint,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()

    def _generate(self, options: List[str], user_options: List[str] = None) -> Dict:
        if user_options:
            if not isinstance(user_options, list):
                raise TypeError("Options must be a list of strings")

            if not all(option in options for option in user_options):
                raise ValueError(
                    f"Invalid options: {user_options}. Valid options: {options}"
                )

            options = user_options

        json_data = {self.inbox_type: options}
        return self._request(f"generate-{self.inbox_type}", json_data)

    def _messages_list(self, inbox: str) -> List[Dict]:
        json_data = {self.inbox_type: inbox}

        response = self._request("message-list", json_data)
        if "messageData" not in response:
            return response

        return response["messageData"]


class EmailNator(_Nator):
    def __init__(self):
        super().__init__("https://www.emailnator.com/", "email")

    def generate_email(self, options: List[str] = None) -> str:
        response = self._generate(
            ["domain", "plusGmail", "dotGmail", "googleMail"], options
        )
        return response["email"][0]

    def get_messages(self, email: str) -> List[Email]:
        messages = self._messages_list(email)
        return [
            Email(
                message["messageID"],
                message["from"],
                message["subject"],
                message["time"],
            )
            for message in messages
            if message["messageID"] != "ADSVPN"
        ]

    def get_message(self, email: str, message_id: str) -> str:
        json_data = {"email": email, "messageID": message_id}
        response = self.session.post(self.url + "message-list", json=json_data)
        response.raise_for_status()
        return response.text


class SMSNator(_Nator):
    def __init__(self):
        super().__init__("https://smsnator.online/", "number")

    def generate_number(self, options: List[str] = None) -> str:
        response = self._generate(["SE", "GB", "FR", "FI", "DK", "BE"], options)
        return response["number"]

    def get_messages(self, number: str) -> List[SMS]:
        messages = self._messages_list(number)
        return [
            SMS(
                message["messageID"],
                message["from"],
                message["message"],
                message["time"],
            )
            for message in messages
            if message["messageID"] != "ADSVPN"
        ]
