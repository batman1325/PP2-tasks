def func(n):
    for x in range(n+1):
        if x % 3 == 0 and x % 4 == 0:
            yield x

n = int(input())
for j in func(n):
    print(j)