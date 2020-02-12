from os import path

import settings
from core.client import RingClient
from resources import RESOURCE_DIR


def sort_word(word: str) -> str:
    return ''.join(sorted(word.strip()))


def load_words() -> dict:
    with open(path.join(RESOURCE_DIR, 'top-406630-words.txt')) as file:
        return {sort_word(word=w.lower()): w.strip().lower() for w in file.readlines()}


def execute():
    word_refs = load_words()

    print(f'count words refs '.ljust(20, '.') + f' : {len(word_refs)}')

    client = RingClient(challenge=126, cookie=settings.SESSION_ID)
    page = client.get_challenge()
    message = page.find('div', attrs={'class': 'message'})

    words = message.contents[2].strip().split(',')

    print(f'words '.ljust(20, '.') + f' : {", ".join(words)}')
    words_response = []
    for word in words:
        if word not in word_refs.values():
            response = word_refs.get(sort_word(word=word))
            if response:
                print(f'shuffled '.ljust(20, '.') + f' : {word}')
                print(f'response '.ljust(20, '.') + f' : {response}')
                words_response.append(response)
            else:
                print('Fucked! retry...')
                exit()
        else:
            words_response.append(word)

    print(client.send_answer(response=','.join(words_response)))


if __name__ == '__main__':
    execute()
