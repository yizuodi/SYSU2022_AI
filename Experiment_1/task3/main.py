def print_triangle(n):
    s = [[0 for j in range(i + 1)] for i in range(n)]

    for i in range(n):
        for j in range(i + 1):
            if j == 0:
                s[i][j] = 1
            elif j != i:
                s[i][j] = s[i - 1][j - 1] + s[i - 1][j]
            else:
                s[i][j] = s[i - 1][j - 1]
    print("下面是帕斯卡三角形前", n, "行")
    for i in range(n):
        print(s[i])


n = 0
while n < 1:
    n = int(input('请输入行数：'))
print_triangle(n)
