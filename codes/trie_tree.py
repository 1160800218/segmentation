class TrieNode:
    def __init__(self, character, terminal, children):
        self.character = character
        self.terminal = terminal
        self.children = children

    # 返回当前节点Terminal的值
    def is_terminal(self):
        return self.terminal

    # 设置当前节点Terminal的值
    def set_terminal(self, terminal):
        self.terminal = terminal

    # 获得当前节点的字符
    def get_character(self):
        return self.character

    # 设置当前节点的字符
    def set_character(self, character):
        self.character = character

    # 获取当前节点的子节点
    def get_children(self):
        return self.children

    # 获取指定的一个子节点
    def get_child(self, character):
        chars = [x.get_character() for x in self.children]
        low = 0
        up = len(chars)
        while(low < up):
            mid = int((low + up)/2)
            if(chars[mid] == character):
                return self.children[mid]
            elif(ord(chars[mid]) < ord(character)):
                low = mid + 1
            else:
                up = mid - 1
        return None

    # 获取子节点，若不存在则创建一个
    def get_child_if_not_exist_then_create(self, character):
        child = self.get_child(character)
        if not child:
            child = TrieNode(character, False, [])
            self.add_child(child)
        return child

    # 添加子节点
    def add_child(self, child):
        self.children.append(child)

    # 移除子节点
    def remove_child(self, child):
        self.children.remove(child)

# 根节点
ROOT_NODE = TrieNode('', False, [])

# 在trie树中查找
def contain(astr):
    # 去除空格
    astr = astr.replace(' ', '')
    # 若长度小于1，则查找失败
    if len(astr) < 1:
        return False
    # 从根节点开始
    node = ROOT_NODE
    # 逐个字符查找
    for i in astr:
        child = node.get_child(i)
        if not child:
            return False
        else:
            # 切换当前节点
            node = child
    #在trie树中存在字符串，若是完整字符串则查找成功，否则查找失败
    return node.is_terminal()


# 添加所有词
def add_all(word_list):
    for word in word_list:
        add(word)

# 向trie中添加词
def add(word):
    # 去除空格
    word = word.replace(' ', '')

    # 若长度小于1，则不添加
    if len(word) < 1:
        return

    # 从根节点开始
    node = ROOT_NODE

    # 逐个字符查找，遇到不存在的字符则创建
    for i in word:
        child = node.get_child_if_not_exist_then_create(i)
        # 切换当点节点
        node = child

    # 添加完成，设置最后一个节点为合法
    node.set_terminal(True)

