from dataclasses import dataclass



@dataclass
class Mountain:
    name: str
    elevation: int


m = Mountain("Mount Everest", 8848)
print(type(m))
print(m)
print(type(str(m)))