import regex
from dataclasses import dataclass

def parsing(string : str):
    def wrapper(cls):
        dataclass(cls)
        return cls
    return wrapper