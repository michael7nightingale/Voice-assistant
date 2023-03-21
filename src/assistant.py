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
import src.file_data_manager as FDM
import pyaudio
from playsound import playsound     # для воспроизведения звука
from src.observer import Subject        # импорт наблюдаемого класса
import webbrowser
import mathmode


class Assistant(Subject, FDM.DataMixin):
    """Класс голосового помощника"""
    def __new__(cls, *args, **kwargs):  # элементарный конструктор класса
        if not hasattr(cls, 'instance'):    # Синглтон
            cls.instance = super().__new__(cls)
        return cls.instance

    # Моносостояние
    MONOCONDITIONAL_DATA = {
        'recognizer': sr.Recognizer(),
        'data': FDM.config_data,
        'threadAwait_flag': False,
        "ERRORLIMIT": 3,
        "modes": ('service', 'commands', 'websearch', 'mathmode')
    }

    def __init__(self):    # элементарный инициализатор класса
        self.__dict__ = self.MONOCONDITIONAL_DATA
        super().__init__()
        self.phrases = []
        self.source = sr.Microphone(device_index=1)
        self.user_num: int = 0

    def execute(self, mode="commands"):
        """Запуск помощника"""
        self.reanswer_phrases = 0
        self.name, self.age, self.keyword = FDM.get_user_info(self.user_num)
        self.mode = mode
        self.answer(f"Привет, {self.name}. Режим работы: {self.mode}", continue_target='commands')

    def speechExceptionAgain(func):
        """Декоратор прослушивания команд"""
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except speech_recognition.UnknownValueError:
                print('UnknownValueError')
                # проверка на превышение времени отклика пользователя
                self.reanswer_phrases += 1
                if self.reanswer_phrases >= self.ERRORLIMIT:
                    # self.send_error()
                    return
                else:
                    self.answer(self.answer(random.choice(self.data['commands']["misunderstand"]['response']),
                                            continue_target="commands"))
            except speech_recognition.WaitTimeoutError:
                print('WaitTimeoutError')
                # проверка на превышение времени отклика пользователя
                self.reanswer_phrases += 1
                if self.reanswer_phrases >= self.ERRORLIMIT:
                    # self.send_error()
                    return
                else:
                    self.answer(random.choice(self.data['commands']['silence']['response']),
                                continue_target="commands")
        return wrapper

    def speechExceptionOnce(func):
        """Декоратор прослушивания сервисных фраз"""
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except speech_recognition.UnknownValueError:
                print("serv", 'UnknownValueError')
                print(self, args, kwargs)
                self.answer(response=kwargs['phrase_to_reanswer'],
                            continue_target="service")
            except speech_recognition.WaitTimeoutError:
                print("serv", 'WaitTimeoutError')
                print(self, args, kwargs)
                self.answer(response=kwargs['phrase_to_reanswer'],
                            continue_target="service")
        return wrapper

    @speechExceptionAgain
    def listen_again(self):   # метод прослушивания команд
        # listening
        with self.source as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source=source, timeout=5)
            text = self.recognizer.recognize_google(audio_data=audio, language='ru_RU')

        # setting user phrase
        self.phrases.append(("Me: ", text))
        self.set_data(self.phrases)
        # matching with commands data
        return self.match_mode(text)

    @speechExceptionOnce
    def listen_once(self, phrase_to_reanswer):
        # listening
        with self.source as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source=source, timeout=5)
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

    def websearch(self, text):
        """Режим web-поиска"""
        query = text
        webbrowser.open('https://www.google.ru/search?q=' + text)

    def mathmode(self, text):
        """Математический режим. На данный момент поддерживает элементраные
        беспрефиксные выражения (два в степени шесть, миллион тысяча три минус ноль)"""
        try:
            response = str(mathmode.phrase_to_expression(text))
        except:
            response = 'Извините, на данный момент не умею такое считать. Подождите, пока Михаил Николаевич сделает' \
                      'для меня обновление...'
        return self.answer(response=response)

    def match_mode(self, text):
        """Функция валидации и мэтчинга режимов работы помощника."""
        # если режим не инициализирован, либо не находит места в self.modes
        if not hasattr(self, "mode"):
            raise ValueError("Не установлен режим работы ассистента")
        if self.mode not in self.modes:
            raise ValueError("Несуществующий режим работы ассистента")
        # иначе если режим корректен
        match self.mode:
            case "commands":
                return self.matchText(text)
            case "websearch":
                return self.websearch(text)
            case "mathmode":
                return self.mathmode(text)


    @FDM.safe_delete_response
    def answer(self, response, continue_target='commands', continue_=True,):
        # setting assistant phrase
        self.phrases.append(("Assistant: ", response))
        self.set_data(self.phrases)
        # audio-answer
        audio_text = gTTS(text=response, lang='ru')
        audio_text.save(self.DATA_DIR + self.RESPONSE_FILE_NAME)
        playsound(self.DATA_DIR + self.RESPONSE_FILE_NAME)
        FDM.delete_response()
        # play()
        # решение о продолжении прослушивания команд
        if continue_:
            if continue_target == 'commands':
                self.listen_again()
            elif continue_target == 'service':
                self.listen_again()
