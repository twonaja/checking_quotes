import requests
import json
from os import path


def get_quote_from_website(currencies: str = 'ETHBTC') -> str:
    """
    :param currencies: пара валют имеющие формат CUR1CUR2
    :return возвращает актуальную котировку с сайта binance:
    """

    if not bool(currencies.strip()):
        raise ValueError
    if type(currencies) != str:
        raise TypeError

    req = requests.get("https://api.binance.com/api/v3/ticker/price", params={"symbol": currencies})
    return req.json()['price']


def read_config_file(file_name: str) -> dict:
    """
        :param file_name: имя файла конфигурации с данными по валютам
        :return: возвращает словарь типа {cur1/cur2: 'triger': 'cond', 'price': 'value'}
    """

    if not bool(file_name.strip()):
        raise ValueError
    if type(file_name) != str:
        raise TypeError
    if not path.exists(file_name) or not file_name.endswith('.json'):
        raise FileExistsError
    with open(file_name) as js_file:
        return json.load(js_file)


def get_first_four_curr(file_name) -> list:
    """

    :param file_name:
    :return:
    """

    if not bool(file_name.strip()):
        raise ValueError
    if type(file_name) != str:
        raise TypeError
    if not path.exists(file_name) or not file_name.endswith('.json'):
        raise FileExistsError

    with open(file_name) as js_file:
        curr_list = list(json.load(js_file).keys())
    ln_curr_list = len(curr_list)

    if ln_curr_list >= 4:
        return curr_list[:4]
    else:
        return curr_list[:ln_curr_list]


def compare_quote(trigger: str, quote_from_file: float, quote_from_website: float) -> bool:
    """
    :param trigger: условие срабатывание триггера
    :param quote_from_file: котировка которая прочитана из файла
    :param quote_from_website: котировка которая получена с сайта
    :return возвращает результат сравнения двух цен:
    """

    if trigger not in ['more', 'less', 'more_eq', 'less_eq']:
        raise ValueError
    if type(trigger) != str or type(quote_from_file) != float \
            or type(quote_from_website) != float:
        raise TypeError

    if trigger == 'more':
        return quote_from_file < quote_from_website
    elif trigger == 'less':
        return quote_from_file > quote_from_website
    elif trigger == 'more_eq':
        return quote_from_file <= quote_from_website
    elif trigger == 'less_eq':
        return quote_from_file >= quote_from_website


def do_job(currencies: str, trigger: str, quote_from_file: str) -> str:
    """
    :param currencies: пара валют формата CUR1/CUR2
    :param trigger: условие срабатывание триггера
    :param quote_from_file: котировка взятая из файла
    :return: возвращает форматированную строку если произошло событие (триггер) или строку с 'None', если для валюты не
    произошло никаких событий
    """

    if not bool(currencies.strip()) or not bool(trigger.strip()) or not bool(quote_from_file.strip()):
        raise ValueError
    if type(currencies) != str or type(trigger) != str or type(quote_from_file) != str:
        raise TypeError

    quote_from_website = get_quote_from_website(currencies.replace('/', ''))

    if compare_quote(trigger, float(quote_from_file), float(quote_from_website)):
        return f'Для пары валют {currencies} произошел триггер {trigger}!\n ' \
               f'Котировка в файле {quote_from_file}, котировка на сайте {quote_from_website.rstrip("0")}'
    else:
        return 'None'
