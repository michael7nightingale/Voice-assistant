# def askWhileFalse(self, text_to_reanswer: str, text_to_answer_finally: str, type_: str):
#     """Функция для переспрашивания, пока не истинно условие"""
#     try:
#         try_phrase = self.listen_once(phrase_to_reanswer=text_to_reanswer)
#         if validDate(type_, try_phrase):
#             self.answer(continue_target='service', response=text_to_answer_finally)
#             return try_phrase
#         return self.askWhileFalse(type_, text_to_reanswer, text_to_answer_finally)
#     except RecursionError:
#         return "Ошибка регистрации"


# def register(self):
#     """Проверка на регистрацию -> регистрация"""
#     if not FDM.isRegistrated():
#         self.answer(response='Привет, давай познакомимся!', continue_target='service')
#         self.answer(response='Как тебя зовут?', continue_target='service')
#         try_name = self.askWhileFalse(type_='str', text_to_reanswer='Не понимаю! Как тебя зовут?',
#                                       text_to_answer_finally='Отлично! Сколько тебе лет?')
#         print('age')
#         try_age = self.askWhileFalse(type_='int', text_to_reanswer='Не понимаю! Сколько тебе лет?',
#                                      text_to_answer_finally='Отлично! Придумай кодовое слово?')
#         print('password')
#         try_password = self.askWhileFalse(type_='str', text_to_reanswer='Не понимаю! Придумай кодовое слово?',
#                                           text_to_answer_finally='Отлично! Регистрация закончена!')
#
#         return FDM.register(try_name, try_age, try_password)