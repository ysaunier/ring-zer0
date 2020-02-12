import hashlib

from core.client import RingClient


def build_list() -> dict:
    hashes = {}
    for number in range(1000, 9999):
        hashes.update({
            hashlib.sha1(str(number).encode()).hexdigest(): str(number)
        })
    return hashes


def execute():
    hashes = build_list()
    client = RingClient()
    client.login()
    page = client.get_challenge(challenge=56)

    message = page.find('div', attrs={'class': 'message'})
    text = message.contents[2].strip()

    response = hashes.get(text)

    print(client.send_answer(challenge=56, response=response))


if __name__ == '__main__':
    execute()
