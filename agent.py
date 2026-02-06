
from model_client.base_client import BaseClient


class Agent:
    """Agent类"""

    def __init__(self, client: BaseClient):
        """
        初始化Agent

        Args:
            client: 模型客户端实例
        """
        self.client = client

    def execute(self, user_input: str) -> str:
        """
        执行Agent任务

        Args:
            user_input: 用户输入

        Returns:
            Agent响应
        """
        # 将工具绑定到client
        # TODO 创建sub agent、定义prompt
        # 创建消息列表
        messages = [
            {"role": "user", "content": user_input}
        ]

        # 调用client的create方法
        response = None

        return response


