import requests
import random
import json
from hashlib import md5

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


def set_key(appid, appkey, config):
    config['appid'] = appid
    config['appkey'] = appkey
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False)


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def display_language_table():
    with open('lang_tb', 'r', encoding='utf-8') as file:
        lang_tb = file.read()
    print(lang_tb)


def set_language(*args):
    langs = args[0].split('-')
    if len(langs) != 2:
        print('Invalid Languages! Please Try Again!')
    else:
        config["from_lang"] = langs[0]
        config['to_lang'] = langs[1]
        with open('config.json', 'w') as file:
            json.dump(config, file, ensure_ascii=False)


def display_history():
    with open('history.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
    for his in history["history"]:
        fromLang = his['from']
        toLang = his['to']
        origin = his["trans_result"][0]['src']
        trans = his["trans_result"][0]['dst']
        print(f'From:\33[35m{fromLang}\33[0m')
        print(f'To:\33[36m{toLang}\33[0m')
        print(f'Origin:\33[32m{origin}\33[0m')
        print(f'Translation:\33[34m{trans}\33[0m')
        print('\n')


def clear_history():
    with open('history.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
        history["history"].clear()

    with open('history.json', 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

    print('\33[32mHistory has been cleared!\33[0m')


hashed_function = {
    "lang": set_language,
    "langtb": display_language_table,

    "disp": display_history,
    "clr": clear_history,

}

if __name__ == '__main__':
    # print welcome
    with open('welcome', 'r') as file:
        welcome = file.read()
    print(welcome)

    while True:
        # load config
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)

        # check whether there is a appid&appkey
        if len(config['appid']) == 0 or len(config['appkey']) == 0:
            appid = input("> Please input your appid below:\n> ")
            appkey = input("> Please input your appkey below:\n> ")
            set_key(appid, appkey, config)
            with open('config.json', 'r', encoding='utf-8') as file:
                config = json.load(file)
            print("> \33[32mSet Key Success!\33[0m")

        query = input("> ")
        if query[0] == '@':
            cmd = query[1:].split()
            if cmd[0]=='exit':
                break
            try:
                hashed_function[cmd[0]](*cmd[1:])
            except:
                print('\033[0;31;40mNot supported function! Please try again!\033[0m')
        else:
            salt = random.randint(32768, 65536)
            sign = make_md5(config['appid'] + query +
                            str(salt) + config['appkey'])
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': config['appid'], 'q': query, 'from': config['from_lang'],
                       'to': config['to_lang'], 'salt': salt, 'sign': sign}

            try:
                r = requests.post(url, params=payload, headers=headers)
                result = r.json()
            except:
                print("\033[0;31;40mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

            try:
                fromLang = result['from']
                toLang = result['to']
                trans = result["trans_result"][0]['dst']
                print(f'From:\33[35m{fromLang}\33[0m')
                print(f'To:\33[36m{toLang}\33[0m')
                print(f'Translation:\33[32m{trans}\33[0m')

                with open("history.json", "r+", encoding="utf-8") as file:
                    history = json.load(file)
                    history['history'].append(result)
                    file.seek(0)
                    json.dump(history, file, indent=4, ensure_ascii=False)
            except:
                print('\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')
