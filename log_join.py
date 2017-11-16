import LogCombiner
import os
import sys


def main():
    args = sys.argv[1:]
    if len(args):
        logs = args
    else:
        logs = ['log1.txt', 'log2.txt', 'log3.txt']
    my_dir = os.path.dirname(__file__)
    logs = list(map(lambda log: os.path.join(my_dir, log), logs))
    log_files = []

    try:
        for log in logs:
            log_files.append(open(log))
        log_combiner = LogCombiner.LogCombiner('test', log_files, r'\[(.+)\]\s+')
        with open('test_log.txt', 'w', encoding='utf-8') as file:
            for log_string in log_combiner.log_generator():
                file.write(log_string)
    finally:
        for log in log_files:
            log.close()


if __name__ == "__main__":
    main()
