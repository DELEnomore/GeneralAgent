import inspect
import json
import asyncio
from typing import Callable, get_type_hints, Coroutine

from docstring_parser import parse

TOOL_REGISTRY: dict[str, 'Tool'] = {}

class Tool:
    def __init__(self, name: str, description: str, parameters: dict, func: Callable):
        self.func = func
        self.json_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }

    async def __call__(self, **kwargs):
        result = self.func(**kwargs)
        if asyncio.iscoroutine(result):
            result = await result
        return str(result)


def _type_to_json_schema(py_type) -> str:
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
        return type_map.get(origin_type)
    return type_map.get(py_type)

def tool():
    """
    将函数注册为全局可见的 Tool
    parameters: 必须为符合 JSON Schema 的字典（OpenAI 要求）
    """

    def decorator(func: Callable) -> Callable:
        name = func.__name__

        if name in TOOL_REGISTRY:
            raise ValueError(f"Tool name '{name}' already registered")

        docstring = parse(func.__doc__ or "")
        function_description = docstring.description
        param_descriptions = {param.arg_name: param.description for param in docstring.params}

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
            param_description = param_descriptions[param_name]
            properties[param_name] = {
                'type': json_type,
                'description': param_description
            }

        parameters = {
            "type": "object",
            "properties": properties,
            "required": required
        }

        TOOL_REGISTRY[name] = Tool(name, function_description, parameters, func)
        return func
    return decorator

async def execute_tool_call(name, arguments):
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    return await TOOL_REGISTRY[name](**arguments)

