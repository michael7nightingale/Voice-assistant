"""
Реализация паттерна Наблюдатель для связи приложения и ассистента.
Грубо говоря, приложение должно при всяком изменении данных фраз ассистента
менять список отображаемых фраз. (подписано на рассылку)
"""
class Subject(object):
    """Класс-наблюдаемый объект"""
    def __init__(self):
        self._data = None
        self._observers = set()

    def subscribe(self, observer):
        """Метод добавления наблюдателя(подписчика)"""
        if not isinstance(observer, Observer):
            raise TypeError("наблюдатель не унаследован от класса Observer")
        else:
            self._observers.add(observer)

    def desubscribe(self, observer):
        """Метод удаления наблюдателя(подписчика)"""
        if observer in self._observers:
            self._observers.remove(observer)
        else:
            raise TypeError("Несуществующий наблюдатель для объекта")

    def set_data(self, new_data):
        """Метод установления данных"""
        self._data = new_data
        self.notify(self._data)

    def get_data(self):
        """Метод получения данных"""
        return self._data

    def notify(self, data):
        """Метод рассылки данных наблюдателям"""
        for observer in self._observers:
            observer.update(data)


class Observer:     # базовый класс Наблюдателя
    def update(self, date_to_send):   # абстрактный метод
        raise NotImplementedError("Метод update() не определен в классе наблюдателя")


# class ObserverPhrasesList(Observer):    # класс наблюдателя за обновлением произнесенных фраз ассистента
#     def update(self, data_to_send):
#         return data_to_send