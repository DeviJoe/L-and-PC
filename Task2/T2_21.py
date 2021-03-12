import typing as types
import sys
from dataclasses import dataclass


@dataclass
class Rectangular:
    row: int
    col: int
    row_pointer: int
    col_pointer: int
    square: int


# В это место указать путь до файла ввода
INPUT_FILE_PATH_1 = "input1.txt"
INPUT_FILE_PATH_2 = "input2.txt"
OUTPUT_1 = ''
OUTPUT_2 = ''

_max_square: int = 0
_results: types.List[Rectangular] = []


def write_matrix_in_file(file_path: str, matrix: types.List[types.List]):
    output_file: types.TextIO = open(file_path, 'w')
    for arr in matrix:
        for symbol in arr:
            if type(symbol) == bool:
                buf = 1 if symbol is True else 0
            else:
                buf = symbol
            output_file.write(str(buf) + ' ')
        output_file.write('\n')
    output_file.close()


def read_file(file_name: str) -> types.List[types.List[bool]]:
    input_file: types.TextIO = open(file_name, 'r')
    matrix: types.List[types.List[bool]] = []
    for line in input_file:
        buf = [bool(int(x)) for x in line.split(" ")]
        matrix.append(buf)
    input_file.close()
    return matrix


def analyze_rectangle(matrix: types.List[types.List[bool]], row: int, col: int) -> Rectangular:
    """
    Получает на вход точку матрицы и, двигаясь вправо и вниз, определяет, является ли данная фигура прямоугольником,
    окруженным пустыми ячейками
    :param matrix: матрица, в которой осуществляется поиск
    :param row: стартовый индекст строки
    :param col: стартовый индекс колонки
    :return: true/false по результату
    """
    if matrix[row][col] is False:
        return None

    # точка окончания прямоугольника по строке
    row_pointer: int = row
    # точка окончания прямоугольника по колонке
    col_pointer: int = col

    # определение границ прямоугольника в высоту
    try:
        while matrix[row_pointer + 1][col] is True:
            row_pointer += 1
    except IndexError:
        row_pointer = len(matrix) - 1

    # определение границ прямоугольника в ширину
    try:
        while matrix[row][col_pointer + 1] is True:
            col_pointer += 1
    except IndexError:
        col_pointer = len(matrix[0]) - 1

    # проверка, что заполнение прямоугольника "без дырок"
    for x in range(row, row_pointer + 1):
        for y in range(col, col_pointer + 1):
            if matrix[x][y] is False:
                return None

    # массив с координатами точек, составляющих "рамку прямоугольника"
    frame: types.List[tuple] = []
    for x in range(row - 1, row_pointer + 2):
        frame.append((x, col - 1))
        frame.append((x, col_pointer + 1))
    for y in range(col, col_pointer + 1):
        frame.append((row - 1, y))
        frame.append((row_pointer + 1, y))
    # проверку проходят только точки, чьи координаты лежат внутри матрицы
    for point in frame:
        if (point[0] < 0) or (point[0] >= len(matrix)) or (point[1] < 0) or (point[1] >= len(matrix)):
            continue
        else:
            if matrix[point[0]][point[1]] is True:
                return None
    return create_rectangular(row, col, row_pointer, col_pointer)


def create_rectangular(row: int, col: int, col_pointer: int, row_pointer: int) -> Rectangular:
    """
    Определяет площадь прямоугольника, зная координату верхнего левого угла и его границы
    (индексы колонок и сторк, в границах которых лежит прямоугольник, см ф-цию выше)
    :param row: стартовый индекс строки
    :param col: стартовый индекс колонки
    :param col_pointer: колонка, до которой (включительно) простирается прямоугольник
    :param row_pointer: строка, до которой (включительно) простирается прямоугольник
    """
    width: int = col_pointer - col + 1
    height: int = row_pointer - row + 1
    square = width * height
    global _max_square, _results
    if square >= _max_square:
        _max_square = square
        return Rectangular(row, col, row_pointer, col_pointer, square)


def rectangular_to_matrix(rec_dict: Rectangular, matrix) -> types.List[types.List[int]]:
    res = [[0 for x in range(0, len(matrix[0]))] for y in range(0, len(matrix))]
    for x in range(rec_dict.row, rec_dict.row_pointer + 1):
        for y in range(rec_dict.col, rec_dict.col_pointer + 1):
            res[x][y] = 1
    return res


def find_max_up_left_rec_in_res():
    global _results
    res_rec: types.List[Rectangular] = []
    result: Rectangular = Rectangular(0, 0, 0, 0, 0)
    row = sys.maxsize
    col = sys.maxsize
    for rec in _results:
        if rec.row < row:
            row = rec.row
            res_rec.append(rec)

    if res_rec.__len__() == 1:
        return res_rec[0]
    else:
        for rec in res_rec:
            if rec.col < col:
                col = rec.col
                result = rec
        return result


def find_max_left(excepting: Rectangular) -> Rectangular:
    global _results
    buf = _results.copy()
    buf.remove(excepting)
    col = sys.maxsize
    res: Rectangular = Rectangular(0, 0, 0, 0, 0)
    for rec in buf:
        if rec.col < col:
            col = rec.col
            res = rec
    return res


def task(input_file: str):
    matrix: types.List[types.List[bool]] = read_file(input_file)
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix[0])):
            buf = analyze_rectangle(matrix, x, y)
            if buf is not None:
                _results.append(buf)

    if len(_results) == 1:
        write_matrix_in_file('output.txt', rectangular_to_matrix(_results[0], matrix))
    else:
        res1: Rectangular = find_max_up_left_rec_in_res()
        res2: Rectangular = find_max_left(res1)
        write_matrix_in_file('output_1.txt', rectangular_to_matrix(res1, matrix))
        write_matrix_in_file('output_2.txt', rectangular_to_matrix(res2, matrix))
    print(*_results, sep='\n')


if __name__ == '__main__':
    task(INPUT_FILE_PATH_1)
