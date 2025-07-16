# MCP 本地助手服务器

这是一个功能强大的 MCP (Model Context Protocol) 服务器，支持执行本地命令、打开应用程序、网页查询和集成 Claude AI。

## 功能特性

- 🖥️ **执行本地命令**：安全地执行系统命令
- 🚀 **打开应用程序**：启动本地应用程序和文件
- 🌐 **网页操作**：打开URL和执行网页搜索
- 📊 **系统信息**：获取详细的系统状态信息
- 📁 **文件操作**：读取、写入、列表、删除文件
- 🤖 **Claude AI集成**：直接与Claude AI对话
- 🔒 **安全限制**：可配置的安全措施

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置API密钥

设置环境变量（可选，用于Claude AI功能）：

```bash
export ANTHROPIC_API_KEY="your_claude_api_key_here"
```

### 3. 运行服务器

```bash
python mcp_server.py
```

## 可用工具

### 1. execute_command
执行本地系统命令
```json
{
  "command": "ls -la",
  "shell": false,
  "timeout": 30
}
```

### 2. open_application
打开本地应用程序
```json
{
  "path": "notepad.exe",
  "args": ["file.txt"]
}
```

### 3. open_url
在浏览器中打开URL
```json
{
  "url": "https://www.google.com"
}
```

### 4. web_search
执行网页搜索
```json
{
  "query": "python tutorial",
  "engine": "google"
}
```

### 5. get_system_info
获取系统信息
```json
{
  "info_type": "basic"
}
```

### 6. file_operations
文件操作
```json
{
  "operation": "read",
  "path": "/path/to/file.txt"
}
```

### 7. claude_chat
与Claude AI聊天
```json
{
  "message": "Hello, Claude!",
  "model": "claude-3-sonnet-20240229",
  "max_tokens": 1000
}
```

## 配置

创建 `config.json` 文件来自定义服务器行为：

```json
{
  "security": {
    "allowedCommands": ["ls", "pwd", "echo"],
    "restrictedPaths": ["/etc", "/usr/bin"],
    "maxExecutionTime": 30
  }
}
```

## 安全注意事项

1. **命令执行**：谨慎执行未知命令，特别是具有管理员权限的命令
2. **文件访问**：避免访问系统关键文件
3. **网络请求**：注意网络安全和隐私
4. **API密钥**：妥善保管Claude API密钥

## 依赖项

- `mcp`: MCP协议支持
- `anthropic`: Claude AI API客户端
- `requests`: HTTP请求库
- `psutil`: 系统信息获取
- `asyncio`: 异步编程支持

## 支持的平台

- Windows
- macOS
- Linux

## 常见问题

### Q: 如何获取Claude API密钥？
A: 访问 [Anthropic Console](https://console.anthropic.com/) 注册并获取API密钥。

### Q: 命令执行失败怎么办？
A: 检查命令权限、路径是否正确，以及是否有必要的系统权限。

### Q: 如何限制可执行的命令？
A: 在配置文件中设置 `allowedCommands` 列表。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本
- 支持基本命令执行
- 集成Claude AI
- 添加安全配置选项
