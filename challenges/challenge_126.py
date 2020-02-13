from os import path

from retrying import retry

from core.client import RingClient, retry_to_find_flag
from resources import RESOURCE_DIR


def sort_word(word: str) -> str:
    return ''.join(sorted(word.strip()))


def load_words() -> dict:
    with open(path.join(RESOURCE_DIR, 'top-406630-words.txt')) as file:
        words = file.readlines()
        values = {w.strip().lower(): True for w in words}
        dictionary = {sort_word(word=w.lower()): w.strip().lower() for w in words}
        return values, dictionary


@retry(
    stop_max_attempt_number=10,
    retry_on_exception=retry_to_find_flag
)
def resolve(client: RingClient, values: dict, dictionary: dict):
    page = client.get_challenge(challenge=126)
    message = page.find('div', attrs={'class': 'message'})

    words = message.contents[2].strip().split(',')

    print('New try!')
    print(f'resolve words '.ljust(20, '.') + f' : {", ".join(words)}')
    words_response = []
    for word in words:
        if not values.get(word.strip().lower()):
            response = dictionary.get(sort_word(word=word))
            if response:
                print(f'* shuffled '.ljust(20, '.') + f' : {word}')
                print(f'* response '.ljust(20, '.') + f' : {response}')
                words_response.append(response)
            else:
                print('Fucked! retry...')
                exit()
        else:
            words_response.append(word)

    print()
    answer = ','.join(words_response)

    print(client.send_answer(challenge=126, response=answer))


def execute():
    values, dictionary = load_words()
    print(f'count words refs '.ljust(20, '.') + f' : {len(values)}\n')

    client = RingClient()
    client.login()

    resolve(client=client, values=values, dictionary=dictionary)


if __name__ == '__main__':
    execute()
