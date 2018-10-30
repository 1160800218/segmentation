import math
from codes.segmentation_LM import read, get_DAG


def calc_bigram(sentence, DAG, route, lfreq, pfreq):
    N = len(sentence) - 5
    route[(N, N)] = (0, 0)
    prewords = {}
    keys = pfreq.keys()
    for key in keys:
        prewords[key] = [word for word in pfreq[key].keys()]
    for index in range(N-1, -1, -1):
        for x in DAG[index]:
            word = sentence[index:x+1]
            for j in range(len(prewords.get(word, ""))):
                pre_word = prewords[word][j]
                pre_index = index - len(pre_word)
                numer = pfreq.get(word, {}).get(sentence[pre_index:index], 0)   # 分子
                denom = lfreq.get(sentence[pre_index:index], 0)                 # 分母
                if not lfreq.get(sentence[pre_index:index], 0) == 0:            # 前一位词在词典中存在
                    route[(pre_index, index)] = ((math.log(numer or 1) - math.log(denom or 1) + route.get((index, x+1),(0,0))[0]), x)


def segmentation_bg(filepath, seg, lfreq, pfreq):
    sent_list = read(filepath).split('\n')
    for sent in sent_list:
        if sent != "":
            sent = '<BOS>' + sent + '<EOS>'
        N = len(sent)-5
        DAG = get_DAG(sent, lfreq)
        route = {}
        temp_seg = []
        calc_bigram(sent, DAG, route, lfreq, pfreq)
        keys = list(route.keys())
        labels = {}
        for key in keys[::-1]:
            labels[key[0]] = key[1]
        starts = list(labels.keys())
        ends = list(labels.values())
        starts.reverse()
        ends.reverse()
        start = 5
        temp_end = 6
        end = 5
        while end < N-1:
            end = labels.get(start, 0)
            if end == 0:
                end = starts[ends.index(temp_end) - 1]
            temp_seg.append(sent[start:end])
            temp_end = end
            start = end
        temp_seg.append(sent[end:end + 1])
        if temp_seg == [""]:
            seg.append([])
        else:
            seg.append(temp_seg)