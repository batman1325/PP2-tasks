a, b = map(int, input().split())
square = (x*x for x in range(a, b+1))
for j in square:
    print(j)