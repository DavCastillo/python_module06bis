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
    print("=== Code Nexus - Data Stream ===\n")


if __name__ == "__main__":
    main()
