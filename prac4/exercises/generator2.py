n = int(input())
evens = (x for x in range(n+1) if x % 2 == 0)
print(",".join(str(x) for x in evens))