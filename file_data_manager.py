import parser
import json
import os



with open("DATA/config.json", encoding='utf-8') as file:
    config_data = json.load(file)

# print(config_data)


commands_functions = tuple(i for i in config_data['commands']
                           if config_data['commands'][i]['response_type'] == 'function')
commands_random = tuple(i for i in config_data['commands']
                        if config_data['commands'][i]['response_type'] == 'random')
functions = (parser.parse_films, parser.parse_games)
commands_functions_dict = dict(zip(commands_functions, functions))


def isRegistrated() -> bool:
    if os.path.exists("DATA/user1.txt"):
        return True
    else:
        return False


def register(name: str, age: int, password: str):
    try:
        if not isRegistrated():
            with open('DATA/user1.txt', 'w', encoding='utf-8') as file:
                # json_file = json.load(file)
                new_user_info = f"{name}, {age}, {password}"
                file.write(new_user_info)
        return name, age, password
    except:
        print('Ошибка файла')


def get_user_info():
    if isRegistrated():
        with open('DATA/user1.txt', 'r', encoding='utf-8') as file:
            user_info = file.read().split(', ')
        return user_info


def save_information(name, age, keyword):
    with open('DATA/user1.txt', 'w') as file:
        file.write("{name:" + f"{name}," +
                   "age:" + f"{age}," +
                    "keyword:" + f"{keyword}"
                   "}")



