# Задача 1 - 13
Необходимо, заменив минимальное кол-во чисел в списке, сделать его арифметической прогрессией, например:

{ 1, 16, 4, 10, 7, 11, 1, -2 } → { 19, 16, 13, 10, 7, 4, 1, -2 } (заменены 3 элемента)
В случае нескольких подходящих вариантов замены минимального кол-ва элементов можно использовать любой.

Подсказка: необходимо для каждой пары элементов списка посчитать, сколько элементов списка придется изменить,
не меняя выбранную пару элементов, чтобы список стал арифметической прогрессией (очевидно, что в целых числах
некоторые пары элементов сразу же не будут подходить для построения арифметической прогрессии; например,
для приведенного примера в качестве опорной пары не подходят числа 4 и 7, т.к. между ними не может
быть дробного числа 5,5).