import re

import requests
from bs4 import BeautifulSoup, PageElement


class FlagNotFound(Exception):
    def __init__(self, html: str, message):
        self.html = html
        super().__init__(message)


class NotConnected(Exception):
    pass


def retry_to_find_flag(exception):
    return isinstance(exception, FlagNotFound)


class RingClient:

    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def get_div_by_class(soup, style_class: str):
        try:
            return soup.find('div', attrs={'class': style_class}).string
        except AttributeError as e:
            return None

    @staticmethod
    def _raise_for_login(response):
        if response.request.url[-5:] == 'login':
            raise NotConnected()

    def _response_to_soup(self, url: str):
        response = self.session.get(url)
        response.raise_for_status()
        self._raise_for_login(response=response)
        return BeautifulSoup(response.content, 'html5lib')

    def login(self):
        import settings
        response = requests.post('https://ringzer0ctf.com/login', data={
            'username': settings.RING_USERNAME,
            'password': settings.RING_PASSWORD,
        })
        response.raise_for_status()
        cookie = response.request.headers.get('Cookie')[10:]
        self.session.headers.update({'cookie': f'PHPSESSID={cookie}'})

    def get_challenge(self, challenge: int) -> PageElement:
        soup = self._response_to_soup(url=f'https://ringzer0ctf.com/challenges/{challenge}')
        return soup.find('div', attrs={'class': 'challenge-wrapper'})

    def send_answer(self, challenge: int, response):
        soup = self._response_to_soup(url=f'https://ringzer0ctf.com/challenges/{challenge}/{response}')

        flag = self.get_div_by_class(soup=soup, style_class='alert alert-info')
        if not flag:
            m = re.search(pattern=r'(FLAG-[A-Za-z0-9]+)', string=soup.prettify(), flags=re.MULTILINE)
            flag = m.group(1) if m else None

        if flag:
            return flag

        raise FlagNotFound(
            html=soup.prettify(),
            message=self.get_div_by_class(soup=soup, style_class='alert alert-danger')
        )
