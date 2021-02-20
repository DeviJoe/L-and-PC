import typing as types

# В это место указать путь до файла ввода
INPUT_FILE_PATH_1 = "input1.txt"
INPUT_FILE_PATH_2 = "input2.txt"

_max_square = 0
_results = []


def write_matrix_in_file(file_path: str, matrix: types.List[types.List[bool]]):
    output_file: types.TextIO = open(file_path, 'w')
    for arr in matrix:
        for symbol in arr:
            buf = 1 if symbol is True else 0
            output_file.write(str(buf) + ' ')
        output_file.write('\n')
    output_file.close()


def read_file(file_name: str) -> types.List[types.List[bool]]:
    input_file: types.TextIO = open(file_name, 'r')
    matrix: types.List[types.List[bool]] = []
    for line in input_file:
        line = [bool(int(x)) for x in line.split(" ")]
        matrix.append(line)
    input_file.close()
    return matrix


def analyze_rectangle(matrix: types.List[types.List[bool]], row: int, col: int) -> bool:
    """
    Получает на вход точку матрицы и, двигаясь вправо и вниз, определяет, является ли данная фигура прямоугольником,
    окруженным пустыми ячейками
    :param matrix: матрица, в которой осуществляется поиск
    :param row: стартовый индекст строки
    :param col: стартовый индекс колонки
    :return: true/false по результату
    """
    if matrix[row][col] is False:
        return False

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
                return False

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
                return False
    update_square(row, col, col_pointer, row_pointer)
    return True


def update_square(row: int, col: int, col_pointer: int, row_pointer: int):
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
        _results.append({
            "point": (row, height),
            "width": width,
            "height": height,
            "square": square})


def clear_results():
    global _results, _max_square
    for rectangle in _results:
        if rectangle["square"] < _max_square:
            _results.remove(rectangle)


def task(input_file: str):
    matrix: types.List[types.List[bool]] = read_file(input_file)
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix[0])):
            analyze_rectangle(matrix, x, y)
        clear_results()
    print(*_results, sep='\n')
    write_matrix_in_file('output.txt', read_file(input_file))


if __name__ == '__main__':
    task(INPUT_FILE_PATH_1)
