
import datetime
import json
from typing import Dict, Optional, Union
import requests
import os


def create_path_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def get_characteristics(id: Union[str, int]) -> Dict[str, Union[str, Dict[str, str]]]:
    url = f"https://wbx-content-v2.wbstatic.net/ru/{id}.json"
    return requests.get(url).json()


def get_rival_info(id: Union[str, int]) -> Dict[str, str]:
    characteristics = get_characteristics(id)
    result: Dict[str, str] = {'description': characteristics['description']}
    for option in characteristics['options']:
        result[option['name']] = option['value']
    return result


def replace_specific_words_to_bold(words: set, text: str) -> str:
    for word in words:
        text = text.replace(word, f'<b>{word}</b>')
    return text


def get_info(id: Union[str, int]) -> Optional[Dict[str, str]]:
    create_path_if_not_exists('data')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    rival_info = get_rival_info(id)
    with open(f'data/{today}_{id}.json', 'w') as f:
        json.dump(rival_info, f, indent=4, ensure_ascii=False)
    if os.path.exists(f'data/{yesterday}_{id}.json'):
        yesterday_rival_info = json.load(open(f'{yesterday}_{id}.json'))
        result = {}
        for key in rival_info:
            if key == 'description':
                continue
            if rival_info[key] != yesterday_rival_info[key]:
                result[key] = (f'{yesterday_rival_info[key]} ➡️ {rival_info[key]}')
        if rival_info != yesterday_rival_info:
            added = set(rival_info["description"].split(' ')) - \
                set(yesterday_rival_info["description"].split(' '))
            deleted = set(yesterday_rival_info["description"].split(' ')) - \
                set(rival_info["description"].split(' '))

            rival_info['description'] = replace_specific_words_to_bold(added, rival_info['description'])
            yesterday_rival_info['description'] = replace_specific_words_to_bold(
                deleted, yesterday_rival_info['description'])
            result['description'] = rival_info['description']
            result['yesterday_description'] = yesterday_rival_info['description']
            result['difference'] = f"Добавились слова в описание {', '.join(added) }, удалились {', '.join(deleted)}"
            return result
    return None


if __name__ == "__main__":
    pass
