代码
# EasyMCSL 轻易我的世界开服工具

## 介绍

EasyMCSL 是一个简易的 Minecraft 服务器启动和管理工具，旨在帮助用户轻松配置和启动 Minecraft 服务器。该工具具有多项功能，包括服务器配置、查看模组和插件列表、修改服务器主配置文件以及翻译功能。

## 功能

- **启动服务器**：根据配置启动 Minecraft 服务器，并显示服务器运行端口。
- **配置服务器**：自动查找服务器文件或手动设置服务器目录，配置启动内存大小和优化参数。
- **服务器文件管理**：
  - 查看模组列表
  - 查看插件列表
  - 修改和查看服务器主配置文件（包括端口、游戏模式和正版验证等设置）
- **翻译功能**：使用百度翻译 API，将英语、俄语、法语和德语文本翻译成中文。

## 使用方法

1. **克隆仓库**

   ```sh
   git clone https://github.com/Easily-miku/EasyMinecraftServerLuncher.git
   cd EasyMCSL
安装依赖

确保你已经安装了 Python，并使用以下命令安装所需的依赖库：

   '''sh
复制代码
pip install requests
运行工具

使用以下命令运行工具：

   '''sh
复制代码
python easymcsl.py
操作说明

启动程序后，你将看到主菜单，可以选择以下选项：

[1]启动服务器：启动已配置的 Minecraft 服务器。
[2]配置服务器：配置服务器启动参数，包括内存大小和优化参数。
[3]服务器文件：管理服务器文件，包括查看模组和插件列表，修改服务器主配置文件。
[4]信息：显示工具的开发者信息。
[5]翻译：使用百度翻译 API 将指定文本翻译为中文。
[0]关闭软件：退出程序。
配置文件

工具会将服务器配置保存在 server_config.json 文件中，包含以下信息：

server_dir：服务器文件目录
server_name：服务器文件名
memory_size：启动内存大小
optimization_code：启动优化参数
服务器主配置文件

服务器主配置文件 server.properties 包含以下可修改的参数：

server-port：服务器端口
gamemode：游戏模式（0-生存，1-创造，2-冒险，3-观察者）
online-mode：是否开启正版验证（true/false）
翻译功能

翻译功能使用百度翻译 API。你需要提供以下 API 凭证：

APP ID
密钥
这些信息已经删除。如果你需要使用百度翻译，请先去百度翻译官网申请免费api后,在 baidu_translate 函数中更新 app_id 和 secret_key。

贡献

欢迎提交 Issue 和 Pull Request 来改进该项目。

许可

本项目基于 MIT 许可协议。

感谢使用 EasyMCSL！希望你能喜欢这个工具。
