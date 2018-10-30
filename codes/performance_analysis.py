# coding=utf-8
import re
import time
from codes.forward_maximum_matching import forward_maximum_matching
from codes.backward_maximum_matching import backward_maximum_matching
from codes.path import *


# 输出黄金标准分割文本
# output "golden_standard.txt"
def bulid_golden_standard(textname):
    fi = open(textname, 'r')
    b = fi.read()
    try:
        text_list = b.split('\n')
    finally:
        fi.close()

    fo = open(gold_std_path, 'w')
    for text in text_list:
        text = text[23:]
        text = re.sub(r'/(\]*[a-zA-Z]+)+ *\[*|\[', '/ ', text)
        fo.write(text)
        fo.write('\n')


# 性能分析
# return [precision, recall, F]
def analysis(seg_text, std_text):
    precision = 0   # 精确率
    recall = 0      # 召回率
    F = 0           # F值
    N = 0           # 黄金标准分割的单词数
    c = 0           # 分词器正确标注的单词数
    e = 0           # 分词器错误标注的单词数

    f1 = open(seg_text, 'r')
    f2 = open(std_text, 'r')
    buf1 = f1.read()
    buf2 = f2.read()
    try:
        seg_list = buf1.split('\n')
        std_list = buf2.split('\n')
    finally:
        f1.close()
        f2.close()

    # 删除分词列表中的空行
    blank = ''
    while blank in seg_list:
        seg_list.remove(blank)
    while blank in std_list:
        std_list.remove(blank)

    for i in range(min(len(seg_list), len(std_list))):
        seg_words = seg_list[i].split('/ ')
        std_words = std_list[i].split('/ ')
        seg_words = seg_words[:len(seg_words) - 1]      # 去掉最后一个空字符
        std_words = std_words[:len(std_words) - 1]
        # 标记每个词的位置
        seg_position = []   # 存放每个词的位置坐标
        std_position = []
        seg_vernier = 1     # 游标由1开始
        std_vernier = 1
        for word in seg_words:
            seg_position.append((seg_vernier, seg_vernier+len(word)))
            seg_vernier += len(word)
        for word in std_words:
            std_position.append((std_vernier, std_vernier+len(word)))
            std_vernier += len(word)
        # 取交集求正确划分的词语数量
        inter = list(set(seg_position).intersection(set(std_position)))
        c += len(inter)
        e += (max(len(seg_position), len(std_position)) - len(inter))
        N += len(std_words)

    precision = c / (c + e)
    recall = c / N
    F = 2 * precision * recall / (precision + recall)

    print('精确率 =', precision * 100, '%')
    print('召回率 =', recall * 100, '%')
    print('F值 =', F * 100, '%')
    return [precision, recall, F]


# 时间分析
# return time(ms)
def time_cost_of_FMM():
    time_start = time.time()
    forward_maximum_matching(dic_path, sent_path)
    time_end = time.time()
    return time_end - time_start


def time_cost_of_BMM():
    time_start = time.time()
    backward_maximum_matching(dic_path, sent_path)
    time_end = time.time()
    return time_end - time_start


def time_cost_of_both():
    time_start = time.time()
    forward_maximum_matching(dic_path, sent_path)
    backward_maximum_matching(dic_path, sent_path)
    time_end = time.time()
    return time_end - time_start


def time_analysis():
    time_FMM = round(time_cost_of_FMM()*1000)
    time_BMM = round(time_cost_of_BMM()*1000)
    print(time_FMM, 'ms')
    print(time_BMM, 'ms')
    print('total time is ',time_FMM + time_BMM, 'ms')
    fo = open(timeCost_path, 'w')
    fo.write('FMM耗时：' + str(time_FMM) + 'ms\n')
    fo.write('BMM耗时：' + str(time_BMM) + 'ms\n')
    fo.write('总共耗时：' + str(time_FMM + time_BMM) + 'ms')
    fo.close()


# 输出性能属性到"score.txt"
def output_2_file(fmm_analysis, bmm_analysis, params):
    fo = open(score_path, 'w')
    fo.write('正向最大匹配分词:\n')
    for i in range(3):
        fo.write(params[i])
        fo.write(str(fmm_analysis[i] * 100))
        fo.write('%\n')

    fo.write('\n')
    fo.write('逆向最大匹配分词:\n')

    for i in range(3):
        fo.write(params[i])
        fo.write(str(bmm_analysis[i] * 100))
        fo.write('%\n')
    fo.close()

def main():
    # 时间分析
    time_analysis()
    # 分词评价
    # bulid_golden_standard(seg_path)
    print('正向最大匹配分词:')
    fmm_analysis = analysis(seg_FMM_path, gold_std_path)
    print('\n')
    print('逆向最大匹配分词:')
    bmm_analysis = analysis(seg_BMM_path, gold_std_path)

    # 输出评价到文本
    params = ['精确率 = ', '召回率 = ', 'F值 = ']
    output_2_file(fmm_analysis=fmm_analysis, bmm_analysis=bmm_analysis, params=params)


if __name__ == '__main__':
    main()