# https://github.com/yizuodi/SYSU2022_AI
# 基于GPL 2.0协议开源，如您使用到了本仓库中的代码，请遵循协议要求开源。
import time

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


f = open("input.txt")
outputfile = open("output_ida_star.txt", "w")

data = []
for i in range(4):
    data += list(map(int, f.readline().split()))

timer = time.perf_counter()  # 用于计时
end_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  # 目标结果
S = translate(data)  # 将列表转换成64位表示状态
E = translate(end_result)

lim = -2  # 防止越界的限制
state = []
finished = 0  # 标识是否到达最终状态，控制while循环
while not finished:
    lim += 2
    while state:
        state.pop()
    state.append([work(S), S, pos_0(S), 0])  # 分别为启发式函数，64位状态，0的位置，g(x)（或者说步数）
    later_state = []
    expanded = {}

    while state:
        [xx, x, y, steps] = state[-1]  # 取栈顶，分别为启发式函数，64位状态，0的位置，g(x)(或者说步数)

        if x in expanded:  # 对于dfs中的回溯过程，不执行拓展
            state.pop()
            del expanded[x]
            continue
        expanded[x] = 1

        if x == E:  # 到达了最终状态就输出并结束，并利用栈内信息输出路径
            print("共", steps, "步")
            outputfile.write("共" + str(steps) + "步,耗费" + str(time.perf_counter() - timer) + "秒\n")

            now_output = 0  # 从第0步开始输出
            last = state[0]
            for i in state:
                steps = i[3]  # 读取该state中的g(x)
                if steps > now_output:  # 筛选掉state中多出的部分
                    x = last[1]
                    outputfile.write("第" + str(now_output) + "步：\n")
                    now_output += 1
                    for j in range(16):  # 从该步的64位状态中解析并写入文件
                        outputfile.write(str((x >> (j << 2)) & 15) + " ")
                        if j == 3 or j == 7 or j == 11 or j == 15:
                            outputfile.write("\n")
                    outputfile.write("\n")
                last = i
            finished = 1  # 表示ida_star过程结束
            break  # 从while循环跳出

        # 探索当前点的4个方向,进行路径检测（判断估计函数是否越界）
        if y - 4 >= 0:  # 上
            if exchange(x, y, y - 4) not in expanded and work(exchange(x, y, y - 4)) + steps + 1 <= lim:
                later_state.append([work(exchange(x, y, y - 4)), exchange(x, y, y - 4), y - 4, steps + 1])

        if y & 3:  # 左
            if exchange(x, y, y - 1) not in expanded and work(exchange(x, y, y - 1)) + steps + 1 <= lim:
                later_state.append([work(exchange(x, y, y - 1)), exchange(x, y, y - 1), y - 1, steps + 1])

        if y & 3 != 3:  # 右
            if exchange(x, y, y + 1) not in expanded and work(exchange(x, y, y + 1)) + steps + 1 <= lim:
                later_state.append([work(exchange(x, y, y + 1)), exchange(x, y, y + 1), y + 1, steps + 1])

        if y + 4 < 16:  # 下
            if exchange(x, y, y + 4) not in expanded and work(exchange(x, y, y + 4)) + steps + 1 <= lim:
                later_state.append([work(exchange(x, y, y + 4)), exchange(x, y, y + 4), y + 4, steps + 1])

        later_state.sort()  # 为后继状态排序，从大到小加入栈中
        while later_state:
            state.append(later_state[-1])
            later_state.pop()

print("用时：", time.perf_counter() - timer, "秒")
print("步骤已输出到指定文件中")
