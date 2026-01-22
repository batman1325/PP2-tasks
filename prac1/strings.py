a = "Hello"
print(a)

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

b = "Hello, World!"
print(b[2:5])
#llo

b = "Hello, World!"
print(b[2:])
#llo, World!

b = "Hello, World!"
print(b[-5:-2])
#orl

a = "Hello, World!"
print(a.upper())
#HELLO, WORLD!

a = "Hello, World!"
print(a.lower())
#hello, world!

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

a = "Hello, World!"
print(a.replace("H", "J"))
#Jello, World!

a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

a = "Hello"
b = "World"
c = a + b
print(c)
#Concatenation

price = 59
txt = f"The price is {price} dollars"
print(txt)