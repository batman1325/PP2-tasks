#1
with open("sample.txt", "w") as file:
    file.write("Hello, World\n")

#2
with open("sample.txt", "r") as file:
    content = file.read()
    print(content)

#3
with open("sample.txt", "a") as file:
    file.write("Helloooo, Woooorld")
with open("sample.txt", "r") as file:
    content2 = file.read()
    print(content2)

#4
import shutil
shutil.copy("sample.txt", "copy_sample.txt")
shutil.copy("sample.txt", "backup_sample.txt")

#5
import os
if os.path.exists("sample.txt"):
  os.remove("sample.txt")
else:
  print("File does not exist")