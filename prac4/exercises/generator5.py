def numbers(n):
    while n >= 0:
        yield n
        n = n - 1

n = int(input())
for num in numbers(n):
    print(num)