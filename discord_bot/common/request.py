import requests

from discord_bot.common.exceptions import TooManyRequests
from exceptions import CODE_TO_EXCEPTION


class Request(object):
    def __init__(self, token, url, method, json_data=None, headers=None):
        self.token = token
        self.url = url
        self.method = method
        self.json_data = json_data
        self.headers = headers

    @staticmethod
    def get_response_data(response):
        json_data = {}
        if response.content:
            json_data = response.json()
        if "code" in json_data and "message" in json_data:
            message = json_data["message"]
            code = json_data["code"]
            exception = CODE_TO_EXCEPTION.get(code)
            if exception:
                raise exception(f"{code}: {message}")
            else:
                raise Exception(f"{code}: {message}")
        return json_data

    def execute(self):
        headers = {"Authorization": f"{self.token}"}
        if self.headers:
            headers.update(self.headers)

        response = requests.request(method=self.method, url=self.url, headers=headers, json=self.json_data, timeout=10)
        if response.status_code == 429:
            response_json = response.json()
            raise TooManyRequests(response_json=response_json, url=self.url)
        return self.get_response_data(response)
