import os
import sys
import datetime
import random
import string


def main():
    print('Введите количество файлов между которыми будут распределены сгенерированные логи.'
          'По умолчанию это 3 файла.')
    logs_num = int(input() or 0)
    logs = list(map(lambda index: 'log' + str(index) + '.txt', range(logs_num))) if logs_num else ['log0.txt', 'log1.txt', 'log2.txt']
    print('Введите суммарное количество сгенерированных записей.'
          'По умолчанию это 100000 записей')
    logs_count = int(input() or 0) or 100000
    my_dir = os.path.dirname(__file__)
    logs = list(map(lambda log: os.path.join(my_dir, log), logs))
    log_files = []
    log_file_name = 'generated_log.txt'
    with open(log_file_name, 'w', encoding='utf-8') as generated:
        for index in range(logs_count):
            date = datetime.datetime.fromtimestamp(index*1000000).strftime('%d-%m-%Y %H:%M:%S')
            message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
            log_pattern = '[{0}] {1}\n'.format(date, message)
            generated.write(log_pattern)
        print('{0} записей успешно сгенерированы в {1}'.format(logs_count, log_file_name))
    try:
        with open('generated_log.txt', 'r', encoding='utf-8') as generated:
            for log in logs:
                log_files.append(open(log, 'w'))
            for line in generated:
                log_index = random.randint(0, len(log_files) - 1)
                log_files[log_index].write(line)
            print('{0} записей успешно распределены в файлы: {1}'.format(logs_count, logs))
    finally:
        for log in log_files:
            log.close()


if __name__ == "__main__":
    main()
