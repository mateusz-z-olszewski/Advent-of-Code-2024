import abc
import os.path
from abc import abstractmethod
import unittest
import time


class AOC(abc.ABC, unittest.TestCase):
    PATH = "C:\\Users\\Mateusz\\PycharmProjects\\Advent Of Code 2024\\inputs\\"
    EXPECTED1 : ...
    EXPECTED2 : ... = None
    DO_BENCHMARK = False

    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)
        name = type(self).__module__
        folder_path = self.PATH + name + "\\"
        with open(folder_path + "example.txt") as file:
            self.EXAMPLE = file.read()
        with open(folder_path + "full.txt") as file:
            self.FULL = file.read()
        self.EXAMPLE2 = None

        if os.path.isfile(folder_path + "example2.txt"):
            with open(folder_path + "example2.txt") as file:
                self.EXAMPLE2 = file.read()

        if os.path.isfile(folder_path + "answers.txt"):
            with (open(folder_path + "answers.txt") as file):
                lines = file.readlines()
                self.ANSWER1 = lines[0].strip()
                self.ANSWER2 = lines[1].strip()
            print("Answers are known and are:")
            print("1.", self.ANSWER1)
            print("2.", self.ANSWER2)
        else:
            self.ANSWER1 = None
            self.ANSWER2 = None

        if os.path.isfile(folder_path + "benchmark.txt"):
            with open(folder_path + "benchmark.txt") as file:
                self.BENCHMARK = file.read()
        else:
            self.BENCHMARK = None



    @abstractmethod
    def part1(self, input : str) -> ...:
        pass

    def part2(self, input : str) -> ...:
        self.part1(input)

    def test(self):
        self.assertEqual(self.EXPECTED1, self.part1(self.EXAMPLE))
        full1 = self.part1(self.FULL)
        print(f"====\nResult for part 1: {full1}")
        if self.ANSWER1 is not None:
            self.assertEqual(self.ANSWER1, str(full1))

        if self.EXAMPLE2 is None:
            self.EXAMPLE2 = self.EXAMPLE
        if self.EXPECTED2 is None:
            print("Did not find expected value for part 2.")
            print(f"Result is {self.part2(self.EXAMPLE2)} anyway.")
        else :
            self.assertEqual(self.EXPECTED2, self.part2(self.EXAMPLE2))

        full2 = self.part2(self.FULL)
        print(f"====\nResult for part 2: {full2}")
        if self.ANSWER2 is not None:
            self.assertEqual(self.ANSWER2, str(full2))

        if not self.DO_BENCHMARK: return
        if self.BENCHMARK is not None:
            self.benchmark(self.BENCHMARK)
        else:
            self.benchmark(self.FULL)

    def benchmark(self, input):
        start_time = time.perf_counter()
        self.part1(input)
        end_time = time.perf_counter()
        print(f"Part 1. took {end_time - start_time:.3f} seconds")
        start_time = time.perf_counter()
        self.part2(input)
        end_time = time.perf_counter()
        print(f"Part 2. took {end_time - start_time:.3f} seconds")


