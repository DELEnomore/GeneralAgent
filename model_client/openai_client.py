from model_client.base_client import BaseClient


class OpenaiClient(BaseClient):
    """OpenAI API聊天客户端"""

    def __init__(self, model: str, base_url: str, api_key: str):
        super().__init__(model, base_url, api_key)
        from openai import OpenAI
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def create(self, messages: list) -> str:
        """创建聊天完成"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
