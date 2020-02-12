import base64
from io import BytesIO

from PIL import Image
from pytesseract import image_to_string
from retrying import retry

from core.client import RingClient, retry_to_find_flag

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)


def string_to_image(img_string: str):
    img_data = base64.b64decode(img_string)
    return Image.open(BytesIO(img_data))


def sanitize_image(img: Image):
    sanitize_img = Image.new(mode='RGB', size=img.size)
    data = img.getdata()

    sanitize_data = []
    for pixel in list(data):
        sanitize_data.append(COLOR_BLACK if pixel == COLOR_WHITE else COLOR_WHITE)

    sanitize_img.putdata(sanitize_data)
    return sanitize_img


@retry(
    stop_max_attempt_number=10,
    retry_on_exception=retry_to_find_flag
)
def resolve(client: RingClient):
    print('New try!')
    page = client.get_challenge(challenge=17)
    message = page.find('div', attrs={'class': 'message'})
    img_tag = message.contents[3]

    img = string_to_image(img_string=img_tag.get('src')[22:])
    sanitize_img = sanitize_image(img=img)

    response = image_to_string(sanitize_img)
    print(f'response '.ljust(20, '.') + f' : {response}')

    print(client.send_answer(challenge=17, response=response))


def execute():
    client = RingClient()
    client.login()
    resolve(client=client)


if __name__ == '__main__':
    execute()
