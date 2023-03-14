# https://github.com/yizuodi/SYSU2022_AI
# 基于GPL 2.0协议开源，如您使用到了本仓库中的代码，请遵循协议要求开源。
import time

expanded = {}
# 预处理出 2^64-1挖掉第i个与第j个位置的状态，方便运算
pre1 = [[0 for i in range(80)] for j in range(80)]
for i in range(80):
    for j in range(80):
        pre1[i][j] = (1 << 64) - 1 - (15 << i) - (15 << j)

# 把64位截成4段，每段16位，预处理出每个16位在不同段时的贡献，实际计算时就可以只需要4的复杂度
pre2 = [[0 for i in range(1 << 16)] for j in range(4)]
for k in range(4):
    for i in range(1 << 16):
        for j in range(4):
            y = ((i >> (j << 2)) & 15) - 1
            if y == -1:
                continue
            pre2[k][i] += abs((y >> 2) - k) + abs((y & 3) - j)


def work(x):  # 启发式函数：曼哈顿距离和
    tmp = 0
    for i in range(4):
        tmp += pre2[i][(x >> (i << 4)) & ((1 << 16) - 1)]
    return tmp


def translate(A):  # 将列表转换为一个二进制64位数
    tmp = 0
    for i in range(16):
        tmp += (A[i] << (i << 2))
    return tmp


# 通过位运算算出新状态
def exchange(x, y, z):  # 交换y和z位置的数，通常y会是我们找到的0的位置
    y <<= 2
    z <<= 2
    return (x & pre1[y][z]) | (((x >> z) & 15) << y)


# 找到0的位置
def pos_0(x):
    for i in range(16):  # 对64位，每4位对比一次
        if ((x >> (i << 2)) & 15) == 0:
            return i


# 用递归方式输出方案
def outputresult(x, step):
    if expanded[x] != -1:  # 先不断回溯，从前面的步骤到后面的步骤输出
        outputresult(exchange(x, pos_0(x), expanded[x]), step - 1)
    outputfile.write("第" + str(step) + "步：\n")
    for i in range(16):
        outputfile.write(str((x >> (i << 2)) & 15) + " ")
        if i == 3 or i == 7 or i == 11 or i == 15:
            outputfile.write("\n")
    outputfile.write("\n")


def astar(S, E):  # 初始状态与最终状态
    state = [[] for i in range(128)]  # 进行状态记录

    cnt = 0  # 测试用
    exist = 0
    state[work(S)].append([S, pos_0(S), -1, 0])  # 分别对应的是64位表示的状态，当前0的位置，上一级状态0的位置，走到当前状态路径的长度
    while True:
        while not state[exist]:
            exist += 1
        [x, y, last_p_0, steps] = state[exist][-1]  # 将state中的值转储
        state[exist].pop()  # 去除现有的”当前状态路径长度“，等待更新
        if x in expanded:
            continue
        expanded[x] = last_p_0  # 一致代价搜索的环检测

        if x == E:  # 到达了最终状态就输出并结束
            print("共", steps, "步")
            outputfile.write("共" + str(steps) + "步,耗费" + str(time.perf_counter() - timer) + "秒\n")
            outputresult(x, steps)  # 输出到文件中
            return

        cnt += 1  # 测试用
        if cnt % 100000 == 0:  # 测试用
            print(cnt, steps, work(x), steps + work(x))  # 测试用，实时观测程序运行进度

        # 探索当前点的4个方向，同时防止返回上一级的状态
        if y - 4 >= 0 and y - 4 != last_p_0:  # 上
            state[steps + 1 + work(exchange(x, y, y - 4))].append([exchange(x, y, y - 4), y - 4, y, steps + 1])

        if y & 3 and y - 1 != last_p_0:  # 左
            state[steps + 1 + work(exchange(x, y, y - 1))].append([exchange(x, y, y - 1), y - 1, y, steps + 1])

        if y & 3 != 3 and y + 1 != last_p_0:  # 右
            state[steps + 1 + work(exchange(x, y, y + 1))].append([exchange(x, y, y + 1), y + 1, y, steps + 1])

        if y + 4 < 16 and y + 4 != last_p_0:  # 下
            state[steps + 1 + work(exchange(x, y, y + 4))].append([exchange(x, y, y + 4), y + 4, y, steps + 1])


f = open("input.txt")
outputfile = open("output_a_star.txt", "w")

data = []
for i in range(4):
    data += list(map(int, f.readline().split()))

timer = time.perf_counter()  # 用于计时
end_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  # 目标结果
astar(translate(data), translate(end_result))  # 使用A*算法处理
print("用时：", time.perf_counter() - timer, "秒")
print("步骤已输出到指定文件中")
