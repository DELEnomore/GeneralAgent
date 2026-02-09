from agent import Agent


if __name__ == '__main__':
    # model = 'Qwen/Qwen3-Coder-Next'
    # model = 'deepseek-ai/DeepSeek-V3.2'
    # model = 'zai-org/GLM-4.7-Flash'
    model = 'deepseek-ai/DeepSeek-R1'
    agent = Agent()
    result = agent.execute("计算(1 + 1) * (1 + 2)的值，先拆分步骤然后创建子Agent执行，其中的加法操作创建子Agent执行，不要直接计算结果")
    print(result)