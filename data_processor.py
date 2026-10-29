from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data: list[tuple[int, str]] = []
        self.rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        result = self.data.pop(0)
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
            self.data.append((self.rank, str(val)))
            self.rank += 1


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
            raise TypeError("Got exception: Improper text data")
        if not isinstance(data, (list)):
            data = [data]
        for val in data:
            self.data.append((self.rank, str(val)))
            self.rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key, val in data:
                if not (isinstance(key, str) and isinstance(val, str)):
                    return False
            return True
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                for chk_dict in data:
                    for key, val in chk_dict.items():
                        if not (isinstance(key, str) and isinstance(val, str)):
                            return False
                return True
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper format data")
        if not isinstance(data, list):
            data = [data]
        for val in data:
            self.data.append((self.rank,
                              f"{val['log_level']}: {val['log_message']}"))
            self.rank += 1


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
    for _ in range(3):
        values = num_proc.output()
        print(f" Numeric value {values[0]}: {values[1]}")

    print("\nTesting Text processor...")
    txt_proc = TextProcessor()
    print(" Trying to validate input '42':", txt_proc.validate(42))
    print(" Processing data: ['Hello', 'Nexus', 'World']")
    txt_proc.ingest(['Hello', 'Nexus', 'World'])
    print(" Extracting 1 value...")
    print(f" Text value {txt_proc.data[0][0]}: {txt_proc.output()[1]}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print(" Trying to validate 'Hello':", log_proc.validate('Hello'))
    lst_dict = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
                {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    print(f" Processing data: {lst_dict}")
    log_proc.ingest(lst_dict)
    print(" Extracting 2 values...")
    for _ in range(2):
        log_ent = log_proc.output()
        print(f" Log entry {log_ent[0]}: {log_ent[1]}")


if __name__ == "__main__":
    main()
