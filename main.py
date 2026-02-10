from agent import Agent
from logging.logger import log

if __name__ == '__main__':
    # model = 'Qwen/Qwen3-Coder-Next'
    # model = 'deepseek-ai/DeepSeek-V3.2'
    # model = 'zai-org/GLM-4.7-Flash'
    model = 'deepseek-ai/DeepSeek-R1'
    agent = Agent()
    user_input = input()
    # user_input = "计算(1 + 1) * (1 + 2)的值，先拆分步骤然后创建子Agent执行，其中的加法操作创建子Agent执行，不要直接计算结果"
    result = agent.execute(user_input)
    log(result)