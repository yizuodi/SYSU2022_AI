s = input("请输入待检验的字符串：\n")
# s = s.replace(' ','')#去除空格(后面也去除了一次，不需要了)
s = s.lower()  # 所有字母转换为小写
s = ''.join(filter(str.isalnum, s))  # 仅保留英文字母和数字
# print(s)
if s == s[::-1]:
    print("True")
else:
    print("False")
