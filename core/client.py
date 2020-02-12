import requests
from bs4 import BeautifulSoup, PageElement


class RingClient:
    def __init__(self, challenge: int, cookie: str):
        self.challenge = challenge
        self.url = f'https://ringzer0ctf.com/challenges/{challenge}'
        self.session = requests.Session()
        self.session.headers.update({'cookie': f'PHPSESSID={cookie}'})

    def get_challenge(self) -> PageElement:
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find('div', attrs={'class': 'challenge-wrapper'})

    def send_answer(self, response):
        response = self.session.get(f'{self.url}/{response}')
        soup = BeautifulSoup(response.content, 'html5lib')
        try:
            return soup.find('div', attrs={'class': 'alert alert-info'}).string
        except AttributeError:
            return soup.prettify()
