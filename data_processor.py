from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data: list[str] = []
        self.rank = 0
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        result = (self.rank, self.data.pop(0))
        self.rank += 1 
        return result


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, (list)):
            for num in data:
                if not isinstance(num, (int, float)):
                    return False
            return True
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        if not isinstance(data, (list)):
            data = [data]
        for val in data:
            self.data.append(str(val))
            


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (str)):
            return True
        elif isinstance(data, (list)):
            for val in data:
                if not isinstance(val, (str)):
                    return False
            return True
        return False
    
    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        if not isinstance(data, (list)):
            data = [data]
        for val in data:
            self.data.append(str(val))


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        pass


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()
    print(" Trying to validate input '42':", num_proc.validate(42))
    print(" Trying to validate input 'Hello':", num_proc.validate('Hello'))
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest('foo')
    except TypeError as error:
        print("", error)
    print(" Processing data: [1, 2, 3, 4, 5]")
    num_proc.ingest([1, 2, 3, 4, 5])
    print(" Extracting 3 values...")
    for val in range(3):
        print(f" Numeric value {val}: {num_proc.output()[1]}")

    print("\nTesting Text processor...")



if __name__ == "__main__":
    main()
