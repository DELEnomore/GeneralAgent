import inspect
from typing import Callable, get_type_hints

TOOL_REGISTRY: dict[str, 'Tool'] = {}

class Tool:
    def __init__(self, name: str, description: str, parameters: dict, func: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters  # JSON Schema
        self.func = func

    def to_openai_schema(self) -> dict:
        """生成 OpenAI API 要求的 tool schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def __call__(self, **kwargs):
        return self.func(**kwargs)


def _type_to_json_schema(py_type) -> dict:
    """将 Python 类型转换为 JSON Schema 类型（简化版）"""

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    # 处理泛型列表和字典
    origin_type = getattr(py_type, '__origin__', None)
    if origin_type is not None:
        return {"type": type_map.get(origin_type)}
    return {"type": type_map.get(py_type)}

def register_tool():
    """
    将函数注册为全局可见的 Tool
    parameters: 必须为符合 JSON Schema 的字典（OpenAI 要求）
    """

    def decorator(func: Callable) -> Callable:
        name = func.__name__

        if name in TOOL_REGISTRY:
            raise ValueError(f"Tool name '{name}' already registered")

        description = (func.__doc__ or "").strip().split("\n")[0]

        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            if param_name == "self" or param_name == 'cls':
                continue
            required.append(param_name)
            py_type = type_hints.get(param_name)
            if py_type is None:
                raise Exception(f'函数{name}入参缺少类型提示，注册tool失败')
            json_type = _type_to_json_schema(py_type)
            properties[param_name] = json_type

        parameters = {
            "type": "object",
            "properties": properties,
            "required": required
        }

        TOOL_REGISTRY[name] = Tool(name, description, parameters, func)
        return func
    return decorator


