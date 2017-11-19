import os
import sys
import filecmp


def main():
    args = sys.argv[1:]
    if len(args):
        log_generated = args[0]
        log_merged = args[1]
    else:
        log_generated = 'generated_log.txt'
        log_merged = 'test_log.txt'
    my_dir = os.path.dirname(__file__)
    log_generated = os.path.join(my_dir, log_generated)
    log_merged = os.path.join(my_dir, log_merged)
    log_files = []

    with open(log_generated, 'r', encoding='utf-8') as generated, \
            open(log_merged, 'r', encoding='utf-8') as merged:
        equal_flag = True
        for line1, line2 in zip(generated, merged):
            if line1 != line2:
                equal_flag = False
                print(repr(line1))
                print('not equal')
                print(repr(line2))
            break
        if equal_flag:
            print('log files are equal')
        else:
            print('log files are NOT equal')



if __name__ == "__main__":
    main()
