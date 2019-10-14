import requests
import json
from time import sleep


# URL API Вконтакте
api_url = 'https://api.vk.com/method/'


def get_friends_ids(token) -> list:
    # Получение списка id всех своих друзей. Полученные данные
    # сохраняются в файл и читаются оттуда при последующих вызовах
    try:
        f = open('friends_ids.json', 'r', encoding='utf-8')
    except IOError:
        params = {'v': '5.52', 'access_token': token}
        answer = requests.get(api_url + 'friends.get', params=params)
        result = json.loads(answer.text)['response']
        with open('friends_ids.json', 'w', encoding='utf-8') as wf:
            json.dump(result, wf, ensure_ascii=False, indent=4)
    else:
        with f:
            result = json.load(f)
    return result['items']


def get_groups_ids(token) -> list:
    # Получение списка id групп всех своих друзей. Полученные данные
    # сохраняются в файл и читаются оттуда при последующих вызовах
    try:
        f = open('my_groups_ids.json', 'r', encoding='utf-8')
    except IOError:
        params = {'v': '5.52', 'access_token': token}
        answer = requests.get(api_url + 'groups.get', params=params)
        result = json.loads(answer.text)['response']
        with open('my_groups_ids.json', 'w', encoding='utf-8') as wf:
            json.dump(result, wf, ensure_ascii=False, indent=4)
    else:
        with f:
            result = json.load(f)
    return result['items']


def get_friends_names(token, f_ids) -> list:
    # Получение списка ФИО всех своих друзей по их id. Полученные данные
    # сохраняются в файл и читаются оттуда при последующих вызовах
    try:
        f = open('friends.json', 'r', encoding='utf-8')
    except IOError:
        params = {'v': '5.52', 'access_token': token}
        persons = []
        friends_cnt = len(f_ids)    # Количество друзей
        # Длина запроса ограничена, поэтому читаем по 100 штук
        for i in range(0, friends_cnt, 100):
            v = 100 if i + 100 < friends_cnt else friends_cnt - i - 1
            params['user_ids'] = ','.join(map(str, f_ids[i:i+v]))
            res = requests.get(api_url + 'users.get', params=params)

            if res.status_code != 200:
                raise RuntimeError(f'HTTP Error: {res.status_code}')

            sleep(.25)  # Without this takes "Too much requests per sec." err
            persons.extend(json.loads(res.text)['response'])
        result = persons
        with open('friends.json', 'w', encoding='utf-8') as wf:
            json.dump(result, wf, ensure_ascii=False, indent=4)
    else:
        with f:
            result = json.load(f)
    return result


def get_friends_groups_ids(token, friends_ids) -> list:
    # Получение списка id всех групп всех своих друзей. Полученные данные
    # сохраняются в файл и читаются оттуда при последующих вызовах
    try:
        f = open('friends_groups_ids.json', 'r', encoding='utf-8')
    except IOError:
        params = {'v': '5.52', 'access_token': token}
        groups = []
        friends_cnt = len(friends_ids)    # Friends count

        print('[' + '*'*31 + 'Чтение списка групп' + '*'*30 + ']\n[', end='')
        errors = 0
        for i in range(friends_cnt):
            params['user_id'] = friends_ids[i]
            res = requests.get(api_url + 'groups.get', params=params)

            if res.status_code != 200:
                raise RuntimeError(f'HTTP Error: {res.status_code}')

            sleep(.25)  # Without this takes "Too much requests per sec." err
            if (i * 80 // friends_cnt) != ((i+1) * 80 // friends_cnt):
                print('*', end='')

            answer_json = json.loads(res.text)
            if 'error' in answer_json:
                errors += 1
            else:
                groups.append(answer_json['response']['items'])

        print(f']\n Success: {friends_cnt - errors}, Errors: {errors}')
        result = groups

        with open('friends_groups_ids.json', 'w', encoding='utf-8') as wf:
            json.dump(result, wf, ensure_ascii=False, indent=4)
    else:
        with f:
            result = json.load(f)
    return result


def get_groups_names(token, groups_ids) -> dict:
    # Получение списка названий групп по списку их id. Полученные данные
    # сохраняются в файл и читаются оттуда при последующих вызовах
    try:
        f = open('groups_names.json', 'r', encoding='utf-8')
    except IOError:
        params = {'v': '5.52', 'access_token': token}
        group_names = {}
        groups_cnt = len(groups_ids)    # Friends count
        print('[' + '*'*29 + 'Чтение названий групп' + '*'*30 + ']\n[', end='')
        errors = 0
        for i in range(0, groups_cnt, 100):
            v = 100 if i + 100 < groups_cnt else groups_cnt - i - 1
            params['group_ids'] = ','.join(map(str, groups_ids[i:i+v]))
            res = requests.get(api_url + 'groups.getById', params=params)

            if res.status_code != 200:
                raise RuntimeError(f'HTTP Error: {res.status_code}')

            sleep(.25)  # Without this takes "Too much requests per sec." err
            if (i * 80 // groups_cnt) != ((i+100) * 80 // groups_cnt):
                print('*', end='')

            answer_json = json.loads(res.text)
            if 'error' in answer_json:
                errors += 1
            else:
                groups_subset = {}
                for group in answer_json['response']:
                    groups_subset[group['id']] = group['name']

                group_names.update(groups_subset)

        print(f']\n Success: {groups_cnt - errors}, Errors: {errors}')
        result = group_names
        with open('groups_names.json', 'w', encoding='utf-8') as wf:
            json.dump(result, wf, ensure_ascii=False, indent=4)
    else:
        with f:
            result = json.load(f)
    return result
