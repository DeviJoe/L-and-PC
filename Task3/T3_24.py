from typing import Dict, TextIO, List, Tuple
from Task3.Sweet import Sweet
import sys

INPUT_CSV_FILE: str = "input.csv"
MONEY: int = 35


def parse_csv_into_dict(file_name: str) -> List[Sweet]:
    res: List[Sweet] = []
    with (open(file_name, 'r', encoding='utf-8')) as thread:
        for line in thread:
            buf: List[str] = line.split(";")
            if buf[1] == 'price\n':
                continue
            buf[1] = int(buf[1])
            res.append(Sweet(*buf))
    return res


def task(sweets: List[Sweet]) -> Tuple[List[Sweet], int]:
    """
    Пройтись по сортированному списку конфет, набрать разнообразных конфет по килограмму.
    Если баланс позволяет вычеркнуть самую дорогую из списка и купить подороже - покупаем
    :param sweets: список конфет
    :return:
    """

    # сортированный список конфет
    s_l: List[Sweet] = sweets.copy()
    s_l.sort(key=lambda sweet_exs: sweet_exs.price)
    print("Исходное")
    print(*s_l, sep='\n')
    print()
    res: List[Sweet] = []
    # затраченные на конфеты деньги
    buf_money = 0
    # максимальное кол-во конфет, которое можно себе позволить
    max_sweets = 0

    # собираем разнообразный список самых дешевых конфет, пока на остаток нельзя будет ничего купить
    i = 0
    while i != len(s_l):
        if buf_money + s_l[i].price <= MONEY:
            res.append(s_l[i])
            buf_money += s_l[i].price
            s_l.remove(s_l[i])
            i -= 1
            max_sweets += 1
        i += 1

    i = len(res) - 1

    while i != -1:
        if MONEY - buf_money == 0:
            return res, MONEY - buf_money

        # res.sort(key=lambda sweet_exs: sweet_exs.price)
        min_money_cash = MONEY - buf_money
        sweet = res[i]
        res.remove(sweet)
        buf_money -= sweet.price
        sweet_cash: Sweet = None

        for s in s_l:
            cash = MONEY - buf_money - s.price
            if cash < 0:
                res.append(sweet)
                return res, MONEY - buf_money - sweet.price
            if cash < min_money_cash:
                min_money_cash = cash
                sweet_cash = s

        if (sweet_cash == sweet) or (sweet_cash is None):
            res.append(sweet)
            buf_money += sweet.price
            break
        res.append(sweet_cash)
        buf_money += sweet_cash.price
        s_l.remove(sweet_cash)
        s_l.append(sweet)
        i -= 1

    # # СТАТИСТИКА !!!!
    # print("Откуда берем")
    # print(*s_l, sep='\n')
    # print()
    # print("Что купили")
    # print(*res, sep='\n')
    # print()
    # print("денег потратили")
    # print(buf_money)
    # print("денег осталось")
    # print(MONEY - buf_money)
    # print("Макс кофет")
    # print(max_sweets)
    return res, MONEY - buf_money


if __name__ == '__main__':
    sweet_l: List[Sweet] = parse_csv_into_dict("input.csv")
    r, saved_money = task(sweet_l)
    print(*r, sep='\n')
    print(saved_money)
    pass