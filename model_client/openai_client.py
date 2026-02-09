import os
import yaml
from openai import OpenAI

with open('base_config.yml', 'r', encoding='utf-8') as f:
    content = yaml.safe_load(f)

default_model = content['model']
default_url = content['base_url']
default_key = content['api_key']

class OpenaiClient:
    """OpenAI API聊天客户端"""

    def __init__(self, model: str = default_model, base_url: str = default_url, api_key: str = default_key):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def create(self, messages: list, tools: list = None) -> dict:
        """创建聊天完成"""
        json_schema_tools = None
        if tools:
            json_schema_tools = [tool.json_schema for tool in tools]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=json_schema_tools
        )

        return response.choices[0].message.model_dump(exclude_none=True)


if __name__ == '__main__':
    test_client = OpenaiClient()

    test_client.create([
            {"role": "user", "content": '你好'}
        ])
    print('done')