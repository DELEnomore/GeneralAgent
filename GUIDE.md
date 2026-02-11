# 通用智能体 (GeneralAgent) 使用指导文档

## 项目概述

GeneralAgent 是一个受 Claude code 启发的通用智能体框架，旨在解决各种复杂任务。通过创建子Agent来分解任务，父Agent可以指定子Agent的所有设置。项目采用模块化设计，支持工具调用和异步操作。

## 项目结构

```
GeneralAgent/
├── main.py                    # 主程序入口
├── README.md                  # 项目简介
├── base_config.yml           # 基础配置文件
├── __init__.py               # Python包初始化
├── __pycache__/              # Python字节码缓存
├── .idea/                    # IDE配置文件
├── agent/                    # Agent相关模块
│   ├── __init__.py
│   └── agent.py             # 主Agent类
├── model_client/            # 模型客户端模块
│   ├── __init__.py
│   └── openai_client.py     # OpenAI兼容API客户端
└── tool/                    # 工具模块
    ├── __init__.py
    ├── tool.py              # 工具注册和管理
    └── common_tools.py      # 常用工具定义
```

## 核心组件

### 1. Agent系统 (`agent/agent.py`)

Agent类是项目的核心，负责：
- 接收用户输入并执行任务
- 调用合适的工具
- 创建和管理子Agent
- 处理工具调用结果

**关键特性：**
- 支持工具调用（包括子Agent创建）
- 异步执行
- 支持复杂的任务分解

**默认系统提示：**
```
"You are an intelligent agent, tasked with fulfilling users' requests.Use appropriate tools reasonably, plan before execution when faced with complex tasks, and if necessary, delegate parts of the task to other agents."
```

### 2. 工具系统 (`tool/`)

#### 2.1 工具注册机制 (`tool/tool.py`)
- 使用 `@tool()` 装饰器注册工具
- 自动从函数签名和文档字符串生成JSON Schema
- 支持异步工具函数

#### 2.2 内置工具 (`tool/common_tools.py`)
项目提供了以下内置工具：

1. **calculator(a: int, b: int)** - 加法运算器
2. **cmd(command: str)** - 执行系统命令
3. **create_file(file_path: str, content: str)** - 创建新文件
4. **read_file(file_path: str)** - 读取文件内容
5. **modify_file(file_path: str, old_content: str, new_content: str)** - 修改文件内容

#### 2.3 特殊工具
- **task(prompt: str, tools: list, user_input: str)** - 创建子Agent执行任务
  - 父Agent可以完全控制子Agent的系统提示和可用工具

### 3. 模型客户端 (`model_client/openai_client.py`)
- 支持OpenAI兼容的API
- 配置从 `base_config.yml` 加载
- 支持工具调用功能

## 快速开始

### 1. 环境准备
确保Python环境已安装以下依赖：
```bash
pip install openai yaml docstring-parser asyncio
```

### 2. 配置模型API
编辑 `base_config.yml`：
```yaml
base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
model: 'deepseek-v3.2'  # 或其他支持的模型
api_key: 'your-api-key-here'
```

支持的模型（需要在 `main.py` 中切换）：
- `Qwen/Qwen3-Coder-Next`
- `deepseek-ai/DeepSeek-V3.2`
- `zai-org/GLM-4.7-Flash`
- `deepseek-ai/DeepSeek-R1`

### 3. 运行程序
```bash
python main.py
```

程序会等待用户输入，您可以输入各种任务请求。

## 使用示例

### 示例1：数学计算
输入：`"计算(1 + 1) * (1 + 2)的值，先创建子Agent计算加法部分，最终由自己进行乘法计算"`

Agent会：
1. 创建子Agent计算 1+1
2. 创建另一个子Agent计算 1+2
3. 自己执行乘法操作 (2 * 3)
4. 返回结果 6

### 示例2：文件操作
输入：`"创建一个空文件，命名为test.md"`
- Agent会调用 `create_file` 工具

输入：`"将本地的abc.md文件名称修改为test.md"`
- Agent会调用 `cmd` 工具执行重命名命令

### 示例3：代码分析
输入：`"阅读本地的全部代码结构，将分析报告输出到文件中"`
- Agent会使用 `read_file` 读取代码
- 分析后使用 `create_file` 输出报告

## 自定义工具

要添加新的工具，只需在 `common_tools.py` 中添加函数并使用 `@tool()` 装饰器：

```python
@tool()
async def your_tool_name(param1: str, param2: int) -> str:
    """
    工具描述
    
    :param param1: 参数1描述
    :param param2: 参数2描述
    :return: 返回结果描述
    """
    # 工具实现逻辑
    return f"执行结果"
```

**注意：**
- 函数必须包含完整的类型提示
- 必须有完整的文档字符串（包括参数描述）
- 工具名称会自动从函数名获取

## Agent执行流程

1. **初始化阶段**
   - 加载配置和模型客户端
   - 初始化所有可用工具

2. **任务接收**
   - 接收用户输入
   - 构建消息历史

3. **循环执行**
   - 调用模型API获取响应
   - 检查是否有工具调用
   - 如果有工具调用，并发执行所有工具
   - 将工具结果添加到消息历史
   - 重复直到没有工具调用

4. **结果返回**
   - 返回最终响应内容

## 任务分解机制

Agent可以通过 `task` 工具创建子Agent来分解复杂任务：
- **系统提示传递**：父Agent可以指定子Agent的系统提示
- **工具权限控制**：父Agent可以限制子Agent的可用工具
- **任务分配**：父Agent指定子Agent执行的具体子任务

这种机制使得：
- 复杂任务可以分层处理
- 每个子任务有明确的边界
- 父Agent保持整体控制

## 配置说明

### base_config.yml
```yaml
# API基础URL
base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'

# 使用的模型名称
model: 'deepseek-v3.2'

# API密钥
api_key: 'sk-xxxxxxxxxxxxxxxxxxxxxxxx'
```

### main.py 配置
可以在 `main.py` 中修改：
```python
# 选择不同的模型
model = 'deepseek-ai/DeepSeek-R1'  # 或其他模型

# 预定义测试输入
user_input = "计算(1 + 1) * (1 + 2)的值"
```

## 调试和日志

程序运行时会有详细的日志输出：
- Agent的角色和响应内容（截断显示）
- 工具调用信息（工具名称和参数）
- 工具执行结果
- 子Agent的创建和执行信息

## 最佳实践

1. **清晰的系统提示**：为不同任务设置合适的系统提示
2. **工具权限最小化**：只给予子Agent完成其任务所需的最小工具权限
3. **任务分解粒度**：合理分解任务，避免过于细碎或过于庞大的子任务
4. **错误处理**：工具应包含适当的错误处理和返回信息
5. **异步优化**：利用异步特性提高并发性能

## 扩展建议

### 1. 添加新工具
根据项目需求添加自定义工具，如：
- 数据库操作工具
- API调用工具
- 数据处理工具

### 2. 增强Agent能力
- 添加记忆机制
- 支持长期任务处理
- 集成更多模型提供商

### 3. 改进任务分解
- 实现更智能的任务分解算法
- 添加任务优先级管理
- 支持任务依赖关系

## 故障排除

### 常见问题

1. **工具调用失败**
   - 检查工具函数是否有完整的类型提示和文档字符串
   - 确保函数是异步的（使用 `async def`）
   - 检查工具参数是否符合JSON Schema要求

2. **模型API连接失败**
   - 检查 `base_config.yml` 配置
   - 验证API密钥和URL是否正确
   - 确认网络连接正常

3. **文件操作权限问题**
   - 检查文件路径权限
   - 确保目录存在或可创建

4. **子Agent创建失败**
   - 检查传递给 `task` 工具的参数格式
   - 确保系统提示字符串正确
   - 验证工具列表是有效的工具名称

### 调试技巧
- 查看控制台输出了解执行流程
- 使用简单的测试任务验证基础功能
- 逐步增加任务复杂度测试系统稳定性

## 未来发展方向

1. **工具市场**：建立可插拔的工具生态系统
2. **可视化界面**：添加Web界面方便交互
3. **性能优化**：实现更高效的任务调度和执行
4. **多模态支持**：集成图像、语音等多模态处理
5. **知识库集成**：连接外部知识库增强Agent能力

---

*此文档基于代码分析自动生成，如有疑问请参考源码或联系开发者。*