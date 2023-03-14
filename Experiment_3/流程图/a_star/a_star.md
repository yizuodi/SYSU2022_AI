```flow
st=>start: 开始
preparesomething=>operation: 预处理部分数据并存储，以加快底层的计算
readpre=>inputoutput: 读取预处理数据
openfile1=>inputoutput: 打开并读入15puzzle问题题目文件
writefile2=>inputoutput: 将结果输出到对应文件
translate1=>inputoutput: 将15puzzle问题题目解析为列表
translate2=>inputoutput: 将问题列表和目标结果列表解析为64位整数表示的状态
A_star=>operation: 调用A*算法模块
timer=>operation: 调用计时器
A_star1=>operation: 将起点放入“开启列表”
A_star_search=>operation: 探索当前点A的4个方向，查找可能通过的节点
A_star_append=>operation: 将可通过的节点加入“开启列表”，将节点A存为其父亲，为该节点计算f(x)等
A_star_del=>operation: 将点A从“开启列表”移除，加入到“关闭列表”
if=>condition: 是否已经找到目标节点
A_star_low=>operation: 在开启列表中寻找估价函数值最低的节点B，将其从“开启列表”删除，加入到“关闭列表”
A_star_search2=>operation: 探索当前点B的4个方向，查找可能通过的节点
if2=>condition: 可通过的节点是否已经在“开启列表”
A_star_append2=>operation: 将可通过的节点加入“开启列表”，将节点B存为其父亲，为该节点计算f(x)等
A_star_update=>operation: 更新该“开启列表”内的g(x)值
A_star_outputresult=>inputoutput: 递归输出每一步的结果
timer2=>operation: 调用计时器
end=>end: 程序结束
st->preparesomething->openfile1->translate1->translate2->timer->A_star
A_star->A_star1->A_star_search->readpre->A_star_append->A_star_del->if
readpre->A_star_append
if(no)->A_star_low->A_star_search2->if2
if2(yes,left)->A_star_update->if
if2(no)->A_star_append2->if
if(yes)->A_star_outputresult->timer2->end

```

