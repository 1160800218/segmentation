# coding=utf-8
import re


# 输出黄金标准分割文本
def bulid_golden_standard(textname):
    fi = open(textname, 'r')
    b = fi.read()
    try:
        text_list = b.split('\n')
    finally:
        fi.close()

    fo = open('golden_standard.txt', 'w')
    for text in text_list:
        text = text[23:]
        text = re.sub(r'/(\]*[a-zA-Z]+)+ *\[*|\[', ' ', text)
        text = text[:len(text)-1]
        fo.write(text)
        fo.write('\n')


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
        seg_words = seg_list[i].split(' ')
        std_words = std_list[i].split(' ')
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


def main():
    bulid_golden_standard('199801_seg.txt')
    print('正向最大匹配分词')
    analysis('seg_FMM.txt', 'golden_standard.txt')
    print('\n')
    print('逆向最大匹配分词')
    analysis('seg_BMM.txt', 'golden_standard.txt')


if __name__ == '__main__':
    main()