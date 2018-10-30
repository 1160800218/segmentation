# 读取文件
# return 未处理文本
def read(filepath):
    file = open(filepath, "r")
    try:
        b = file.read()
    finally:
        file.close()
    return b


# 输出分词结果到文件
def output_2_file(seg_text, out_txt):
    temp = []
    for segList in seg_text:
        if not segList:
            temp.append(''.join(segList))
        else:
            temp.append('/ '.join(segList) + '/ ')
    output_seg = '\n'.join(temp)
    fo = open(out_txt, 'w')
    fo.write(output_seg)
    fo.close()


# 二分查找
def BinSearch(word, list):
    low = 0
    up = len(list) - 1
    while low <= up:
        # matched = True
        mid = int((low + up) / 2)
        if list[mid] == word:
            return True
        elif list[mid] < word:
            low = mid + 1
        else:
            up = mid - 1
    return False


# 二叉树节点
class BSTNode:
    def __init__(self, data, lchild, rchild):
        self.data = data
        self.lchild = lchild
        self.rchild = rchild

    def get_data(self):
        return self.data

    def get_lchild(self):
        return self.lchild

    def get_rchild(self):
        return self.rchild

    def set_data(self, new_data):
        self.data = new_data

    def set_lchild(self, new_lchild):
        self.lchild = new_lchild

    def set_rchild(self, new_rchild):
        self.lchild = new_rchild