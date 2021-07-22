import os

path ="C:/Users/Admin/Desktop/CS114/yeb"
for i in os.listdir(path):
    path_ = path + "/" + i
    file = open(path, 'r')
    file = file.read()
    print(file)