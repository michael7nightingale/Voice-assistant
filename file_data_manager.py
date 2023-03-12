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
amount_of_users = 0


def is_any_registrated() -> bool:
    if os.path.exists("DATA/users.txt"):
        return True
    else:
        return False


# def register(name: str, age: int, password: str):
#     try:
#         if not isRegistrated():
#             with open('DATA/users.txt', 'w', encoding='utf-8') as file:
#                 # json_file = json.load(file)
#                 new_user_info = f"{name}, {age}, {password}"
#                 file.write(new_user_info)
#         return name, age, password
#     except:
#         print('Ошибка файла')


def get_user_info(number: int):
    with open(f'DATA/users.txt', 'r', encoding='utf-8') as file:
        users_info = file.readlines()
        user_required_indo = users_info[number - 1].strip().split()
        return user_required_indo
    return False


def get_users_info() -> list:
    with open('DATA/users.txt', "r", encoding="utf-8") as file:
        users_info = [i for i in file]
    return users_info


def save_information(name, age, keyword):
    global amount_of_users
    amount_of_users += 1
    with open('DATA/users.txt', 'a+', encoding="utf-8") as file:
        file.write(f"{name} {age} {keyword}\n")




