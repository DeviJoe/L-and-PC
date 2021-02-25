from typing import List
import typing
import itertools
import sys
from Task1 import DistanceIterator

# В это место указать путь до файла ввода
INPUT_FILE_PATH = "input.txt"


def read_file(file_name: str) -> List[int]:
    """
    Чтение файла и конвертация его содержимого в целочисленный список
    :return: целочисленный список
    """
    input_file = open(file_name, 'r')
    input_data: str = ""
    for line in input_file:
        input_data = line
    input_file.close()
    return [int(n) for n in input_data.split(", ")]


def write_file(file_name: str, data: str):
    """
    Запись списка в файл
    :param file_name: имя файла
    :param data: список
    """
    output_file = open(file_name, "w")
    output_file.write(str(data))
    output_file.close()


def is_progression_exists(num1: int, num2: int, distance: int) -> bool:
    """
    Для двух элементов из списка проверяет, являются ли они частью арифметической прогрессии
    :param num1: первое число
    :param num2: второе число
    :param distance: расстояние между этими числами, включая эти числа
    :return: true - если существует, false - если нет
    """
    delta = num2 - num1
    step = delta / (distance - 1)
    return True if (step % 1 == 0.0) else False


def task(file_path: str):
    """
    Подробное описание задачи см. в файле task1.md <a href = "Task1/task1.md"/>
    """
    input_list: List[int] = read_file(file_path)
    # итератор, выбирающий комбинации по 2 без повторений из списка, возвращает в виде кортежа индексов списка
    comb_iter: typing.Iterator = itertools.combinations([x for x in range(0, len(input_list) - 1)], 2)
    di = DistanceIterator.DistanceIterator(input_list)

    # в качестве стартового значения минимального кол-ва перестановок принято максимальное целое число
    min_permutations: int = sys.maxsize
    output_list: List = []

    for tuple_2 in comb_iter:
        dist = next(di)
        if is_progression_exists(tuple_2[0], tuple_2[1], dist):
            # шаг возможной прогрессии
            step_progress = int((input_list[tuple_2[1]] - input_list[tuple_2[0]]) / (dist - 1))
            dto = generate_list_progression_from_list_with_step_and_pivot(input_list, tuple_2[0], step_progress)
            if dto[1] < min_permutations:
                output_list = dto[0]
                min_permutations = dto[1]
    write_file("output.txt", str(output_list) + "\n" + str(min_permutations))


def generate_list_progression_from_list_with_step_and_pivot(inp_list: List, pivot_index: int, step: int) -> tuple:
    """
    Из исходного листа по выбранному элементу и шагу перестраивает список в прогрессию, возвращая новый список и количество измененных
    элементов
    :param inp_list: входной список
    :param pivot_index: выбранный индекс, по которому начнет считаться прогрессия
    :param step: шаг прогрессии
    :return: кортеж вида (новый список, кол-во измененных элементов)
    """
    # счетчик количества изменений
    counter = 0
    buf: List = inp_list.copy()
    index = pivot_index - 1
    while index != -1:
        if buf[index] + step != buf[index + 1]:
            buf[index] = buf[index + 1] - step
            counter += 1
        index -= 1

    index = pivot_index + 1
    while index != len(buf):
        if buf[index] - step != buf[index - 1]:
            buf[index] = buf[index - 1] + step
            counter += 1
        index += 1

    return buf, counter


if __name__ == '__main__':
    task(INPUT_FILE_PATH)
