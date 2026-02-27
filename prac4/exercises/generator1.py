n = int(input())
squares = (x*x for x in range(n+1))
for j in squares:
    print(j)