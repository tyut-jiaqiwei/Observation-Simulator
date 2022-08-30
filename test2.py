# N = input()
# n = input().split() # n个特征
# dict = {}
# for i in range(int(N)-1):
#     x = input().split()
#     key = x[0]
#     values = []
#     for value in x[1:]:
#         values.append(int(value))
#     dict.update({key:values})
# print(dict)

dict = {'1': [2,3], '2': [4,1]}
def cha(key,kkk,dict):
    value = dict[kkk]
    for v in value:
        if str(v) == key:
            return 0
        elif str(v) in dict.keys():
            return cha(key,str(v),dict)
        elif str(v) not in dict.keys():
            pass
    return 1
a = str()
for i in dict:
    res = cha(i,i,dict)
    a = a + str(res) + ' '
print(a)



