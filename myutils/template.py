import abc
from abc import abstractmethod
import unittest


class AOC(abc.ABC, unittest.TestCase):
    PATH = "C:\\Users\\Mateusz\\PycharmProjects\\Advent Of Code\\inputs\\"
    EXPECTED1 : ...
    EXPECTED2 : ... = None

    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)
        name = type(self).__module__
        folder_path = self.PATH + name + "\\"
        with open(folder_path + "example.txt") as file:
            self.EXAMPLE = file.read()
        with open(folder_path + "full.txt") as file:
            self.FULL = file.read()

    @abstractmethod
    def part1(self, input : str) -> ...:
        pass

    def part2(self, input : str) -> ...:
        self.part1(input)

    def test(self):
        self.assertEqual(self.EXPECTED1, self.part1(self.EXAMPLE))
        print(f"====\nResult for part 1: {self.part1(self.FULL)}\n\n")

        if self.EXPECTED2 is None:
            print("Did not find expected value for part 2.")
            print(f"Result is {self.part2(self.EXAMPLE)} anyway.")
        else :
            self.assertEqual(self.EXPECTED2, self.part2(self.EXAMPLE))
        print(f"====\nResult for part 2: {self.part2(self.FULL)}")

