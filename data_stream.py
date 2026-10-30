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


class DataProcessor:
    def __init__(self) -> None:
        self.processor: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, NumericProcessor):
            self.processor.append(proc)
        elif isinstance(proc, TextProcessor):
            self.processor.append(proc)
        elif isinstance(proc, LogProcessor):
            self.processor.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for proc in self.processor:
            if proc and proc.va
        #for elem in stream:
         #   if self.processor[0].validate(elem):
          #      self.processor[0].ingest(elem)
           ##    self.processor[1].ingest(elem)
            #elif self.processor[2].validate(elem):
             #     self.processor[2].ingest(elem)
            #else:
                #print(f"DataStream error - Can't process element in stream: {elem}")

    def print_processors_stats(self) -> None:
        if not self.processor:
            print("No processor found, no data")
        elif isinstance(self.processor[0], NumericProcessor):
            print(f"Numeric Processor: total {self.processor[0].rank} items processed, remaining {len(self.processor[0].data)} on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    print("== Data stream statistics ==")
    stream = DataProcessor()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    data_stream = ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]
    stream.register_processor(NumericProcessor())
    print(f"Send first batch of data on stream: {data_stream}")
    stream.process_stream(data_stream)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

if __name__ == "__main__":
    main()
