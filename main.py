import asyncio
from agent.agent import Agent
from tool.common_tools import init_tools

init_tools()

async def main():
    # model = 'Qwen/Qwen3-Coder-Next'
    # model = 'deepseek-ai/DeepSeek-V3.2'
    # model = 'zai-org/GLM-4.7-Flash'
    model = 'deepseek-ai/DeepSeek-R1'
    agent = Agent()
    # user_input = input()
    user_input = "计算(1 + 1) * (1 + 2)的值，先创建子Agent计算加法部分，最终由自己进行乘法计算"
    result = await agent.execute(user_input)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())