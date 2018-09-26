# coding=utf-8
import re
import trie_tree as trie


def forward_maximum_matching(dic, in_text):
    # 读取词典文件
    file = open(dic, "r")
    try:
        b = file.read()
    finally:
        file.close()
    # 将词典转化Trie树并计算最长词的长度
    word_list = b.split('\n')
    maxLen = 0
    for i in range(len(word_list)):
        word_list[i] = re.sub(r' +\d+ +[a-z]+', '', word_list[i])
        if len(word_list[i]) > maxLen:
            maxLen = len(word_list[i])
    trie.add_all(word_list)

    # 读取待分词文件
    fi = open(in_text, 'r')
    try:
        b = fi.read()
    finally:
        fi.close()
    text = b.split('\n')

    seg_text = []           # 存储切分的文本
    # 逐行切分
    for str in text:
        # 用于存储切分好的词的列表
        segList = []
        while len(str) > 0:
            length = maxLen
            # 如果最大分词长度大于待切分字符串长度，则切分长度设置为待切分字符串长度
            if len(str) < maxLen:
                length = len(str)
            # 正向取字符串中长度为length的子串
            tryWord = str[0:length]
            while not trie.contain(tryWord):
                # 若子串长度为1，跳出循环
                if len(tryWord) == 1:
                    break
                # 截掉子串尾部一个字，用剩余部分到字典中匹配
                tryWord = tryWord[0:len(tryWord) - 1]
            # 将匹配成功的词加入到分词列表中
            segList.append(tryWord)
            # 将匹配成功的词从待分词字符串中去除，继续循环，直到分词完成
            str = str[len(tryWord):]
        seg_text.append(segList)
    return seg_text

def output_2_file(seg_text, out_text):
    fo = open(out_text, 'w')
    for segList in seg_text:
        for word in segList:
            fo.write(word)
            if not segList.index(word) == len(segList) - 1:
                fo.write(' ')
        fo.write('\n')


def main():
    seg_text = forward_maximum_matching("dic.txt", '199801_sent.txt')
    output_2_file(seg_text, 'seg_FMM.txt')

if __name__ == '__main__':
    main()
