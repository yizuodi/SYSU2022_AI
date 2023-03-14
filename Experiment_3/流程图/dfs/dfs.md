```flow
st=>start: 开始
readpre=>inputoutput: 读取预处理数据
openfile=>inputoutput: 打开并读入目标方形图形的数据（迷宫数据）到列表
findstartandend=>inputoutput: 查找起点和终点位置
pre=>operation: 初始化用于记录某点的父亲节点、记录路径、记录访问状态的列表
stack=>operation: 初始化用于记录未访问的可达点的坐标的栈
dfs=>operation: 调用深度优先搜索模块
if=>condition: 是否到达终点
if2=>operation: 分别判断当前点A的4个方向的点是否可被访问
if3=>condition: 某方向点点B是否可被访问
setvisited2=>operation: 设置该方向点B被访问并将点B入栈，设置点B的父亲节点为点A
back=>operation: 从终点出发回溯路径上的点,生成关键路径
endornot=>condition: 判断是否到达终点
pushintostack=>operation: 将当前点入队列
if_stack_empty=>condition: 判断在经过对4个方向的判断后，是否队列为空
do=>operation: 获取队列中第一个点，并做出队列操作
print=>inputoutput: 输出关键路径
end=>end: 程序结束
st->openfile->findstartandend->pre->dfs->if2->if3
if3(yes)->setvisited2->endornot
endornot(yes)->back->print->end
endornot(no)->dfs
if_stack_empty(yes,left)->do->dfs
if_stack_empty(no)->dfs
```











