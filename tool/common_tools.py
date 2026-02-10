import os
import subprocess
from typing import Optional
from tool.tool import tool


@tool()
def calculator(a: int, b: int):
    """
    加法运算器
    :param a: 参数1
    :param b: 参数2
    :return:
    """
    return a + b


@tool()
def cmd(command: str):
    """
    执行系统命令并返回输出结果
    :param command: 要执行的命令字符串
    :return: 命令执行的输出结果
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        output = f"stdout: {result.stdout}\nstderr: {result.stderr}\nreturncode: {result.returncode}"
        return output
    except Exception as e:
        return f"命令执行出错: {str(e)}"


@tool()
def create_file(file_path: str, content: str):
    """
    创建新文件并写入内容
    :param file_path: 文件路径
    :param content: 文件内容
    :return: 操作结果
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"文件创建成功: {file_path}"
    except Exception as e:
        return f"文件创建失败: {str(e)}"


@tool()
def read_file(file_path: str):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"文件不存在: {file_path}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"


@tool()
def modify_file(file_path: str, old_content: str, new_content: str):
    """
    修改文件内容，将指定旧内容替换为新内容
    :param file_path: 文件路径
    :param old_content: 要替换的旧内容
    :param new_content: 新内容
    :return: 操作结果
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_content not in content:
            return f"未找到指定的旧内容: {old_content}"

        updated_content = content.replace(old_content, new_content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return f"文件修改成功: {file_path}"
    except FileNotFoundError:
        return f"文件不存在: {file_path}"
    except Exception as e:
        return f"修改文件失败: {str(e)}"


