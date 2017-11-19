import os
import sys
import datetime
import random
import string


def main():
    args = sys.argv[1:]
    if len(args):
        logs_num = args[0]
        logs_count = args[1]
        logs = list(map(lambda index: 'log' + str(index) + '.txt', range(logs_num)))
    else:
        logs = ['log1.txt', 'log2.txt', 'log3.txt']
        logs_count = 100000
    my_dir = os.path.dirname(__file__)
    logs = list(map(lambda log: os.path.join(my_dir, log), logs))
    log_files = []

    with open('generated_log.txt', 'w', encoding='utf-8') as generated:
        for index in range(logs_count):
            date = datetime.datetime.fromtimestamp(index*1000000).strftime('%d-%m-%Y %H:%M:%S')
            message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
            log_pattern = '[{0}] {1}\n'.format(date, message)
            generated.write(log_pattern)

    try:
        with open('generated_log.txt', 'r', encoding='utf-8') as generated:
            for log in logs:
                log_files.append(open(log, 'w'))
            for line in generated:
                log_index = random.randint(0, len(log_files) - 1)
                log_files[log_index].write(line)
    finally:
        for log in log_files:
            log.close()


if __name__ == "__main__":
    main()
