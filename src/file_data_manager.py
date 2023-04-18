from src import parser
import json
import os


class DataMixin:
    DATA_DIR: str = os.getcwd().replace('src', '').replace('windows', '') + r"\DATA\\"
    print(DATA_DIR)
    RESPONSE_FORMAT: str = ".mp3"
    RESPONSE_FILE_NAME: str = "response" + RESPONSE_FORMAT


class UsersManager(DataMixin):
    def __init__(self, filepath: str = None):
        if filepath is None:
            self.__filepath = self.DATA_DIR
        else:
            self.__filepath = filepath
        self._amount_of_users = len(self.get_users_info())

    def get_user_info(self, number: int) -> list:
        if self.is_any_registered():
            with open(f'{self.DATA_DIR}users.txt', 'r', encoding='utf-8') as file:
                users_info = file.readlines()
                user_required_indo = users_info[number - 1].strip().split()
                return user_required_indo
        return []

    def get_users_info(self) -> list:
        if self.is_any_registered():
            with open(f'{self.DATA_DIR}users.txt', "r", encoding="utf-8") as file:
                users_info = [i for i in file]
            return users_info
        return []

    def save_information(self, name: str,
                         age: int,
                         keyword: str) -> None:
        """Сохранение информации в файл"""
        self._amount_of_users += 1
        with open(f'{self.DATA_DIR}users.txt', 'a+', encoding="utf-8") as file:
            file.write(f"{name} {age} {keyword}\n")

    def is_any_registered(self) -> bool:
        return os.path.exists(f"{self.DATA_DIR}users.txt")


class AssistantManager(UsersManager):
    def __init__(self):
        # менеджер пользователей
        super().__init__()
        # self.__userManager = UsersManager()
        # данные для ассистента
        self.config_data = self.loadData()
        self.commands_data = self.config_data['commands']
        self.commands_functions = tuple(i for i in self.commands_data
                                   if self.commands_data[i]['response_type'] == 'function')
        self.commands_random = tuple(i for i in self.commands_data
                                if self.commands_data[i]['response_type'] == 'random')
        functions = (parser.parse_films, parser.parse_games)
        self.commands_functions_dict = dict(zip(self.commands_functions, functions))
        self.modes_triggers_data = self.config_data['modes']['triggers']
        self.modes_list_data = self.config_data['modes']['list_modes']

    def loadData(self) -> dict:
        with open(f"{self.DATA_DIR}config.json", encoding='utf-8') as file:
            config_data = json.load(file)
        return config_data

    def safe_delete_response(self, func):
        def wrapper(self, *args, **kwargs):
            if os.path.exists(self.DATA_DIR + self.RESPONSE_FILE_NAME):
                os.remove(self.DATA_DIR + self.RESPONSE_FILE_NAME)
            return func(self, *args, **kwargs)

        self.delete_response()
        return wrapper

    def delete_response(self):
        """Удаление ответа ассистента"""
        if os.path.exists(self.DATA_DIR + self.RESPONSE_FILE_NAME):
            os.remove(self.DATA_DIR + self.RESPONSE_FILE_NAME)


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
