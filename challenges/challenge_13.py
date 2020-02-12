import hashlib

from core.client import RingClient


def execute():
    client = RingClient()
    client.login()
    page = client.get_challenge(challenge=13)

    message = page.find('div', attrs={'class': 'message'})
    text = message.contents[2].strip()

    response = hashlib.sha512(text.encode()).hexdigest()

    print(client.send_answer(challenge=13, response=response))


if __name__ == '__main__':
    execute()
