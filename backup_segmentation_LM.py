# coding=utf-8
import time
import math
# from forward_maximum_matching import output_2_file
def output_2_file(seg_text, out_text):
    temp = []
    for segList in seg_text:
        if not segList:
            temp.append(''.join(segList))
        else:
            temp.append('/ '.join(segList) + '/ ')
    output_seg = '\n'.join(temp)
    fo = open(out_text, 'w')
    fo.write(output_seg)
    fo.close()

def read(filepath):
    file = open(filepath, "r")
    try:
        b = file.read()
    finally:
        file.close()
    return b


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


# 获得前词词典
def pro_prefix_dictionary():
    pfreq={}
    with open('newdic.txt', 'r') as f:
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


# 基于一元语法（最大词频）
def calc_max_route(sentence, DAG, route, lfreq, ltotal):
    N = len(sentence)
    route[N] = (0, 0)
    logtotal = math.log(ltotal)     # 取对数运算避免溢出，+1进行平滑处理
    for index in range(N - 1, -1, -1):
        route[index] = max((math.log(lfreq.get(sentence[index:x+1], 0) or 1) - logtotal + route[x+1][0], x) for x in DAG[index])    # 动态规划实现最大词频搜索，+1进行平滑处理




# 基于二元语法
def calc_bigram(sentence, DAG, route, lfreq, pfreq, prewords):
    '''
    生成route
    '''
    N = len(sentence) - 5
    print(sentence)
    route[(N, N)] = (0, 0)
    for index in range(N-1, 4, -1):
        max=0
        for x in DAG[index]:
            word = sentence[index:x+1]
            pre_len = calc_pre_len(prewords.get(word, ""))
            for j in pre_len:
                pre_index = index - j
                numer = pfreq.get(word, {}).get(sentence[pre_index:index], 0)   # 分子
                denom = lfreq.get(sentence[pre_index:index], 0)                 # 分母
                if not lfreq.get(sentence[pre_index:index], 0) == 0:            # 前一位词在词典中存在
                    route[(pre_index, index)] = ((math.log(numer or 1) - math.log(denom or 1) + route.get((index, x+1),(0,0))[0]), x)


def calc_pre_len(list):
    lengths = set()
    for i in list:
        lengths.add(len(i))
    return lengths

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


def segmentation_bg(filepath, seg, lfreq, pfreq):
    '''
    根据route分词
    '''
    prewords = {}
    keys = pfreq.keys()
    for key in keys:
        prewords[key] = [word for word in pfreq[key].keys()]

    sent_list = read(filepath).split('\n')
    for sent in sent_list:
        if sent != "":
            sent = '<BOS>' + sent + '<EOS>'
        N = len(sent)-5
        DAG = get_DAG(sent, lfreq)
        route = {}
        temp_seg = []
        calc_bigram(sent, DAG, route, lfreq, pfreq, prewords)
        keys = list(route.keys())
        labels = {}
        for key in keys[::-1]:
            labels[key[0]] = key[1]
        starts = list(labels.keys())
        ends = list(labels.values())
        starts.reverse()
        ends.reverse()
        ends.append(-1)
        start = 5
        temp_end = -1
        end = 5
        while end < N-1:
            end = labels.get(start, 0)
            if end == 0:
                end = starts[ends.index(temp_end) - 1]
            temp_seg.append(sent[start:end])
            temp_end = end
            start = end
        if end < N:
            temp_seg.append(sent[end:end + 1])
        seg.append(temp_seg)


def main():
    # lfreq, ltotal = build_pfdict('dic.txt')
    # print(lfreq, ltotal)
    # seg = []
    # start_time = time.time()
    # segmentation_mr('199801_sent.txt', seg, lfreq, ltotal)
    # end_time = time.time()
    # print(round((end_time - start_time)*1000), 'ms')
    # output_2_file(seg, 'seg_LM.txt')
    # # 分词评价
    # analysis('seg_LM.txt', 'golden_standard.txt')

    lfreq, ltotal = build_pfdict('dic.txt')
    pfreq = pro_prefix_dictionary()

    seg = []
    start_time = time.time()
    segmentation_bg('199801_sent.txt', seg, lfreq, pfreq)
    end_time = time.time()
    print(round((end_time - start_time) * 1000), 'ms')
    output_2_file(seg, 'seg_LM_bg.txt')


    # 测试代码
    # test_seg = []
    # test_route = {}
    # DAG = get_DAG('', lfreq)
    # print(DAG)
    # test_calc('', DAG, test_route, test_seg, lfreq, ltotal)
    # print(test_route)
    # print(test_seg)

if __name__ == '__main__':
    main()