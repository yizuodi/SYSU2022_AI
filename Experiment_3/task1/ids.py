import time
# 迭代加深搜索ids Iterative Deepening Search
class Stack:  # 栈
    element = []

    def __init__(self):
        self.element = []

    def pop(self):
        self.element = self.element[:-1]

    def push(self, data):
        self.element.append(data)

    def empty(self):
        return len(self.element) == 0

    def size(self):
        return len(self.element)


class Queue:  # 队列
    element = []

    def __init__(self):
        self.element = []

    def dequeue(self):  # 出队
        self.element = self.element[1:]

    def push(self, data):
        self.element.append(data)

    def empty(self):
        return len(self.element) == 0

    def size(self):
        return len(self.element)

    def front(self):  # 队首
        return self.element[0]


d_xy = [[0, 0, 1, -1], [-1, 1, 0, 0]]  # 表示不同的方向


def ids(start_x, start_y, end_x, end_y, stack_x, stack_y, data, visited, now_depth, max_depth, high_x, high_y,
        father):  # 迭代加深
    if now_depth == max_depth:  # 使用队列记录当前最大深度的节点
        high_x.push(start_x)
        high_y.push(start_y)
        return
    for i in range(4):  # 针对上下左右四个不同方向
        x = start_x + d_xy[0][i]
        y = start_y + d_xy[1][i]
        if data[x][y] != '1' and visited[x][y] == 1:  # 可被访问
            visited[x][y] = 0
            stack_x.push(x)  # 入栈
            stack_y.push(y)
            father[x][y] = [start_x, start_y]
            if visited[end_x][end_y] == 0:  # 如果到达了终点
                return
            ids(x, y, end_x, end_y, stack_x, stack_y, data, visited, now_depth + 1, max_depth, high_x, high_y, father)
            stack_x.pop()  # 出栈
            stack_y.pop()
    if stack_x.empty():  # 如果在当前深度没找到目标位置，逐个再对最大深度节点进行ids
        while not (high_x.empty() or high_y.empty()):
            x = high_x.front()  # 获取队列中第一个点，并做出队列操作
            y = high_y.front()
            high_x.dequeue()
            high_y.dequeue()
            ids(x, y, end_x, end_y, stack_x, stack_y, data, visited, 0, max_depth, high_x, high_y, father)
    return


def readfile(filename, list_out):  # 从文件读入
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = list(line.replace("\n", ""))
            list_out.append(line)


def main():
    timer = time.perf_counter()  # 用于计时
    list_of_data = []
    readfile("MazeData.txt", list_of_data)
    start = []
    end = []
    for i in range(len(list_of_data)):
        for j in range(len(list_of_data[i])):
            if list_of_data[i][j] == "S":  # 找起点
                start.append(i)
                start.append(j)
            elif list_of_data[i][j] == "E":  # 找终点
                end.append(i)
                end.append(j)
                break
    print("起点[", start[0], ",", start[1], "]")
    print("终点[", end[0], ",", end[1], "]")

    visited = []  # 记录所有从起点出发可访问到的点，0代表可访问到（已被访问），1代表不可访问到（或者未被访问），参考边界用1表示
    way = []  # 记录从起点出发到终点的路径上的点
    father = []  # 用于记录某点的父亲节点是谁，如father[x][y] = [a][b] ,表示是从(a,b)出发访问到(x,y)
    for i in range(len(list_of_data)):
        temp = [1] * len(list_of_data[0])
        visited.append(temp[:])
        way.append(temp[:])
        temp = [[]] * len(list_of_data[0])
        father.append(temp[:])
    visited[start[0]][start[1]] = 0  # 表示从起点出发，起点是可达的

    stack_x, stack_y = Stack(), Stack()  # 用于记录未访问的可达点的坐标
    high_x, high_y = Queue(), Queue()  # 用于存储ids中处于最大深度的可达点的坐标
    ids(start[0], start[1], end[0], end[1], stack_x, stack_y, list_of_data, visited, 0, 10, high_x, high_y, father)

    x, y = end[0], end[1]
    while len(father[end[0]][end[1]]) != 0:  # 从终点出发回溯路径上的点,生成关键路径
        if x == start[0] and y == start[1]:
            break
        way[x][y] = 0
        x, y = father[x][y][0], father[x][y][1]
    print("用时：", time.perf_counter() - timer)
    temp = way[:]  # 关键路径上的点
    for i in range(len(temp)):  # 输出路径上的所有点
        tmp = ""
        for j in range(len(temp[i])):
            if i == 0 or j == 0 or i == len(temp) - 1 or j == len(temp[i]) - 1:  # 输出边界
                tmp += "1"
            elif i == start[0] and j == start[1]:  # 输出起点
                tmp += "S"
            elif i == end[0] and j == end[1]:  # 输出终点
                tmp += "E"
            elif temp[i][j] != 1:  # 输出路径
                tmp += str(temp[i][j])
            else:
                tmp += " "
        print(tmp)


if __name__ == '__main__':
    main()
