import os
import hashlib

############################
#   功能  :文件去重
#   时间  :2017年2月13日
#   作者  :G_C
############################


def md5(path):
    """计算并返回文件MD5码"""
    if not os.path.isfile(path):
        return
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        data = f.read(1024)
        while data:
            md5.update(data)
            data = f.read(1024)
    return md5.hexdigest()


def file_path(path):
    """给出入口文件夹 yield返回所有文件 """
    """
    Python3中的yield from语法
        http://blog.theerrorlog.com/yield-from-in-python-3.html
    pep-0380
        http://legacy.python.org/dev/peps/pep-0380/
    """
    if os.path.isdir(path):
        for f in os.listdir(path):
            file = os.path.join(path, f)
            if os.path.isfile(file):
                yield file
            elif os.path.isdir(file):
                yield from file_path(file)
    elif os.path.isfile(path):
        yield path

MD5 = set()
path = 'file_to_path'
for path in file_path(path):
    """遍历文件列表 计算MD5 处理重复的文件"""
    m = md5(path)
    if m and m not in MD5:
        MD5.add(m)
    else:
        # 处理重复文件的函数
        # os.remove(path)
        print(m, path)
