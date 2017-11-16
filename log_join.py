import datetime
import re
import time
import heapq
from collections import namedtuple
import os

log_data = namedtuple('log_data', ['data', 'string', 'file'])


class LogDateException(Exception):
    pass


class LogCombiner:
    @staticmethod
    def parse_date(string, reg_pattern):
        date_match = re.match(reg_pattern, string)
        if date_match is None:
            raise LogDateException
        date = date_match.group(1)
        return time.strptime(date, '%d-%m-%Y %H:%M:%S')

    def __init__(self, result_file_name, log_files, date_parse_pattern):
        self.log_heap = []
        self.parse_pattern = date_parse_pattern
        self.log_files = log_files
        self._init__log_generator()

    def _push_heap_data(self, log_file):
        push_flag = True
        while push_flag:
            log_string = log_file.readline()
            if log_string:
                try:
                    date = LogCombiner.parse_date(log_string, self.parse_pattern)
                    heapq.heappush(self.log_heap, (date, log_string, log_file))
                    push_flag = False
                except LogDateException:
                    push_flag = True
            else:
                self.log_files.remove(log_file)
                push_flag = False

    def _pop_heap_data(self):
        return heapq.heappop(self.log_heap)

    def _init__log_generator(self):
        for log in self.log_files:
            self._push_heap_data(log)

    def log_generator(self):
        while len(self.log_files):
            log_item = log_data(*self._pop_heap_data())
            yield log_item.string
            self._push_heap_data(log_item.file)
        return



logs = ['log1.txt', 'log2.txt', 'log3.txt']
my_dir = os.path.dirname(__file__)
logs = list(map(lambda log: os.path.join(my_dir, log), logs))
log_files = []


try:
    for log in logs:
        log_files.append(open(log))
    logCombiner = LogCombiner('test', log_files, r'\[(.+)\]\s+')
    for log_string in logCombiner.log_generator():
        print(log_string)
finally:
    for log in log_files:
        log.close()

