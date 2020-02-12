import settings
from core.client import RingClient


def execute():
    client = RingClient(challenge=57, cookie=settings.SESSION_ID)
    page = client.get_challenge()
    messages = page.findAll('div', attrs={'class': 'message'})

    hash_to_crack = messages[0].contents[2].strip()
    salt = messages[1].contents[2].strip()

    print(f'hash '.ljust(20, '.') + f' : {hash_to_crack}')
    print(f'salt '.ljust(20, '.') + f' : {salt}')

    # response = hashes.get(text)

    # print(client.send_answer(response=response))


if __name__ == '__main__':
    execute()
