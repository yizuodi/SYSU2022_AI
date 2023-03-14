









```flow
st=>start: 开始
readpre=>inputoutput: 读取预处理数据
openfile=>inputoutput: 打开并读入目标方形图形的数据（迷宫数据）到列表
findstartandend=>inputoutput: 查找起点和终点位置
pre=>operation: 初始化用于记录某点的父亲节点、记录路径、记录访问状态的列表
queue=>operation: 初始化用于记录未访问的可达点的坐标的队列
bfs=>operation: 调用广度优先搜索模块
if=>condition: 是否到达终点
setvisited1=>operation: 设置当前点被访问
if2=>operation: 分别判断4个方向的点是否可被访问
if3=>condition: 该方向点是否可被访问
setvisited2=>operation: 设置当前点被访问并记录当前点的来源
back=>operation: 从终点出发回溯路径上的点,生成关键路径
endornot=>condition: 判断是否到达终点
pushintoqueue=>operation: 将当前点入队列
if_queue_empty=>condition: 判断在经过对4个方向的判断后，是否队列为空
do=>operation: 获取队列中第一个点，并做出队列操作
print=>inputoutput: 输出关键路径
end=>end: 程序结束
st->openfile->findstartandend->pre->bfs->setvisited1->if2->if3
if3(yes)->setvisited2->endornot
endornot(yes)->back->print->end
endornot(no)->pushintoqueue->if_queue_empty
if_queue_empty(yes,left)->do->bfs
if_queue_empty(no)->bfs
```











