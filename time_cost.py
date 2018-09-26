# coding=utf-8
import time
from forward_maximum_matching import forward_maximum_matching


def time_cost_of_FMM():
    time_start = time.time()
    forward_maximum_matching("dic.txt", '199801_sent.txt')
    time_end = time.time()
    return time_end - time_start


def main():
    print(round(time_cost_of_FMM()*1000), 'ms')


if __name__ == '__main__':
    main()