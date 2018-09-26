# coding=utf-8
import re


# 从文本中构建词典
def build_dictionary_from_text(textname):
    fi = open(textname, "r")
    text_lines = fi.readlines()
    dictionary = dict()                         # 词典
    words = set()                               # 存放词， 用于判断该词是否出现过
    for line in text_lines:
        if not re.match(r'\r*\n$', line):
            strings = line[23:].split("  ")         # 过滤开头并划分词
            for string in strings:
                if not re.match(r'\r*\n$', string):
                    string = string.split("/")      # 划分词语和词性
                    word = (string[0], string[1])   # 注意：list不是hashable， 不可用于not in查找，所以用元组
                    if word not in words:
                        words.add(word)
                        dictionary[word] = 1        # 词频
                    else:
                        # print dictionary[word]
                        dictionary[word] += 1
    fi.close()
    fo = open("dic.txt", "w")
    for word in dictionary:
        fo.write(word[0])
        fo.write(" ")
        fo.write(str(dictionary[word]))
        fo.write(" ")
        fo.write(word[1])
        fo.write("\n")
    fo.close()


def main():
    build_dictionary_from_text("199801_seg.txt")


if __name__ == "__main__":
    main()
