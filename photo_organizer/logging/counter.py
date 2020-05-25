import logging
import math


class CounterLogger:
    """
    Helper logger for logging counter contents like: "Files renamed: 2000"
    Mainly for communicating progress
    """

    def __init__(self):
        self.counter = {}
        self.cur_step = {}

    def inc(self, prefix: str, increment: int = 1, step: int = 1000) -> None:
        if prefix not in self.counter:
            self.counter[prefix] = increment
            self.cur_step[prefix] = 0
        else:
            self.counter[prefix] = self.counter[prefix] + increment

        new_step = math.floor(self.counter[prefix] / step)
        if new_step > self.cur_step[prefix]:
            self.cur_step[prefix] = new_step
            logging.info(f"{prefix}: {self.cur_step[prefix] * step}")

    def dump(self) -> None:
        for prefix, count in self.counter.items():
            logging.info(f"{prefix}: {count}")