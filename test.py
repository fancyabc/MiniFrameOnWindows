import sys
import re

"""
测试sys模块，在windows平台上的特点

"""

"""
print(sys.path)  # 打印系统路径
print(sys.argv)     # 打印参数列表
print(sys.version)  # 打印版本
print(len(sys.argv))    # 打印参数个数
print(sys.argv[4])
"""


ret = re.match(r"([^:]*):(.*)", "fj:sd:ak:l:qwer")
print(ret.group(1))
print(ret.group(2))
