import settings
from core.client import RingClient


def decode_binary_string(text) -> str:
    return ''.join(chr(int(text[i * 8:i * 8 + 8], 2)) for i in range(len(text) // 8))


def execute():
    client = RingClient()
    client.login()
    page = client.get_challenge(challenge=17)

    message = page.find('div', attrs={'class': 'message'})
    image_tag = message.contents[3]

    print(image_tag.get('src'))
    # response = hashlib.sha512(decode_binary_string(text=text).encode()).hexdigest()

    # print(client.send_answer(response=response))


if __name__ == '__main__':
    execute()
