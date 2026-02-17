x = lambda a : a + 10
print(x(5))

#__________________

x = lambda a, b : a * b
print(x(5, 6))

#__________________

x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#__________________

def myfunc(n):
  return lambda a : a * n

#__________________

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#__________________

def myfunc(n):
  return lambda a : a * n

mytripler = myfunc(3)

print(mytripler(11))

#__________________

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))

#__________________

numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#__________________

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#__________________

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#__________________

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#__________________