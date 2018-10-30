# coding=utf-8
import time
import math
from codes.helper import output_2_file, read
from codes.performance_analysis import analysis
from codes.path import *


# 获得前缀词典和总词数
def build_pfdict(dic_path):
    lfreq = {}      # 保存前缀词典中的词和词频
    ltotal = 0      # 保存总词数
    str_dic = read(dic_path).split('\n')
    for line in str_dic:
        # 保存离线词典中的词和词频
        word, freq = line.split(' ')[0:2]
        freq = int(freq)
        lfreq[word] = freq
        ltotal += freq
        # 对于离线词典中的每个词，获取其前缀词
        for i in range(len(word)):
            wfrag = word[:i + 1]
            if wfrag not in lfreq:
                lfreq[wfrag] = 0
    return lfreq, ltotal


# 获得关联词词典
def pro_prefix_dictionary():
    pfreq={}
    with open(conj_dic, 'r') as f:
        line = f.readline()
        while len(line)>0:
            word1, word2, freq = line.split()[0:3]
            freq = int(freq)
            if word1 not in pfreq.keys():
                value_dic = {}
                pfreq[word1] = value_dic
                value_dic[word2] = freq
            else:
                pfreq[word1][word2] = freq
            line=f.readline()
    return pfreq


# 获得有向无环图DAG
def get_DAG(sentence, lfreq):
    DAG = {}
    N = len(sentence)
    for k in range(N):
        temp_list = []
        i = k
        frag = sentence[k]
        while i < N and frag in lfreq:
            if lfreq[frag] > 0:
                temp_list.append(i)
            i += 1
            frag = sentence[k:i+1]
        if not temp_list:
            temp_list.append(k)
        DAG[k] = temp_list
    return DAG


##########################
# 基于一元语法（最大词频）#
##########################

# 获得最优路径并保存在route
def calc_max_route(sentence, DAG, route, lfreq, ltotal):
    N = len(sentence)
    route[N] = (0, 0)
    logtotal = math.log(ltotal)     # 取对数运算避免溢出，+1进行平滑处理
    for index in range(N - 1, -1, -1):
        route[index] = max((math.log(lfreq.get(sentence[index:x+1], 0) or 1) - logtotal + route[x+1][0], x) for x in DAG[index])    # 动态规划实现最大词频搜索，+1进行平滑处理

def segmentation_mr(filepath, seg, lfreq, ltotal):
    sent_list = read(filepath).split('\n')
    for sent in sent_list:
        N = len(sent)
        DAG = get_DAG(sent, lfreq)
        # print(DAG)
        route = {}
        temp_seg = []
        calc_max_route(sent, DAG, route, lfreq, ltotal)
        start = 0
        while start < N:
            end = route[start][1]
            temp_seg.append(sent[start:end + 1])
            start = end + 1
        seg.append(temp_seg)


##########################
# 基于二元语法（条件概率）#
##########################

# 计算条件概率的对数
# return float: 条件概率的对数
def calc_p(pre_word, last_word, lfreq, pfreq):
    denom = lfreq.get(pre_word, 0)
    numer = pfreq.get(last_word, {}).get(pre_word, 0)
    return math.log(numer or 0.0000001) - math.log(denom or 1)      # 平滑处理


# 词图最长路径分词
# return list: seg 已分词文本列表
def calc_bigram_by_graph(sentence, DAG, route, lfreq, pfreq):
    ###################
    # 生成有向无环词图 #
    ###################
    N = len(sentence) - 5       # 减去<EOS>的长度
    start = 5                   # 跳过<BOS>从第一个字开始
    pre_graph = {}              # 每个词节点存有下一个相连词的词图
    last_graph = {}             # 每个词节点存有上一个相连词的词图
    BOS = {}                    # <BOS>的下一词词典
    for x in DAG[5]:
        BOS[(5, x+1)] = calc_p("<BOS>", sentence[5:x+1], lfreq, pfreq)
    pre_graph["<BOS>"] = BOS    # 初始化
    # 遍历DAG生成词图
    while start < N:
        ends = DAG[start]
        for end in ends:
            pre_word = sentence[start:end + 1]      # wi-1
            next_start = end+1
            next_ends = DAG[end+1]
            temp_dict_pre = {}
            for next_end in next_ends:
                last_word = sentence[next_start:next_end+1]     # wi
                if last_word == "<":
                    last_word = "<EOS>"
                    temp_dict_pre[last_word] = calc_p(pre_word, last_word, lfreq, pfreq)
                else:
                    temp_dict_pre[(next_start, next_end+1)] = calc_p(pre_word, last_word, lfreq, pfreq)
            pre_graph[(start, end + 1)] = temp_dict_pre
        start += 1

    # 求last_graph
    keys = list(pre_graph.keys())
    for key in keys:
        nodes = pre_graph[key].keys()
        for node in nodes:
            last_graph[node] = last_graph.get(node, list())
            last_graph[node].append(key)

    #####################
    # 动态规划求最长路径 #
    #####################
    keys.append("<EOS>")
    for key in keys:
        if key == "<BOS>":
            route[key] = (0.0, '<BOS>')
        else:
            nodes = last_graph.get(key, list())
            if len(nodes) == 0:
                route[key] = (-65507, '<BOS>')      # 平滑处理
                continue
            route[key] = max((pre_graph[node][key] + route[node][0], node) for node in nodes)
    # print(route)
    # 回溯获得最长路径
    seg = []
    position = '<EOS>'
    while True:
        position = route[position][1]
        if position == '<BOS>':
            break
        seg.insert(0, sentence[position[0]:position[1]])
    # print(seg)
    return seg

def segmentation_graph(filepath, seg, lfreq, pfreq):
    sent_list = read(filepath).split('\n')
    for sent in sent_list:
        if sent != "\r\n":
            sent = '<BOS>' + sent + '<EOS>'
        DAG = get_DAG(sent, lfreq)
        route = {}
        temp_seg = calc_bigram_by_graph(sent, DAG, route, lfreq, pfreq)
        seg.append(temp_seg)


# 测试一元文法分词并进行时间及性能分析
def test_1_gram(in_path, out_path):
    lfreq, ltotal = build_pfdict(dic_path)
    # print(lfreq, ltotal)
    seg = []
    start_time = time.time()
    segmentation_mr(in_path, seg, lfreq, ltotal)
    end_time = time.time()
    print(round((end_time - start_time) * 1000), 'ms')
    output_2_file(seg, out_path)
    # 分词评价
    analysis(out_path, gold_std_path)


# 测试二元文法分词并进行时间和性能分析
def test_2_gram(in_path, out_path):
    lfreq, ltotal = build_pfdict(dic_path)
    pfreq = pro_prefix_dictionary()
    seg = []
    start_time = time.time()
    segmentation_graph(in_path, seg, lfreq, pfreq)
    end_time = time.time()
    print(round((end_time - start_time) * 1000), 'ms')
    output_2_file(seg, out_path)
    # 分词评价
    analysis(out_path, gold_std_path)


def main():
    test_1_gram(sent_path, seg_LM_path)
    test_2_gram(sent_path, seg_LM_path)


if __name__ == '__main__':
    main()