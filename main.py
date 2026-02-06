from agent import Agent
from model_client.openai_client import OpenaiClient

if __name__ == '__main__':
    agent = Agent(OpenaiClient(
        base_url='https://router.huggingface.co/v1',
        api_key='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',
        model='zai-org/GLM-4.7-Flash'
    ))
    agent.execute("随便做点什么")