from model_client.openai_client import OpenaiClient
from tools.tool import Tool, TOOL_REGISTRY, execute_tool_call, tool

DEFAULT_SYSTEM_PROMPT = "You are an intelligent agent, tasked with fulfilling users' requests.Use appropriate tools reasonably, plan before execution when faced with complex tasks, and if necessary, delegate parts of the task to other agents."

OPENAI_CLIENT = OpenaiClient()

CUR_AGENT_LEVEL = -1

class Agent:
    """Agent类"""

    def __init__(self, client: OpenaiClient = OPENAI_CLIENT, available_tools: Tool = None, system_prompt=DEFAULT_SYSTEM_PROMPT):
        self.client = client
        self.system_prompt = system_prompt
        if available_tools:
            self.tools = [TOOL_REGISTRY[tool_name] for tool_name in available_tools]
        else:
            self.tools = TOOL_REGISTRY.values()
        global CUR_AGENT_LEVEL
        CUR_AGENT_LEVEL += 1

    def execute(self, user_input: str) -> str:
        """
        执行Agent任务
        """
        # 将工具绑定到client
        # 创建消息列表
        messages = [
            {"role": "user", "content": user_input}
        ]
        while True:
            message = self.client.create(messages, self.tools)
            messages.append(message)
            if not message.get('tool_calls'):
                return message['content']
            else:
                messages.extend([{
                    'role': 'tool',
                    'content': execute_tool_call(tool_call['function']['name'], tool_call['function']['arguments']),
                    'name': tool_call['function']['name'],
                    'id': tool_call['id'],
                } for tool_call in message['tool_calls']])
    def __del__(self):
        global CUR_AGENT_LEVEL
        CUR_AGENT_LEVEL -= 1

@tool()
def task(prompt: str, tools: list, user_input: str) -> str:
    """
    Assign the task to the sub-agent for execution.
    :param prompt: system prompt, set by the super Agent according to its task.
    :param tools:  tools available to sub agent, filtered by super agent
    :param user_input: the exact subtask that sub agent has to finish
    :return:
    """

    print(f'创建子agent, prompt:{prompt}, tools:{tools}, input:{user_input}')
    agent = Agent(system_prompt=prompt, available_tools=tools)
    result = agent.execute(user_input)
    print(f'子Agent执行结束，结果:{result}')
    del agent
    return result
