#1
import os
path = "abc/def/ghi"
os.makedirs(path, exist_ok=True)

#2
items = os.listdir("abc")
for item in items:
    print(item)
items = os.listdir("abc/def")
for item in items:
    print(item)

#3
c = "abc"
for root, dirs, files in os.walk(c):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))

#4
import shutil
shutil.copy("copy_sample.txt", "abc/def/ghi/copy_sample.txt")
shutil.move("abc/def/ghi/copy_sample.txt", "abc/def/copy_sample.txt")