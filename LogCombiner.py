import re
import time
import heapq
from collections import namedtuple

log_data = namedtuple('log_data', ['data', 'string', 'file'])


class LogDateException(Exception):
    pass


class LogCombiner:
    """
    Provide generator to merge list of log files into one file
    """
    @staticmethod
    def parse_date(string, reg_pattern):
        """
        :param string: date in string format
        :param reg_pattern: regexp date pattern
        :return: returns date in struct_time format
        """
        date_match = re.match(reg_pattern, string)
        if date_match is None:
            raise LogDateException
        date = date_match.group(1)
        return time.strptime(date, '%d-%m-%Y %H:%M:%S')

    def __init__(self, log_files, date_parse_pattern):
        self._log_heap = []
        self._parse_pattern = date_parse_pattern
        self._log_files = log_files
        self._init_log_generator()

    def _push_heap_data(self, log_file):
        """
        To merge two log lists we need to take log string with min date from the top of files in file list
        I've decided to use priority queue to sort top strings of files
        This function pushes new tuple (date, log_string, log_file) into queue
        :param log_file:
        :return:
        """
        push_flag = True
        while push_flag:
            log_string = log_file.readline()
            if log_string:
                try:
                    date = LogCombiner.parse_date(log_string, self._parse_pattern)
                    heapq.heappush(self._log_heap, (date, log_string, log_file))
                    push_flag = False
                except LogDateException:
                    push_flag = True
            else:
                self._log_files.remove(log_file)
                push_flag = False

    def _pop_heap_data(self):
        """
        priority queue always gives us min item at the root
        :return:
        """
        return heapq.heappop(self._log_heap)

    def _init_log_generator(self):
        """
        Before use we need to fill our queue
        :return:
        """
        for log in self._log_files:
            self._push_heap_data(log)

    def __iter__(self):
        """
        This generator gives us new log string one by one in ascending order
        :return:
        """
        while len(self._log_files):
            log_item = log_data(*self._pop_heap_data())
            yield log_item.string
            self._push_heap_data(log_item.file)
        return