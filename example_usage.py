#!/usr/bin/env python3
"""
MCP本地助手服务器使用示例
"""

import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_mcp_server():
    """测试MCP服务器功能"""
    
    # 连接到MCP服务器
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # 初始化连接
            await session.initialize()
            
            print("🚀 MCP本地助手服务器测试")
            print("=" * 50)
            
            # 1. 获取可用工具列表
            print("\n📋 获取工具列表...")
            tools = await session.list_tools()
            print(f"可用工具数量: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 2. 测试系统信息获取
            print("\n💻 获取系统信息...")
            result = await session.call_tool("get_system_info", {"info_type": "basic"})
            if result.content:
                system_info = json.loads(result.content[0].text)
                print(f"操作系统: {system_info.get('system')}")
                print(f"平台: {system_info.get('platform')}")
                print(f"处理器: {system_info.get('processor')}")
            
            # 3. 测试命令执行
            print("\n⚡ 执行命令测试...")
            commands = [
                {"command": "echo Hello MCP!", "shell": True},
                {"command": "python --version", "shell": True},
                {"command": "pwd" if system_info.get('system') != 'Windows' else "cd", "shell": True}
            ]
            
            for cmd_info in commands:
                print(f"执行: {cmd_info['command']}")
                result = await session.call_tool("execute_command", cmd_info)
                if result.content:
                    output = json.loads(result.content[0].text)
                    if output.get('returncode') == 0:
                        print(f"✅ 输出: {output.get('stdout', '').strip()}")
                    else:
                        print(f"❌ 错误: {output.get('stderr', '').strip()}")
            
            # 4. 测试文件操作
            print("\n📁 文件操作测试...")
            test_file = "test_mcp.txt"
            test_content = "这是MCP服务器的测试文件\n当前时间: " + str(asyncio.get_event_loop().time())
            
            # 写入文件
            result = await session.call_tool("file_operations", {
                "operation": "write",
                "path": test_file,
                "content": test_content
            })
            print(f"写入文件: {result.content[0].text}")
            
            # 读取文件
            result = await session.call_tool("file_operations", {
                "operation": "read",
                "path": test_file
            })
            print(f"读取文件内容: {result.content[0].text[:50]}...")
            
            # 删除文件
            result = await session.call_tool("file_operations", {
                "operation": "delete",
                "path": test_file
            })
            print(f"删除文件: {result.content[0].text}")
            
            # 5. 测试网页搜索
            print("\n🔍 网页搜索测试...")
            result = await session.call_tool("web_search", {
                "query": "Python MCP protocol",
                "engine": "google"
            })
            print(f"搜索结果: {result.content[0].text}")
            
            # 6. 测试打开URL
            print("\n🌐 打开URL测试...")
            result = await session.call_tool("open_url", {
                "url": "https://github.com/modelcontextprotocol/python-sdk"
            })
            print(f"打开URL: {result.content[0].text}")
            
            # 7. 测试Claude聊天（如果配置了API密钥）
            print("\n🤖 Claude聊天测试...")
            result = await session.call_tool("claude_chat", {
                "message": "请简单介绍一下MCP协议",
                "max_tokens": 200
            })
            print(f"Claude回复: {result.content[0].text}")
            
            # 8. 测试应用程序打开（谨慎使用）
            print("\n🚀 应用程序测试...")
            if system_info.get('system') == 'Windows':
                # Windows系统测试
                applications = [
                    {"path": "notepad.exe", "args": []},
                    {"path": "calc.exe", "args": []}
                ]
            elif system_info.get('system') == 'Darwin':
                # macOS系统测试
                applications = [
                    {"path": "open", "args": ["-a", "TextEdit"]},
                    {"path": "open", "args": ["-a", "Calculator"]}
                ]
            else:
                # Linux系统测试
                applications = [
                    {"path": "gedit", "args": []},
                    {"path": "gnome-calculator", "args": []}
                ]
            
            for app in applications:
                try:
                    result = await session.call_tool("open_application", app)
                    print(f"打开应用: {result.content[0].text}")
                    await asyncio.sleep(1)  # 短暂等待
                except Exception as e:
                    print(f"应用打开失败: {e}")
            
            print("\n✅ 测试完成！")


async def interactive_mode():
    """交互模式"""
    print("🎮 进入交互模式")
    print("输入 'help' 查看可用命令，输入 'quit' 退出")
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            while True:
                try:
                    user_input = input("\n> ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    elif user_input.lower() == 'help':
                        print_help()
                        continue
                    elif user_input.lower() == 'tools':
                        tools = await session.list_tools()
                        print("📋 可用工具:")
                        for tool in tools.tools:
                            print(f"  - {tool.name}")
                        continue
                    
                    # 解析命令
                    parts = user_input.split(' ', 2)
                    if len(parts) < 2:
                        print("❌ 格式错误。使用: <工具名> <JSON参数>")
                        continue
                    
                    tool_name = parts[0]
                    try:
                        if len(parts) == 2:
                            args = json.loads(parts[1])
                        else:
                            args = json.loads(' '.join(parts[1:]))
                    except json.JSONDecodeError:
                        print("❌ JSON格式错误")
                        continue
                    
                    # 执行工具
                    result = await session.call_tool(tool_name, args)
                    if result.content:
                        print(f"📤 结果: {result.content[0].text}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ 错误: {e}")
    
    print("👋 再见！")


def print_help():
    """显示帮助信息"""
    help_text = """
🎮 交互模式命令:

基本命令:
  help                     - 显示此帮助
  tools                    - 列出所有可用工具
  quit/exit/q              - 退出程序

工具使用格式:
  <工具名> <JSON参数>

示例命令:
  execute_command {"command": "echo hello", "shell": true}
  get_system_info {"info_type": "basic"}
  file_operations {"operation": "list", "path": "."}
  open_url {"url": "https://google.com"}
  web_search {"query": "python", "engine": "google"}
  claude_chat {"message": "Hello Claude!"}
  open_application {"path": "notepad.exe"}

注意: JSON参数必须使用双引号
"""
    print(help_text)


async def benchmark_mode():
    """性能测试模式"""
    print("⚡ 性能测试模式")
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 测试命令执行性能
            import time
            
            print("测试命令执行性能...")
            start_time = time.time()
            
            tasks = []
            for i in range(10):
                task = session.call_tool("execute_command", {
                    "command": f"echo test_{i}",
                    "shell": True
                })
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            successful = sum(1 for r in results if r.content and "test_" in r.content[0].text)
            
            print(f"📊 性能测试结果:")
            print(f"  - 总时间: {end_time - start_time:.2f}秒")
            print(f"  - 成功执行: {successful}/10")
            print(f"  - 平均每个命令: {(end_time - start_time)/10:.3f}秒")


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "test":
            asyncio.run(test_mcp_server())
        elif mode == "interactive":
            asyncio.run(interactive_mode())
        elif mode == "benchmark":
            asyncio.run(benchmark_mode())
        else:
            print("❌ 未知模式。可用模式: test, interactive, benchmark")
    else:
        print("🎯 MCP本地助手服务器测试工具")
        print("\n可用模式:")
        print("  python example_usage.py test         - 运行自动测试")
        print("  python example_usage.py interactive  - 进入交互模式")
        print("  python example_usage.py benchmark    - 性能测试")


if __name__ == "__main__":
    main()

