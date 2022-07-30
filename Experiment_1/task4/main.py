import copy
import random


class MyList():
    memory = []

    def __init__(self):
        pass

    def __init__(self, list_input):
        self.memory = copy.deepcopy(list_input)

    def push(self, args):
        self.memory.append(args)

    def get(self, num):
        copy_list = copy.deepcopy(self.memory)
        n = int(num)
        if n < 0 or n > len(self.memory):
            print("参数非法，已输出所有元素")
            print(copy_list)
        else:
            print(random.sample(copy_list, num))

    def length(self):
        print(len(self.memory))

    def delete(self):
        print(self.memory.pop(0))

    def clear(self):
        self.memory = []


temp_list = MyList([123, 'abc'])
print("列表当前情况:", temp_list.memory)
temp_list.push(456)
print("列表当前情况:", temp_list.memory)
temp_list.push(789)
print("列表当前情况:", temp_list.memory)
temp_list.get(2)
print("列表当前情况:", temp_list.memory)
temp_list.get(-1)
print("列表当前情况:", temp_list.memory)
temp_list.length()
print("列表当前情况:", temp_list.memory)
temp_list.delete()
print("列表当前情况:", temp_list.memory)
temp_list.delete()
print("列表当前情况:", temp_list.memory)
temp_list.clear()
print("列表当前情况:", temp_list.memory)
print("Byebye!")
