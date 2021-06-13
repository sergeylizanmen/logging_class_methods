import functools
from typing import Callable
import time


def logging(func: Callable):
    """
    Лог-Декоратор для функций

    Добавляет в лог файл информацию
    по дате и времени использования функции, название функции, и документация функции
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        with open('methods_info.log', 'a', encoding='utf-8') as log_file:
            log_file.write(time.strftime("%d.%m.%Y %H:%M", time.localtime()))
            log_file.write(f' function: {func.__name__}\n')
            log_file.write(f'doc: {func.__doc__} \n')
        res = func(*args, **kwargs)
        return res

    return wrapper


def decorator_for_class_methods(decorator: Callable):
    """
    Декоратор для классов

    Применяет для всех методов класса (кроме "магических") переданный декоратор
    """

    @functools.wraps(decorator)
    def decorate(cls):
        for method_name in dir(cls):
            if not method_name.startswith('__'):
                cur_method = getattr(cls, method_name)
                decorated_method = decorator(cur_method)
                setattr(cls, method_name, decorated_method)
        return cls

    return decorate


@logging
def cube(number: int) -> int:
    """ Функция, возвращающая куб числа """
    return number ** 3


@decorator_for_class_methods(logging)
class Number:
    """
    Класс - число

    Args:
        number (int): значение числа
    """

    def __init__(self, number: int) -> None:
        self.number = number

    def __str__(self):
        return f'Число {self.number}'

    def square(self) -> int:
        """ Функция, возвращающая квадрат числа """
        return self.number ** 2

    def power(self, value: int) -> int:
        """ Функция, возвращающая заданную степень числа """
        return self.number ** value


n = Number(2)
print(n.square())
time.sleep(2)
print(n.power(7))
time.sleep(2)
print(cube(7))
