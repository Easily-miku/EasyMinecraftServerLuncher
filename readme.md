# EasyMCSL - 轻易我的世界开服工具

EasyMCSL 是一个简单易用的 Minecraft 服务器管理工具，旨在帮助用户轻松配置、启动和管理 Minecraft 服务器。

## 特性

- 启动 Minecraft 服务器
- 配置服务器参数
- 查看和管理模组和插件
- 显示服务器信息
- 多语言翻译功能
- 下载 Minecraft 服务端并显示下载进度

## 安装

### 依赖项

在运行该工具之前，请确保已安装以下 Python 依赖项：

- `requests`
- `tqdm`

你可以通过以下命令安装所需的依赖项：

```bash
pip install requests tqdm
下载源码
你可以通过以下命令克隆本项目：
```
```bash
复制代码
git clone https://github.com/yourusername/EasyMCSL.git
cd EasyMCSL
```
```bash
使用方法
运行主脚本以启动工具：
python main.py
在主菜单中，你可以选择以下选项：

启动服务器
配置服务器
服务器文件
显示信息
翻译
下载 Minecraft 服务端
关闭软件
启动服务器
选择启动服务器选项后，工具将根据配置文件中的设置启动 Minecraft 服务器。如果配置文件不存在，系统会提示你先进行配置。
```

## 配置服务器
```bash
进入配置服务器菜单后，你可以设置服务器的启动参数，例如内存大小和优化代码。配置完成后会保存到 server_config.json 文件中。

具体操作步骤：

提供服务器目录路径（如果未找到服务器文件）。
输入启动内存大小（例如1024M）。
输入启动优化代码（例如 -XX:+UseG1GC）。
配置完成后，工具会显示当前的配置，并保存到 server_config.json 文件中。
```
## 服务器文件
```bash
在服务器文件菜单中，你可以：

查看模组列表
查看插件列表
修改或查看服务器主配置文件
下载 Minecraft 服务端
在下载 Minecraft 服务端菜单中，你可以选择要下载的服务端类型和版本，工具会自动下载并显示进度。

具体操作步骤：

选择服务端类型。
选择服务端版本。
工具会自动下载并显示下载进度。
显示信息
选择此选项可以查看工具的开发者信息和其他相关信息。
```
## 翻译
工具集成了百度翻译功能，但默认的 APP ID 和密钥已被删除。请自行注册百度翻译 API 并在代码中添加你的 APP ID 和密钥。

具体操作步骤：

访问 百度翻译API官网.
注册并获取 APP ID 和密钥。
在代码中的 baidu_translate 函数中添加你的 APP ID 和密钥。
修改代码如下：
```python
复制代码
def baidu_translate(query, from_lang='en', to_lang='zh'):
    app_id = '你的 APP ID'
    secret_key = '你的密钥'
    
    salt = random.randint(32768, 65536)
    sign = app_id + query + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()

    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    params = {
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
        if 'trans_result' in result:
            translated_text = result['trans_result'][0]['dst']
            print(f'[信息] 翻译结果：{translated_text}')
            return translated_text
        else:
            print(f'[错误] 翻译失败：{result}')
            return None
    except requests.RequestException as e:
        print(f'[错误] 请求翻译时发生错误：{e}')
        return None
    except json.JSONDecodeError as e:
        print(f'[错误] 解析翻译响应时发生错误：{e}')
        return None
```

## 开发者

QQ: 1502271252
贡献

欢迎贡献代码和提出建议！请提交 pull request 或在 issues 中反馈问题。

## 许可证

本项目采用 MIT 许可证。详情请参见 LICENSE 文件。
