class Predicate:  # 我们先定义一个谓词类来对子句中的谓词进行存储
    element = []

    def __init__(self, str_in):
        self.element = []
        if len(str_in) != 0:
            if str_in[0] == ',':  # 把原来用于分隔谓词的 , 去掉
                str_in = str_in[1:]
            tmp = ""
            for i in range(len(str_in)):
                tmp += str_in[i]
                if str_in[i] == '(' or str_in[i] == ',' or str_in[i] == ')':
                    self.element.append(tmp[0:-1])
                    tmp = ""

    def new(self, list_in):
        for i in range(len(list_in)):
            self.element.append(list_in[i])

    def rename(self, old_name, new_name):
        for i in range(len(old_name)):
            j = 1
            while j < len(self.element):
                if self.element[j] == old_name[i]:
                    self.element[j] = new_name[i]
                j = j + 1

    def get_pre(self):  # 返回谓词的前缀是否为"¬"
        return self.element[0][0] == "¬"

    def get_name(self):  # 返回谓词名称
        if self.get_pre():
            return self.element[0][1:]
        else:
            return self.element[0]


def print_clause(clause_in):  # 从谓词列表打印出原来的子句
    tmp = ""
    if len(clause_in) > 1:
        tmp = tmp + "("
    for i in range(len(clause_in)):
        tmp = tmp + clause_in[i].element[0] + "("
        for j in range(1, len(clause_in[i].element)):
            tmp = tmp + clause_in[i].element[j]
            if j < len(clause_in[i].element) - 1:
                tmp = tmp + ","
        tmp = tmp + ")"
        if i < len(clause_in) - 1:
            tmp = tmp + ","
    if len(clause_in) > 1:
        tmp = tmp + ")"
    if (tmp != ""):
        print(tmp)


def print_msg(key, i, j, old_name, new_name, set_of_clause):
    tmp = str(len(set_of_clause)) + ": R[" + str(i + 1)  # 输出相关信息如 R[A1= 1 ,A2= 6 a ](x = tony,)
    if len(new_name) == 0 and len(set_of_clause[i]) != 1:
        tmp = tmp + chr(key + 97)
    tmp = tmp + ", " + str(j + 1) + chr(key + 97) + "]("
    for k in range(len(old_name)):
        tmp = tmp + old_name[k] + "=" + new_name[k]
        if k < len(old_name) - 1:
            tmp = tmp + ", "
    tmp = tmp + ") = "
    print(tmp, end="")


def end_or_not(new_clause, set_of_clause):
    if len(new_clause) == 0:  # 新生成的new_clause已经为空
        print("[]")
        return True
    if len(new_clause) == 1:  # 查找已有的子句中是否存在与新子句互补
        for i in range(len(set_of_clause) - 1):  # set_of_clause[j]超过一个谓词的取或的子句
            if len(set_of_clause[i]) == 1 and new_clause[0].get_name() == set_of_clause[i][0].get_name() and new_clause[0].element[1:] == \
                    set_of_clause[i][0].element[1:] and new_clause[0].get_pre() != set_of_clause[i][0].get_pre():
                print(len(set_of_clause) + 1, ": R[", i + 1, ", ", len(set_of_clause), "]() = []", sep="")
                return True
    return False  # 不符合条件不结束


def main():
    set_of_clause = []
    print("首先，请输入子句数量：")
    num_of_clause = input()
    print("下面，请输入", num_of_clause, "条子句：")
    for i in range(int(num_of_clause)):
        clause_in = input()
        if clause_in == "":
            print("输入过程有误（输入为空），程序将退出")
            return
        if clause_in[0] == '(':  # 如果子句最左侧有括号，则去掉
            clause_in = clause_in[1:-1]
        clause_in = clause_in.replace(' ', '')  # 如果子句内有空格，则去掉
        set_of_clause.append([])  # 一个列表，将输入的子句拆分存储
        tmp = ""  # 用于拆分子句使用的中间变量
        for j in range(len(clause_in)):  # 拆分存储在列表里
            tmp += clause_in[j]
            if clause_in[j] == ')':  # 用')'作为结尾分割成多个谓词公式
                if j + 1 != num_of_clause:
                    clause_tmp = Predicate(tmp)  # 创造一个谓词公式类Predicate的变量
                    set_of_clause[i].append(clause_tmp)  # 加入到子句集的第i个子句中
                tmp = ""

    for i in range(len(set_of_clause)):  # 先输出刚刚输入的子句集
        print_clause(set_of_clause[i])

    status = True
    while status:
        for i in range(len(set_of_clause)):
            if not status:
                break
            if len(set_of_clause[i]) == 1:  # 只对一个谓词的子句set_of_clause[i]进行下面处理
                for j in range(0, len(set_of_clause)):  # 和其它的子句进行比较
                    if not status:
                        break
                    if i == j:  # 不和自己比较
                        continue
                    old_name = []
                    new_name = []  # 将自由变量转换为约束变量
                    key = -1  # -1表示该子句的同名谓词不能进行消去
                    for k in range(len(set_of_clause[j])):  # 在子句set_of_clause[j]中找相同的谓词，且可以消去，设置key为其位置
                        if set_of_clause[i][0].get_name() == set_of_clause[j][k].get_name() and set_of_clause[i][
                            0].get_pre() != set_of_clause[j][k].get_pre():
                            key = k
                            for l in range(len(set_of_clause[j][k].element) - 1):  # 找到可以换名的变量并记录
                                if len(set_of_clause[j][k].element[l + 1]) == 1:  # 是自由变量
                                    old_name.append(set_of_clause[j][k].element[l + 1])
                                    new_name.append(set_of_clause[i][0].element[l + 1])
                                elif len(set_of_clause[i][0].element[l + 1]) == 1:
                                    old_name.append(set_of_clause[i][k].element[l + 1])
                                    new_name.append(set_of_clause[j][0].element[l + 1])
                                elif set_of_clause[j][k].element[l + 1] != set_of_clause[i][0].element[l + 1]:
                                    key = -1
                                    break
                            break
                    if key == -1:  # 否则换名 消去 生成新子句
                        continue
                    new_clause = []  # 记录生成的新子句
                    for k in range(len(set_of_clause[j])):
                        if k != key:  # 位置为key的已经被消去了，所以不在新子句里
                            p = Predicate("")
                            p.new(set_of_clause[j][k].element)
                            p.rename(old_name, new_name)
                            new_clause.append(p)
                    if len(new_clause) == 1:  # 判断是否生成的子句是否与已有重复（不判断是否生成了子句）
                        for k in range(len(set_of_clause)):
                            if len(set_of_clause[k]) == 1 and new_clause[0].element == set_of_clause[k][0].element:
                                key = -1
                                break
                    if key == -1:  # 如果生成的子句已存在，跳过加入子句集的过程
                        continue
                    set_of_clause.append(new_clause)  # 生成的新的子句加入的子句集中
                    print_msg(key, i, j, old_name, new_name, set_of_clause)  # 输出生成新子句的相关信息
                    print_clause(new_clause)  # 输出该新子句
                    if end_or_not(new_clause, set_of_clause):  # 判断是否应该结束归结过程
                        status = False
                        break
            #  下面的部分，是为了解决测试样例之外的一些问题 因为上面的程序用到的规则是 (A)and(¬A,B,C,...) => (B,C,...)
            else:  # set_of_clause[i]是有多个谓词的子句
                for j in range(0,
                               len(set_of_clause)):  # 找可使用规则 (¬A,B,C,...)and(A,B,C,...) => (B,C,...) 的子句set_of_clause(j)
                    key = -1
                    if i != j and len(set_of_clause[i]) == len(set_of_clause[j]):
                        for k in range(len(set_of_clause[i])):
                            if set_of_clause[i][k].element == set_of_clause[j][k].element:
                                # 实际情况中，应该进一步考虑各种可进行变量换名的情况
                                continue
                            elif set_of_clause[i][k].get_name() == set_of_clause[j][k].get_name() and set_of_clause[i][
                                                                                                          k].element[
                                                                                                      1:] == \
                                    set_of_clause[j][k].element[1:]:
                                # 需要在这里判断变量换名的情况
                                if key != -1:  # 表明已经存在一处不等的情况，无法使用该规则进行消除
                                    key = -1
                                    break
                                key = k
                            else:
                                key = -1
                                break
                    if key == -1:
                        continue
                    new_clause = []
                    for k in range(len(set_of_clause[i])):
                        if k != key:
                            p = Predicate("")
                            p.new(set_of_clause[j][k].element)
                            new_clause.append(p)
                    if len(new_clause) == 1:  # 判断是否生成的子句是否与已有重复（不判断是否生成了子句）
                        for k in range(len(set_of_clause)):
                            if len(set_of_clause[k]) == 1 and new_clause[0].element == set_of_clause[k][0].element:
                                key = -1
                                break
                    if key == -1:  # 如果生成的子句已存在，跳过加入子句集的过程
                        continue
                    set_of_clause.append(new_clause)
                    print_msg(key, i, j, [], [], set_of_clause)  # 输出生成新子句的相关信息
                    print_clause(new_clause)  # 输出该新子句
                    if end_or_not(new_clause, set_of_clause):  # 判断是否应该结束归结过程
                        status = False
                        break
    print("Success!")


if __name__ == '__main__':
    main()
