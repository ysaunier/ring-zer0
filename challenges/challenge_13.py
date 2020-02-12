import hashlib

import settings
from core.client import RingClient


def execute():
    client = RingClient(challenge=13, cookie=settings.SESSION_ID)
    page = client.get_challenge()

    message = page.find('div', attrs={'class': 'message'})
    text = message.contents[2].strip()

    response = hashlib.sha512(text.encode()).hexdigest()

    print(client.send_answer(response=response))


if __name__ == '__main__':
    execute()
