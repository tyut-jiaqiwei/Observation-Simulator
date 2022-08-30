
N = int(input())
N_res = []
for i in range(N):
    n = int(input())
    x = input().split()

    max_num,start,end = 0,10e6,10e6
    for xi_index,xi in enumerate(x):
        for xj_index,xj in enumerate(x[xi_index:]):
            # print(xi_index,xj_index+xi_index+1)
            num = 1
            for i in x[int(xi_index):int(xi_index + xj_index+1)]:
                num = num*int(i)
            print('###')
            print(xi_index,xi_index + xj_index,num)
            if num >= max_num and xi_index <= start and xj_index+1<=end:
                max_num,start,end= num,xi_index+1,xj_index+xi_index+1
                break
            elif num >= max_num and xi_index <= start:
                max_num, start, end = num, xi_index+1, xj_index+xi_index+1
                break
            elif num >= max_num :
                max_num, start, end = num, xi_index+1, xj_index+xi_index+1
    print("$$$$")
    print(start, end)

