import requests as r
import json


class HttpsConfiguration(object):
    def __init__(self, host: str, username: str, password: str, ssl_verify: str | bool, timeout: int):
        self.host = host
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.timeout = timeout


def get_json_response(c: HttpsConfiguration, endpoint: str):
    response = r.get(
        'https://%s/%s' % (c.host, endpoint),
        auth=(c.username, c.password),
        verify=c.ssl_verify,
        timeout=(c.timeout, c.timeout)
    )
    return json.loads(response.text)
