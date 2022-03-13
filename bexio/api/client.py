import requests

from json.decoder import JSONDecodeError
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .exceptions import BexioAPIError

from .. import config


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def raise_api_error(response):
    try:
        body = response.json()
    except JSONDecodeError:
        error = response.reason
    else:
        if isinstance(body, list):
            error = str(body)
        else:
            error = body.get('detail', f'{response.reason} {response.text}')
    url = f'{response.request.method} {response.request.url}'
    raise BexioAPIError(
        message=error,
        url=url,
        status_code=response.status_code)


class APIClient:

    def __init__(self):
        self.session = requests_retry_session()

    def __default_headers(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        if config.api_token:
            headers['authorization'] = 'Bearer {}'.format(config.api_token)
        return headers

    def __url(self, path):
        return urljoin(config.api_host, path)

    def __request(self, method, path, data=None, params=None):
        headers = self.__default_headers()
        response = self.session.request(
            method,
            self.__url(path),
            headers=headers,
            params=params,
            json=data)
        if not response.ok:
            raise_api_error(response)
        return response

    def get(self, path, params=None):
        return self.__request('GET', path, params=params)

    def put(self, path, data=None, params=None):
        return self.__request('PUT', path, data=data, params=params)

    def post(self, path, data=None, params=None, files=None):
        return self.__request('POST', path, data=data, params=params, files=files)

    def delete(self, path):
        return self.__request('DELETE', path)
