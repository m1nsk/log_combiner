import re
import time
import heapq
from collections import namedtuple
from datetime import datetime

log_data = namedtuple('log_data', ['data', 'string', 'file'])


class LogDateException(Exception):
    pass


class LogCombiner:
    @staticmethod
    def parse_date(reg_pattern, string):
        date_match = re.match(reg_pattern, string)
        if date_match is None:
            raise LogDateException
        date = date_match.group(1)
        return time.strptime(date, '%d-%m-%Y %H:%M:%S')

    def _generator_builder(self, file):
        def generator(file):
            log_flag = True
            min_date = None
            log_string = file.readline()
            while log_flag:
                if log_string:
                    try:
                        log_date = self.parse_date(self.parse_pattern, log_string)
                        min_date = yield log_date if min_date is None else (log_date if min_date > log_date else ())
                        if min_date is not None and min_date == log_date:
                            log_string = file.readline()
                            dt = datetime.fromtimestamp(time.mktime(log_date))
                            print(dt)
                    except LogDateException:
                        log_string = file.readline()
                else:
                    return
        return generator(file)

    def _init_generators(self):
        self.generator_list = []
        for file in self.log_files:
            self.generator_list.append(self._generator_builder(file))

    def __init__(self, log_files, date_parse_pattern):
        self.log_heap = []
        self.parse_pattern = date_parse_pattern
        self.log_files = log_files
        self._init_generators()

    def _init__log_generator(self):
        for log in self.log_files:
            self._push_heap_data(log)

    def generate(self):
        min_date = None
        remove_gen = None
        for gen in self.generator_list:
            next(gen)
        while len(self.generator_list):
            if remove_gen is not None:
                self.generator_list.remove(remove_gen)
                remove_gen = None
            for gen in self.generator_list:
                try:
                    min_date = gen.send(min_date)
                    dt = datetime.fromtimestamp(time.mktime(min_date))
                    # print(dt)
                except StopIteration:
                    remove_gen = gen
