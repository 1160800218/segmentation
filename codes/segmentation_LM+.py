# coding=utf-8
import time
import math
from codes.performance_analysis import analysis
from codes.helper import read, output_2_file
from codes.path import *


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


def get_forward_DAG(DAG):
    forward_dag={}
    for i in range(len(DAG)):
        forward_dag[i]=[]
        for key in DAG.keys():
            if i in DAG[key]:
                forward_dag[i].append(key)
    return forward_dag


# 基于二元语法
def calc_bigram(sentence, DAG, forward_DAG,route, lfreq, pfreq, prewords):
    '''
    生成route
    '''
    N = len(sentence) - 5
    route[(N, N)] = (0, 0)
    for index in range(N-1, 4, -1):
        for x in forward_DAG[index-1]:      # 前词是sentence[x:index],要求route[x,index]=?
            max_P=-1000000
            max_y=0
            for y in DAG[index]:    # 后词是sentence[index:y+1],route[x,index]=(P,y+1)
                numer = pfreq.get(sentence[index:y+1], {}).get(sentence[x:index], 0)  # 分子
                denom = lfreq.get(sentence[x:index], 0)  # 分母
                tmp_P=math.log(numer or 0.000001) - math.log(denom or 1) + route.get((index, y+1),(0,0))[0]
                if tmp_P>max_P:
                    max_P=tmp_P
                    max_y=y
            route[x,index]=(max_P,max_y+1)


def calc_pre_len(list):
    lengths = set()
    for i in list:
        lengths.add(len(i))
    return lengths


def segmentation_bigram(filepath, seg, lfreq, pfreq):
    '''
    根据route分词
    '''
    prewords = {}
    keys = pfreq.keys()
    for key in keys:
        prewords[key] = [word for word in pfreq[key].keys()]

    sent_list = read(filepath).split('\n')
    for sent in sent_list:
        if sent == '':
            seg.append([])
            continue
        if sent != "":
            sent = '<BOS>' + sent + '<EOS>'
        N = len(sent)-5
        DAG = get_DAG(sent, lfreq)
        forward_DAG=get_forward_DAG(DAG)
        route = {}
        temp_seg = []
        calc_bigram(sent, DAG,forward_DAG, route, lfreq, pfreq, prewords)   # 建立这句话的route
        # print(route)

        pos0=pos1=0
        for key in route.keys():
            if key[0] == 4:
                pos0=key[1]
                pos1=route[key][1]
                break
        temp_seg.append(sent[pos0:pos1])
        while pos1 != N:
            value=route[(pos0,pos1)]
            pos0=pos1
            pos1=value[1]
            temp_seg.append(sent[pos0:pos1])
        seg.append(temp_seg)
        # print(seg)


def main():
    lfreq, ltotal = build_pfdict(dic_path)
    pfreq = pro_prefix_dictionary()

    seg = []
    start_time = time.time()
    segmentation_bigram(sent_path, seg, lfreq, pfreq)
    end_time = time.time()
    print(round((end_time - start_time) * 1000), 'ms')
    output_2_file(seg, seg_LM_bg_path)

    analysis(seg_LM_bg_path, gold_std_path)


if __name__ == '__main__':
    main()