import json
import os
from const import DEFAULT_RAWS


def update_or_get_parser_data(
        key: str = None,
        value: str = None,
        get: bool = False,
        delete: bool = False,
        ):
    if not os.path.exists('parser_data.json'):
        with open('parser_data.json', 'w', encoding='utf-8') as json_file:
            parser_data = {
                'titles': [],
                'raws': DEFAULT_RAWS,
                'relations': [],
                'downloads': {},
                'nyaapantsu': [],
                'erai-raws': [],
                'subsplease': [],
                'resolutions': {},
            }
            json.dump(parser_data, json_file, ensure_ascii=False)
    with open('parser_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if get:
        return data
    elif delete:
        if isinstance(data[key], dict):
            del data[key][value]
        elif isinstance(data[key], list):
            for i, j in enumerate(data[key]):
                if j == value:
                    del data[key][i]
    else:
        if value not in data[key]:
            if key == 'relations' and value.split('->')[0] != '':
                data[key].append(value)
                if value.split('->')[0] not in data['titles']:
                    data['titles'].append(value.split('->')[0])
            elif key == 'raws' and value != '':
                data[key].append(value)
            elif key == 'resolutions':
                data[key][value.split('->')[0]] = value.split('->')[1]
            else:
                data[key].append(value)
    with open('parser_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


if __name__ == '__main__':
    pass
