# TODO 增删改查文件，执行cmd命令，
from tools.tool import tool


@tool()
def calculator(a:int, b:int):
    """
    加法运算器
    :param a: 参数1
    :param b: 参数2
    :return:
    """
    return a + b