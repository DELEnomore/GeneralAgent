import asyncio
from random import randint

from model_client.openai_client import OpenaiClient
from tool.tool import Tool, TOOL_REGISTRY, execute_tool_call, tool

DEFAULT_SYSTEM_PROMPT = "You are an intelligent agent, tasked with fulfilling users' requests.Use appropriate tools reasonably, plan before execution when faced with complex tasks, and if necessary, delegate parts of the task to other agents."

OPENAI_CLIENT = OpenaiClient()



class Agent:
    """Agent类"""

    def __init__(self, client: OpenaiClient = OPENAI_CLIENT, available_tools: Tool = None, system_prompt=DEFAULT_SYSTEM_PROMPT):
        self.client = client
        self.system_prompt = system_prompt
        if available_tools:
            self.tools = [TOOL_REGISTRY[tool_name] for tool_name in available_tools]
        else:
            self.tools = list(TOOL_REGISTRY.values())

    async def execute(self, user_input: str) -> str:
        """
        执行Agent任务
        """
        # 创建消息列表
        messages = [
            {"role": "user", "content": user_input}
        ]
        while True:
            message = await self.client.create(messages, self.tools)
            content = message['content'].replace('\n', '')
            truncated_content =  content[:50] + '...' if len(content) > 50 else content
            print(f'{message['role']}: {truncated_content}')
            messages.append(message)
            if not message.get('tool_calls'):
                return message['content']
            else:
                # 并发执行所有工具调用
                tool_results = await asyncio.gather(*[
                    execute_tool_call(tool_call['function']['name'], tool_call['function']['arguments'])
                    for tool_call in message['tool_calls']
                ])
                for i in range(len(message['tool_calls'])):
                    print(f'--执行工具:{message['tool_calls'][i]['function']['name']}, 参数：{message['tool_calls'][i]['function']['arguments']}')
                    print(f'--工具执行结果：{_truncate_message(tool_results[i])}')
                    messages.append({
                        'role': 'tool',
                        'content': tool_results[i],
                        'name': message['tool_calls'][i]['function']['name'],
                        'id': message['tool_calls'][i]['id'],
                    })

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

def _truncate_message(message):
    """
    消息截断，去除换行，方便控制台打印
    :param message:
    :return:
    """
    if isinstance(message, dict):
        message = str(message)
    if len(message) > 100:
        message = message[0:100]
    message = ''.join(message.splitlines())
    return message