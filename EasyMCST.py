import os
import subprocess
import hashlib
import requests
import random
import json

title_big = '''==========================================
███████ ███    ███  ██████ ███████ ██
██      ████  ████ ██      ██      ██
█████   ██ ████ ██ ██      ███████ ██
██      ██  ██  ██ ██           ██ ██
███████ ██      ██  ██████ ███████ ███████
=========================================='''
title_small = '=欢迎使用EasyMCSL轻易我的世界开服工具='

CONFIG_FILE = 'server_config.json'
SERVER_PROPERTIES = 'server.properties'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print(title_big)
    print(title_small)
    print('[1]启动服务器')
    print('[2]配置服务器')
    print('[3]服务器文件')
    print('[4]信息')
    print('[5]翻译')
    print('[0]关闭软件')
    print('==========================================')
    shuru = input('输入对应数字以继续：')
    return shuru

def start_server(config):
    if not config:
        print('[错误] 未找到服务器配置，请先进行配置。')
        input('按回车键返回菜单...')
        return

    server_path = os.path.join(config['server_dir'], config['server_name'])
    memory_size = config['memory_size']
    optimization_code = config['optimization_code']

    # 读取服务器端口号
    port = read_server_port(config['server_dir'])

    clear_screen()
    print(title_big)
    print(f'[信息] 正在启动服务器（端口号: {port}）...')
    try:
        command = f"java -Xmx{memory_size} -Xms{memory_size} {optimization_code} -jar {server_path} nogui"
        subprocess.run(command, shell=True)
        print('[信息] 服务器启动完成。')
    except Exception as e:
        print(f'[错误] 启动服务器时发生错误：{e}')
    input('按回车键返回菜单...')
    clear_screen()

def configure_server():
    clear_screen()
    print('进入服务器配置...')
    server_name = find_server_jar()

    if not server_name:
        print('未找到服务器文件，请提供服务器目录:')
        server_dir = input('请输入服务器目录路径：')
        if not os.path.isdir(server_dir):
            print('目录不存在，请检查路径后重试。')
            input('按回车键返回菜单...')
            return
        server_name = find_server_jar(server_dir)
        if not server_name:
            print('提供的目录中仍未找到服务器文件，请检查后重试。')
            input('按回车键返回菜单...')
            return
    else:
        server_dir = '.'  # 当前目录
        print(f'已找到服务器文件：{server_name}')

    memory_size = input('请输入启动内存大小（例如1024M）：')
    optimization_code = input('请输入启动优化代码（例如 -XX:+UseG1GC）：')

    config = {
        'server_dir': server_dir,
        'server_name': server_name,
        'memory_size': memory_size,
        'optimization_code': optimization_code
    }

    save_config(config)
    print('服务器配置完成。')
    print(f'服务器文件：{os.path.join(config["server_dir"], config["server_name"])}')
    print(f'启动内存大小：{config["memory_size"]}')
    print(f'启动优化代码：{config["optimization_code"]}')
    input('按回车键返回菜单...')
    clear_screen()
    return config

def server_files_menu(config):
    if not config:
        print('[错误] 未找到服务器配置，请先进行配置。')
        input('按回车键返回菜单...')
        return

    while True:
        clear_screen()
        print('服务器文件菜单')
        print('[1]查看模组列表')
        print('[2]查看插件列表')
        print('[3]修改|查看服务器主配置文件')
        print('[0]返回主菜单')
        shuru = input('输入对应数字以继续：')

        if shuru == '1':
            list_mods(config['server_dir'])
        elif shuru == '2':
            list_plugins(config['server_dir'])
        elif shuru == '3':
            modify_server_properties(config['server_dir'])
        elif shuru == '0':
            break
        else:
            print('无效输入，请输入正确的数字。')
            input('按回车键返回菜单...')

def list_mods(server_dir):
    mods_dir = os.path.join(server_dir, 'mods')
    if os.path.isdir(mods_dir):
        mods = os.listdir(mods_dir)
        if mods:
            print('模组列表：')
            for mod in mods:
                print(mod)
        else:
            print('模组目录为空。')
    else:
        print('未找到模组目录。')
    input('按回车键返回菜单...')

def list_plugins(server_dir):
    plugins_dir = os.path.join(server_dir, 'plugins')
    if os.path.isdir(plugins_dir):
        plugins = os.listdir(plugins_dir)
        if plugins:
            print('插件列表：')
            for plugin in plugins:
                print(plugin)
        else:
            print('插件目录为空。')
    else:
        print('未找到插件目录。')
    input('按回车键返回菜单...')

def modify_server_properties(server_dir):
    properties_path = os.path.join(server_dir, SERVER_PROPERTIES)
    if not os.path.isfile(properties_path):
        print(f'未找到{SERVER_PROPERTIES}文件。')
        input('按回车键返回菜单...')
        return

    with open(properties_path, 'r') as f:
        properties = f.readlines()

    print('服务器主配置文件内容：')
    for line in properties:
        print(line.strip())

    while True:
        print('[1]修改服务器端口')
        print('[2]修改游戏模式')
        print('[3]修改正版验证')
        print('[0]返回上级菜单')
        shuru = input('输入对应数字以继续：')

        if shuru == '1':
            new_port = input('请输入新的服务器端口号：')
            update_property(properties, 'server-port', new_port)
        elif shuru == '2':
            new_mode = input('请输入新的游戏模式（0-生存，1-创造，2-冒险，3-观察者）：')
            update_property(properties, 'gamemode', new_mode)
        elif shuru == '3':
            online_mode = input('是否开启正版验证（true/false）：')
            update_property(properties, 'online-mode', online_mode)
        elif shuru == '0':
            break
        else:
            print('无效输入，请输入正确的数字。')

    with open(properties_path, 'w') as f:
        f.writelines(properties)

    print(f'{SERVER_PROPERTIES}文件已更新。')
    input('按回车键返回菜单...')

def update_property(properties, key, value):
    for i in range(len(properties)):
        if properties[i].startswith(key):
            properties[i] = f'{key}={value}\n'
            break

def read_server_port(server_dir):
    properties_path = os.path.join(server_dir, SERVER_PROPERTIES)
    if os.path.isfile(properties_path):
        with open(properties_path, 'r') as f:
            properties = f.readlines()
        for line in properties:
            if line.startswith('server-port'):
                return line.strip().split('=')[1]
    return '25565'  # 默认端口

def display_info():
    clear_screen()
    print('==========================================')
    print('本工具由QQ1502271252开发制作')
    print('制作不易，感谢下载使用！')
    print('==========================================')
    input('按回车键返回菜单...')
    clear_screen()

def baidu_translate(query, from_lang='en', to_lang='zh'):
    app_id = '您的百度翻译id'
    secret_key = '您的百度翻译密钥'
    
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

def translation_menu():
    languages = {
        '1': ('英语', 'en'),
        '2': ('俄语', 'ru'),
        '3': ('法语', 'fra'),
        '4': ('德语', 'de')
    }

    to_lang = 'zh'

    while True:
        print('选择原语言：')
        for key, (name, code) in languages.items():
            print(f'[{key}] {name}')
        from_lang_key = input('请选择原语言（输入对应数字）：')

        if from_lang_key in languages:
            from_lang = languages[from_lang_key][1]

            query = input('请输入要翻译的文本：')
            baidu_translate(query, from_lang, to_lang)
        else:
            print('无效的语言选择，请重新输入。')

        cont = input('是否继续翻译？（y/n）：')
        if cont.lower() != 'y':
            break

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

config = load_config()
while True:
    choice = main_menu()
    if choice == '1':
        start_server(config)
    elif choice == '2':
        config = configure_server()
    elif choice == '3':
        server_files_menu(config)
    elif choice == '4':
        display_info()
    elif choice == '5':
        translation_menu()
    elif choice == '0':
        print('关闭软件...')
        break
    else:
        print('无效输入，请输入正确的数字。')
        input('按回车键返回菜单...')
        clear_screen()
