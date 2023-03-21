import numpy as np


numbers = ("ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять")

tens_numbers = ("одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать",
                "семнадцать", "восемнадцать", "девятнадцать")

tens = ("десять", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто")

hundreds = ("сто",  "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот")

degrees = ("тысяча", "миллион")

operators = {"умножить": "*", "степени": "**", "разделить": "/", "синус": "sin", "косинус": "cos",
             "плюс": "+", "минус": "-"}



def text_to_integer(text: str) -> str:
    integer = 0
    last_more_int = 10**10
    saved_prefix = 1
    for i, word in enumerate(text.split()):
        # сразу проверка если есть префиксное число



        if word in numbers:
            to_add = numbers.index(word)
        elif word in tens_numbers:
            to_add = tens_numbers.index(word) + 11
        elif word in tens:
            to_add = (tens.index(word) + 1) * 10
        elif word in hundreds:
            to_add = (hundreds.index(word) + 1) * 100
        elif word in degrees:
            to_add = 10**((degrees.index(word) + 1)*3)
        else:
            return "No matches found"
        if last_more_int > to_add:
            last_more_int = to_add
            integer += to_add

    return str(integer)


print(text_to_integer(""))


def phrase_to_expression(text: str) -> int:
    result = ''
    words = (i for i in text.split() if i not in ('на', 'в', ...))
    first_add = list()
    for i in words:
        if i in operators.values():
            result += str(i)
        elif i.isdigit():
            result += str(i)
        elif i in operators:
            if first_add:
                result += text_to_integer(" ".join(first_add))
            first_add.clear()
            result += operators[i]
        else:
            first_add.append(i)
    if first_add:
        result += text_to_integer(" ".join(first_add))

    return eval(result)


# print(phrase_to_expression("два разделить на пять"))

