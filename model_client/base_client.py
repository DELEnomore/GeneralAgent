from abc import abstractmethod


class BaseClient:
    """模型客户端基类"""

    def __init__(self, model: str, base_url: str, api_key: str):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

    @abstractmethod
    def create(self, messages: list) -> str:
        return None