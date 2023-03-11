"""
Логика голосового ассистента.
Выступает в роли независимого-класса.
Реализован паттерн Моносостояние
"""
import speech_recognition
import speech_recognition as sr
import os
from gtts import gTTS
import random
import file_data_manager as FDM
from playsound import playsound     # для воспроизведения звука
from observer import Subject        # импорт наблюдаемого класса


class Assistant(Subject):
    """Класс голосового помощника"""
    def __new__(cls, *args, **kwargs):  # элементарный конструктор класса
        if not hasattr(cls, 'instance'):    # Синглтон
            cls.instance = super().__new__(cls)
        return cls.instance

    # Моносостояние
    MONOCONDITIONAL_DATA = {
        'recognizer': sr.Recognizer(),
        'data': FDM.config_data,
        'threadAwait_flag': False
    }

    def __init__(self):    # элементарный инициализатор класса
        self.__dict__ = self.MONOCONDITIONAL_DATA
        super().__init__()
        self.phrases = []
        self.source = sr.Microphone(device_index=1)

    def execute(self):
        if not FDM.isRegistrated():
            self.name, self.age, self.keyword = self.register()
        else:
            self.name, self.age, self.keyword = FDM.get_user_info()
        # self.name = 'Михаил'
        self.answer(f"Привет, {self.name}", continue_target='commands')


    def askWhileFalse(self, text_to_reanswer: str, text_to_answer_finally: str, type_: str):
        """Функция для переспрашивания, пока не истинно условие"""
        try:
            try_phrase = self.listen_service(phrase_to_reanswer=text_to_reanswer)
            print(try_phrase)
            if validDate(type_, try_phrase):
                self.answer(continue_target='service', response=text_to_answer_finally)
                return try_phrase

            return self.askWhileFalse(type_, text_to_reanswer, text_to_answer_finally)

        except RecursionError:
            return "Ошибка регистрации"


    def speechExceptionCommands(func):
        """Декоратор прослушивания комманд"""
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except speech_recognition.UnknownValueError:
                print('UnknownValueError')
                self.answer(self.answer(random.choice(self.data['commands']["misunderstand"]['response']),
                                            continue_target="commands"))
            except speech_recognition.WaitTimeoutError:
                print('WaitTimeoutError')
                self.answer(random.choice(self.data['commands']['silence']['response']),
                                continue_target="commands")
        return wrapper


    def speechExceptionService(func):
        """Декоратор прослушивания сервисных фраз"""
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except speech_recognition.UnknownValueError:
                print('UnknownValueError')
                print(self, args, kwargs)
                self.answer(response=kwargs['phrase_to_reanswer'],
                            continue_target="service")
            except speech_recognition.WaitTimeoutError:
                print('WaitTimeoutError')
                print(self, args, kwargs)
                self.answer(response=kwargs['phrase_to_reanswer'],
                            continue_target="service")
        return wrapper



    # проверка на регистрацию -> регистрация
    def register(self):
        if not FDM.isRegistrated():
            self.answer(response='Привет, давай познакомимся!', continue_target='service')
            self.answer(response='Как тебя зовут?', continue_target='service')
            try_name = self.askWhileFalse(type_='str', text_to_reanswer='Не понимаю! Как тебя зовут?',
                                          text_to_answer_finally='Отлично! Сколько тебе лет?')
            print('age')
            try_age = self.askWhileFalse(type_='int', text_to_reanswer='Не понимаю! Сколько тебе лет?',
                                          text_to_answer_finally='Отлично! Придумай кодовое слово?')
            print('password')
            try_password = self.askWhileFalse(type_='str', text_to_reanswer='Не понимаю! Придумай кодовое слово?',
                                          text_to_answer_finally='Отлично! Регистрация закончена!')

            return FDM.register(try_name, try_age, try_password)


    @speechExceptionCommands
    def listen_commands(self):   # метод прослушивания команд
        # continue_target = objective[:]
        # listening
        with self.source as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source=source)
            text = self.recognizer.recognize_google(audio_data=audio, language='ru_RU')

        # setting user phrase
        self.phrases.append(("Me: ", text))
        self.set_data(self.phrases)
        # matching with commands data
        return self.matchText(text)


    @speechExceptionService
    def listen_service(self, phrase_to_reanswer):
        # listening
        with self.source as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source=source)
            text = self.recognizer.recognize_google(audio_data=audio, language='ru_RU')

        # setting user phrase
        self.phrases.append(("Me: ", text))
        self.set_data(self.phrases)
        return text

    # поиск фразы в триггерах - ответ
    def matchText(self, phrase: str):   # распознает команды
        # проходимся по каждой команде из бд
        print('распознование')
        for command in self.data['commands']:
            # проверка на наличие слова-триггера в списке триггеров команды (триггер = спусковой крючок)
            if phrase.lower().strip() in self.data['commands'][command]["trigger"]:
                if command in FDM.commands_functions_dict:
                    response = FDM.commands_functions_dict[command]()
                else:
                    response = random.choice(self.data['commands'][command]['response'])
                continue_ = False if command == 'goodbye' else True
                return self.answer(response, continue_=continue_, continue_target='commands')     # вызов метода ответа с флагом продолжения
        return self.answer("Я вас не понимаю", continue_target='commands')


    def answer_text(self, response,  continue_target='commands', continue_=True,):
        # print(response.title())
        if continue_:   # если любая команда кроме goodbye
            if continue_target == 'commands':  # если слушаем команды
                self.listen_commands()
            else: pass   # если слушаем служебные команды
        self.phrases.append(("Assistant: ", response))
        return self.set_data(self.phrases)


    # отдельный метод ответа позволяет в будущем посылать ответ в динамик
    def answer(self, response, continue_target='commands', continue_=True,):
        # setting assistant phrase
        self.phrases.append(("Assistant: ", response))
        self.set_data(self.phrases)
        # audio-answer
        audio_text = gTTS(text=response, lang='ru', slow=False)
        audio_text.save('response.mp3')
        playsound('response.mp3')
        os.remove('response.mp3')
        # решение о продолжении прослушивания команд
        if continue_:
            if continue_target == 'commands':
                self.listen_commands()
            elif continue_target == 'service':
                return


def validDate(type_: str, phrase, maxQuantityWords: int = 3, maxLength: int = 40):
    """Проверка слов"""
    if phrase is not None:
        if type_ == 'int':
            return validAge(phrase)
        elif type_ == 'str':
            phrase_divided = phrase.split()
            if len(phrase) <= maxLength and len(phrase_divided) <= maxQuantityWords:
                return True
    return False


def validAge(phrase) -> bool:
    if phrase.isdigit():
        if 9 <= int(phrase) <= 100:
            return True
    return False
