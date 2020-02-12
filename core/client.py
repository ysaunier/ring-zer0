import re

import requests
from bs4 import BeautifulSoup, PageElement



class FlagNotFound(Exception):
    def __init__(self, html: str, message):
        self.html = html
        super().__init__(message)


# text = html_to_text(html=response.text)
# m = re.search(pattern=r'(FLAG-[A-Za-z0-9]+)', string=text, flags=re.MULTILINE)

class RingClient:
    def __init__(self, challenge: int, cookie: str):
        self.challenge = challenge
        self.url = f'https://ringzer0ctf.com/challenges/{challenge}'
        self.session = requests.Session()
        self.session.headers.update({'cookie': f'PHPSESSID={cookie}'})

    @staticmethod
    def get_div_by_class(soup, style_class: str):
        try:
            return soup.find('div', attrs={'class': style_class}).string
        except AttributeError as e:
            return None

    def get_challenge(self) -> PageElement:
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find('div', attrs={'class': 'challenge-wrapper'})

    def send_answer(self, response):
        response = self.session.get(f'{self.url}/{response}')
        soup = BeautifulSoup(response.content, 'html5lib')

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
