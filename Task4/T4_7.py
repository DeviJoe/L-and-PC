from typing import List, Dict, Tuple
import re

MONTHS_CSV: str = "months.csv"


def months_dict(input_csv: str) -> Tuple[Dict[int, int], Dict[str, int]]:
    """
    получает таблицу, по которой строит два словаря с длиной месяцев, первый - номер месяца и кол-во дней,
     второй - название месяца и кол-во дней
    :param input_csv: входная таблица
    :return:
    """
    d_int = {}
    d_str = {}
    with (open(input_csv, 'r', encoding='utf-8')) as thread:
        for line in thread:
            try:
                buf = line.split(';')
                buf[0] = int(buf[0])
                buf[2] = int(buf[2])
            except Exception:
                continue
            d_int[buf[0]] = buf[2]
            d_str[buf[1]] = buf[2]
    return d_int, d_str


def is_year_leap(year: str):
    i_year = int(year)
    if i_year % 4 != 0:
        return False

    if i_year % 100 != 0:
        return True
    else:
        if i_year % 400 == 0:
            return True
        else:
            return False


def is_numdate_correct(date: str) -> bool:
    """
    Проверяет введенную дату в числовом формате на корректность
    :param date: дата строкой
    :return:
    """
    parse: List[str] = date.split('.')
    # проверить дату на корректность
    if is_year_leap(parse[2]) and parse[1] == '02' and int(parse[0]) <= 29:
        return True

    d, _ = months_dict(MONTHS_CSV)
    days = d.get(int(parse[1]))

    if days < int(parse[0]):
        return False

    return True
    pass


def is_str_date_correct(date: str) -> bool:
    parse = date.split(' ')
    _, di = months_dict(MONTHS_CSV)
    days = di.get(parse[1])
    if days is None:
        return False
    else:
        if int(parse[0]) > days:
            return False

    if len(parse) == 3:
        if is_year_leap(parse[2]) and parse[1] == 'февраля' and int(parse[0]) <= 29:
            return True
    return True
    pass


def remove_date_numbers(text: List[str]):
    res = []
    for line in text:
        # даты числом
        list_eq_num = re.findall(r'\b((?:[0-2]\d|3[0-1]).(?:0\d|1[0-2]).\d{4})\b', line)
        # даты строкой без года (2 числа в дате)
        list_eq_str = re.findall(r'\b(?:[0-2]\d|3[0-1]) [^. ()\\/&!?]+\b', line)
        # даты строкой с годом (2 числа в дате)
        list_eq_str_year = re.findall(r'\b(?:[0-2]\d|3[0-1]) [^. ()\\/&!?]+ \d{4}\b', line)
        l2 = re.findall(r'\b[1-9] [^. ()\\/&!?]+ \d{4}\b', line)
        list_eq_str_year = list_eq_str_year + l2
        l3 = re.findall(r'\b[1-9] [^. ()\\/&!?]+\b', line)
        list_eq_str = list_eq_str + l3
        # print(list_eq_num)
        # print()
        # print(list_eq_str_year)
        # print()
        # print(list_eq_str)
        # print()

        # проверка численных дат
        for date in list_eq_num:
            if is_numdate_correct(date):
                line = line.replace(date, '')

        for date2 in list_eq_str_year:
            if is_str_date_correct(date2):
                line = line.replace(date2, '')

        for date1 in list_eq_str:
            if is_str_date_correct(date1):
                line = line.replace(date1, '')
        # print(line)
        res.append(line)
    return res
    pass


def read_file(file_name: str) -> List[str]:
    """
    Чтение файла и конвертация его содержимого в список
    :return: целочисленный список
    """
    input_file = open(file_name, 'r', encoding='utf-8')
    input_data: List[str] = []
    for line in input_file:
        input_data.append(line)
    input_file.close()
    return input_data


if __name__ == '__main__':
    t = read_file("input.txt")
    t = remove_date_numbers(t)
    print(*t, sep='\n')
    # print(*t)
    pass
