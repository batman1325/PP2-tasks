print(10 > 9)
print(10 == 9)
print(10 < 9)
"""
True
False
False
"""

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
#b is not greater than a

print(bool("Hello"))
print(bool(15))
"""
True
True
"""

x = "Hello"
y = 15
print(bool(x))
print(bool(y))
"""
True
True
"""

bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
#those will return false

