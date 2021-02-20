import typing as types

# В это место указать путь до файла ввода
INPUT_FILE_PATH_1 = "input1.txt"
INPUT_FILE_PATH_2 = "input2.txt"


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


def is_rectangle(matrix: types.List[types.List[bool]], row: int, col: int) -> bool:
    if matrix[row][col] is False:
        return False

    row_pointer = row
    col_pointer = col

    try:
        while matrix[row_pointer + 1][col] is True:
            row_pointer += 1
    except IndexError as e:
        row_pointer = len(matrix) - 1

    try:
        while matrix[row][col_pointer + 1] is True:
            col_pointer += 1
    except IndexError as e:
        col_pointer = len(matrix[0]) - 1

    for x in range(row, row_pointer + 1):
        for y in range(col, col_pointer + 1):
            if matrix[x][y] is False:
                return False

    frame: types.List[tuple] = []
    for x in range(row - 1, row_pointer + 2):
        frame.append((x, col - 1))
        frame.append((x, col_pointer + 1))
    for y in range(col, col_pointer + 1):
        frame.append((row - 1, y))
        frame.append((row_pointer + 1, y))
    for point in frame:
        if (point[0] < 0) or (point[0] >= len(matrix)) or (point[1] < 0) or (point[1] >= len(matrix)):
            continue
        else:
            if matrix[point[0]][point[1]] is True:
                return False

    return True


def task(input_file: str):
    matrix: types.List[types.List[bool]] = read_file(input_file)
    for x in range(0, len(matrix)):
        for y in range(0, len(matrix[0])):
            print(str(int(is_rectangle(matrix, x, y))) + ' ', end='')
        print()
    write_matrix_in_file('output.txt', read_file(input_file))


if __name__ == '__main__':
    task(INPUT_FILE_PATH_1)
