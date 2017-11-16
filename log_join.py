import LogCombiner
import os
import sys


def main():
    """
    I had a lot of time to finish this task, that's why i'we tried to do my best.
    I've decided to complicate the task and considered case with list of log files
    """
    args = sys.argv[1:]
    if len(args):
        logs = args
    else:
        logs = ['log1.txt', 'log2.txt', 'log3.txt']
    my_dir = os.path.dirname(__file__)
    logs = list(map(lambda log: os.path.join(my_dir, log), logs))
    re_pattern = r'\[(.+)\]\s+'
    log_files = []

    try:
        for log in logs:
            log_files.append(open(log))
        log_combiner = LogCombiner.LogCombiner(log_files, re_pattern)
        with open('test_log.txt', 'w', encoding='utf-8') as file:
            for log_string in log_combiner:
                file.write(log_string)
    finally:
        for log in log_files:
            log.close()


if __name__ == "__main__":
    main()
