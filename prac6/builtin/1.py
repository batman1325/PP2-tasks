#1
num = [1, 2, 3, 4, 5]
s = list(map(lambda x: x**2, num))
print(s)
e = list(filter(lambda x: x % 2 == 0, num))
print(e)

#2
from functools import reduce
t = reduce(lambda x, y: x + y, num)
print(t)

#3
liist = ["aaaa", "bbbb", "cccc"]
for index, letter in enumerate(liist):
    print(index, letter)

numb = [20, 40, 60]

for l, n in zip(liist, numb):
    print(l, n)

#4
a = 10000
print(type(a))
print(isinstance(a, int))

a = "123"
b = 45.6
numbe = int(a)
flt = float(a)
string = str(b)

print(numbe, flt, string)