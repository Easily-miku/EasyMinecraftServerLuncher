import os
import subprocess
import hashlib
import requests
import random
import json
from tqdm import tqdm
import colorama
from colorama import Fore

colorama.init(autoreset=True)

# 大标题和小标题
TITLE_BIG = Fore.CYAN + '''==========================================
███████ ███    ███  ██████ ███████ ██
██      ████  ████ ██      ██      ██
█████   ██ ████ ██ ██      ███████ ██
██      ██  ██  ██ ██           ██ ██
███████ ██      ██  ██████ ███████ ███████
=========================================='''

TITLE_SMALL = Fore.YELLOW + '=欢迎使用EasyMCSL轻易我的世界开服工具='

CONFIG_FILE = 'server_config.json'
SERVER_PROPERTIES = 'server.properties'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_message(message, color=Fore.WHITE, input_prompt=False):
    print(color + message)
    if input_prompt:
        input('按回车键继续...')


def main_menu():
    clear_screen()
    print(TITLE_BIG)
    print(TITLE_SMALL)
    menu = [
        '[1]启动服务器',
        '[2]配置服务器',
        '[3]服务器文件',
        '[4]信息',
        '[5]翻译',
        '[6]下载Minecraft服务端',
        '[0]关闭软件'
    ]
    print(Fore.GREEN + '\n'.join(menu))
    print(Fore.CYAN + '==========================================')
    return input(Fore.WHITE + '输入对应数字以继续：')

def is_eula_accepted(eula_file_path):
    """检查 eula.txt 文件中是否已同意 EULA"""
    if not os.path.isfile(eula_file_path):
        return False  # 如果 eula.txt 文件不存在，表示未同意
    with open(eula_file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('eula='):
                return line.strip().lower() == 'eula=true'
    return False

def accept_eula(eula_file_path):
    """自动同意 EULA"""
    with open(eula_file_path, 'w') as file:
        file.write('eula=true\n')  # 将 eula 设置为 true
    print(Fore.GREEN + "已自动同意 EULA。")

def start_server(config):
    if not config:
        print(Fore.RED + '[错误] 未找到服务器配置，请先进行配置。')
        input('按回车键返回菜单...')
        return
    
    server_dir = config['server_dir']
    server_name = config['server_name']
    memory_size = config['memory_size']
    optimization_code = config['optimization_code']
    port = read_server_port(server_dir)
    
    # 检查 eula.txt 文件并处理
    eula_file_path = os.path.join(server_dir, 'eula.txt')
    if not is_eula_accepted(eula_file_path):
        print(Fore.YELLOW + "未同意 EULA，您必须同意 EULA 才能启动服务器。")
        agree = input("是否同意 EULA（输入 'yes' 同意，其他键退出）：").strip().lower()
        if agree == 'yes':
            accept_eula(eula_file_path)
            print(Fore.GREEN + "已同意 EULA，继续启动服务器...")
        else:
            print(Fore.RED + "您必须同意 EULA 才能启动服务器。退出程序...")
            input('按回车键返回菜单...')
            return
    
    # 选择 Java 版本
    java_command = choose_java_version()
    if not java_command:
        input('按回车键返回菜单...')
        return

    server_path = os.path.join(server_dir, server_name)
    clear_screen()
    print(TITLE_BIG)
    print(f'[信息] 正在启动服务器（端口号: {port}）...')
    
    try:
        command = f"{java_command} -Xmx{memory_size} -Xms{memory_size} {optimization_code} -jar {server_path} nogui"
        subprocess.run(command, shell=True)
        print(Fore.GREEN + '[信息] 服务器启动完成。')
    except Exception as e:
        print(Fore.RED + f'[错误] 启动服务器时发生错误：{e}')
        input('按回车键返回菜单...')
    clear_screen()


def configure_server():
    clear_screen()
    print(Fore.YELLOW + '进入服务器配置...')
    server_dir = input('请输入服务器目录路径：') if not find_server_jar() else '.'
    server_name = find_server_jar(server_dir)
    if not server_name:
        display_message('未找到服务器文件，请提供有效的目录路径。', Fore.RED, True)
        return None

    print(Fore.GREEN + f'已找到服务器文件：{server_name}')
    memory_size = input('请输入启动内存大小（例如1024M）：')
    optimization_code = input('请输入启动优化代码（例如 -XX:+UseG1GC）：')

    config = {
        'server_dir': server_dir,
        'server_name': server_name,
        'memory_size': memory_size,
        'optimization_code': optimization_code
    }
    save_config(config)
    display_message(f'服务器配置完成。\n服务器文件：{server_name}\n启动内存大小：{memory_size}\n启动优化代码：{optimization_code}', Fore.GREEN, True)
    return config


def list_directory_items(directory, item_type):
    path = os.path.join(directory, item_type)
    if os.path.isdir(path):
        items = os.listdir(path)
        if items:
            print(f'{item_type.capitalize()} 列表：')
            for item in items:
                print(item)
        else:
            print(f'{item_type.capitalize()} 目录为空。')
    else:
        print(f'未找到{item_type}目录。')
    input('按回车键返回菜单...')

def choose_java_version():
    """选择Java版本：默认或自定义路径"""
    print(Fore.YELLOW + '[1] 使用系统默认的 Java')
    print(Fore.YELLOW + '[2] 使用自定义的 Java 路径')
    choice = input('请选择 Java 版本（输入对应数字）：')

    if choice == '1':
        return 'java'  # 默认的 Java 命令
    elif choice == '2':
        java_path = input('请输入自定义的 Java 路径：')
        if os.path.isfile(java_path):
            return java_path
        else:
            print(Fore.RED + '指定的路径无效。请确保该路径指向一个有效的 Java 可执行文件。')
            return None
    else:
        print(Fore.RED + '无效的选择。')
        return None

def modify_server_properties(server_dir):
    properties_path = os.path.join(server_dir, SERVER_PROPERTIES)
    if not os.path.isfile(properties_path):
        display_message(f'未找到{SERVER_PROPERTIES}文件。', Fore.RED, True)
        return

    with open(properties_path, 'r') as f:
        properties = f.readlines()

    print('服务器主配置文件内容：')
    for line in properties:
        print(line.strip())

    while True:
        options = [
            ('修改服务器端口', 'server-port'),
            ('修改游戏模式', 'gamemode'),
            ('修改正版验证', 'online-mode'),
            ('返回上级菜单', None)
        ]
        for i, (desc, _) in enumerate(options):
            print(f'[{i + 1}] {desc}')
        choice = input('输入对应数字以继续：')

        if choice == '1':
            new_port = input('请输入新的服务器端口号：')
            update_property(properties, 'server-port', new_port)
        elif choice == '2':
            new_mode = input('请输入新的游戏模式（0-生存，1-创造，2-冒险，3-观察者）：')
            update_property(properties, 'gamemode', new_mode)
        elif choice == '3':
            online_mode = input('是否开启正版验证（true/false）：')
            update_property(properties, 'online-mode', online_mode)
        elif choice == '4':
            break
        else:
            print('无效输入，请输入正确的数字。')

    with open(properties_path, 'w') as f:
        f.writelines(properties)

    display_message(f'{SERVER_PROPERTIES}文件已更新。', Fore.GREEN, True)


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
    return '25565'


def display_info():
    clear_screen()
    print('==========================================')
    print('本工具由QQ1502271252开发制作')
    print('制作不易，感谢下载使用！')
    print('==========================================')
    input('按回车键返回菜单...')
    clear_screen()


def baidu_translate(query, from_lang='en', to_lang='zh'):
    app_id, secret_key = '', ''
    salt = random.randint(32768, 65536)
    sign = hashlib.md5((app_id + query + str(salt) + secret_key).encode()).hexdigest()
    params = {
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }
    try:
        response = requests.get("http://api.fanyi.baidu.com/api/trans/vip/translate", params=params)
        result = response.json()
        if 'trans_result' in result:
            print(f'[信息] 翻译结果：{result["trans_result"][0]["dst"]}')
        else:
            print(f'[错误] 翻译失败：{result}')
    except requests.RequestException as e:
        print(f'[错误] 请求翻译时发生错误：{e}')
    except json.JSONDecodeError as e:
        print(f'[错误] 解析翻译响应时发生错误：{e}')


def translation_menu():
    languages = {'1': ('英语', 'en'), '2': ('俄语', 'ru'), '3': ('法语', 'fra'), '4': ('德语', 'de')}
    to_lang = 'zh'

    while True:
        print('选择原语言：')
        for key, (name, _) in languages.items():
            print(f'[{key}] {name}')
        from_lang_key = input('请选择原语言（输入对应数字）：')

        if from_lang_key in languages:
            from_lang = languages[from_lang_key][1]
            query = input('请输入要翻译的文本：')
            baidu_translate(query, from_lang, to_lang)
        else:
            print('无效的语言选择，请重新输入。')

        if input('是否继续翻译？（y/n）：').lower() != 'y':
            break


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def download_minecraft_server():
    servers = fetch_supported_servers()
    if not servers:
        return

    print("支持的服务端列表：")
    for i, server in enumerate(servers):
        print(f"{i + 1}. 名称: {server['name']}, 标签: {server['tag']}, 推荐: {server['recommend']}")

    choice = int(input("请输入要下载的服务端编号: ")) - 1
    if choice < 0 or choice >= len(servers):
        print("无效的选择。")
        return

    server_name = servers[choice]['name']
    server_info = fetch_server_info(server_name)
    if not server_info:
        return

    server_data = server_info['data']
    print(f"服务端名字: {server_data['name']}, 服务端类型: {server_data['tag']}")
    print("支持的版本：")
    for i, version in enumerate(server_data['mc_versions']):
        print(f"[{i + 1}] {version}")

    version_choice = int(input("请输入要下载的版本编号: ")) - 1
    if version_choice < 0 or version_choice >= len(server_data['mc_versions']):
        print("无效的选择。")
        return

    version = server_data['mc_versions'][version_choice]
    core_info = fetch_core_version(server_name, version)
    if not core_info:
        return

    if 'data' in core_info and 'builds' in core_info['data'] and len(core_info['data']['builds']) > 0:
        core_version = core_info['data']['builds'][0]['core_version']
        download_info = fetch_download_url(server_name, version, core_version)
        if download_info and 'data' in download_info and 'download_url' in download_info['data']:
            download_url = download_info['data']['download_url']
            download_core(download_url, server_name, version)
        else:
            print("未能获取到下载URL。")
    else:
        print("未能获取到核心版本信息。")


def fetch_supported_servers():
    url = "https://download.fastmirror.net/api/v3"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'] if data.get('code') == 'fin::success' and data['success'] else None
    print(f"从API获取数据失败。状态码: {response.status_code}")
    return None


def fetch_server_info(server_name):
    return fetch_api_data(f"https://download.fastmirror.net/api/v3/{server_name}")


def fetch_core_version(server_name, version):
    return fetch_api_data(f"https://download.fastmirror.net/api/v3/{server_name}/{version}")


def fetch_download_url(server_name, version, core_version):
    return fetch_api_data(f"https://download.fastmirror.net/api/v3/{server_name}/{version}/{core_version}")


def fetch_api_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"从API获取数据失败。状态码: {response.status_code}")
    return None

def server_files_menu(config):
    if not config:
        display_message('[错误] 未找到服务器配置，请先进行配置。', Fore.RED, True)
        return

    server_dir = config['server_dir']
    print(Fore.YELLOW + f'当前服务器目录：{server_dir}')
    while True:
        print('\n[1] 列出所有文件')
        print('[2] 修改服务器属性文件')
        print('[0] 返回主菜单')
        choice = input('请输入数字选择操作：')

        if choice == '1':
            list_directory_items(server_dir, '')
        elif choice == '2':
            modify_server_properties(server_dir)
        elif choice == '0':
            break
        else:
            print(Fore.RED + '无效输入，请重新输入。')


def find_server_jar(directory=None):
    if not directory:
        directory = os.getcwd()  # 默认当前工作目录
    server_jar_files = [f for f in os.listdir(directory) if f.endswith('.jar')]

    if not server_jar_files:
        return None
    # 假设第一个jar文件就是服务器主文件
    return server_jar_files[0]


def download_core(download_url, server_name, version):
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        with open(f"{server_name}-{version}.jar", "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        print(f"{server_name}-{version}.jar 下载完成。")
    else:
        print(f"下载失败。状态码: {response.status_code}")


if __name__ == '__main__':
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
        elif choice == '6':
            download_minecraft_server()
        elif choice == '0':
            print(Fore.YELLOW + '关闭软件...')
            break
        else:
            print(Fore.RED + '无效输入，请输入正确的数字。')
            input('按回车键返回菜单...')
        clear_screen()
