from typing import Type


class DistanceIterator:
    counter: int
    max: int

    def __init__(self, inp_list: list) -> None:
        super().__init__()
        self.inp_list = inp_list
        self.counter = 1
        self.max = len(inp_list)

    def __next__(self):
        self.counter += 1
        if self.counter <= self.max:
            return self.counter
        else:
            if self.max == 2:
                raise StopIteration
            self.counter = 2
            self.max -= 1
            return self.counter

    def __iter__(self):
        return self