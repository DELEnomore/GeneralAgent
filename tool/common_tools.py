import os
import asyncio
from random import randint

from agent.agent import Agent
from tool.tool import tool


@tool()
async def calculator(a: int, b: int):
    """
    加法运算器
    :param a: 参数1
    :param b: 参数2
    :return:
    """
    return a + b


@tool()
async def cmd(command: str):
    """
    执行系统命令并返回输出结果
    :param command: 要执行的命令字符串
    :return: 命令执行的输出结果
    """
    try:
        result = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True
        )
        stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=30)
        output = f"stdout: {stdout.decode('utf-8', errors='replace')}\nstderr: {stderr.decode('utf-8', errors='replace')}\nreturncode: {result.returncode}"
        return output
    except asyncio.TimeoutError:
        return "命令执行超时"
    except Exception as e:
        return f"命令执行出错: {str(e)}"


@tool()
async def create_file(file_path: str, content: str):
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

        # 在线程池中执行文件写入，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: open(file_path, 'w', encoding='utf-8').write(content))
        return f"文件创建成功: {file_path}"
    except Exception as e:
        return f"文件创建失败: {str(e)}"


@tool()
async def read_file(file_path: str):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容
    """
    try:
        # 在线程池中执行文件读取，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, lambda: open(file_path, 'r', encoding='utf-8').read())
        return content
    except FileNotFoundError:
        return f"文件不存在: {file_path}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"


@tool()
async def modify_file(file_path: str, old_content: str, new_content: str):
    """
    修改文件内容，将指定旧内容替换为新内容
    :param file_path: 文件路径
    :param old_content: 要替换的旧内容
    :param new_content: 新内容
    :return: 操作结果
    """
    try:
        # 在线程池中执行文件读取和写入，避免阻塞事件循环
        loop = asyncio.get_event_loop()

        def _modify():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_content not in content:
                return f"未找到指定的旧内容: {old_content}"

            updated_content = content.replace(old_content, new_content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return f"文件修改成功: {file_path}"

        result = await loop.run_in_executor(None, _modify)
        return result
    except FileNotFoundError:
        return f"文件不存在: {file_path}"
    except Exception as e:
        return f"修改文件失败: {str(e)}"


@tool()
async def task(prompt: str, tools: list, user_input: str) -> str:
    """
    Assign the task to the sub-agent for execution.
    :param prompt: system prompt, set by the super Agent according to its task.
    :param tools:  tools available to sub agent, filtered by super agent
    :param user_input: the exact subtask that sub agent has to finish
    :return:
    """
    id = randint(1, 10)
    print(f'创建子agent{id}, prompt:{prompt}, tools:{tools}, input:{user_input}')

    agent = Agent(system_prompt=prompt, available_tools=tools)
    result = await agent.execute(user_input)
    print(f'子Agent{id}执行结束，结果:{result}')
    del agent
    return result