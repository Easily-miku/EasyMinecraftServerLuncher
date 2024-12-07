# EasyMCSL 2.0.1 更新日志

## 版本 2.0.1 - 2024年12月

### 新功能

- **EULA 同意自动处理**：
  - 新增了启动服务器时自动检查 `eula.txt` 文件的功能。如果文件中没有同意 EULA（`eula=false`），系统会提示用户是否同意，并且在用户同意后自动修改 `eula.txt` 为 `eula=true`，从而自动同意 Mojang 的 EULA 条款。

- **Java 版本选择**：
  - 用户现在可以选择使用系统默认的 `java` 命令来启动服务器，或者输入自定义的 Java 路径。这样可以确保使用特定版本的 Java 来运行 Minecraft 服务器，避免了不同 Java 版本对服务器性能或兼容性可能带来的影响。

### 功能优化

- **更精细的错误处理**：
  - 在 `eula.txt` 文件检查、Java 路径选择等环节增加了更多的错误提示与校验，确保用户输入正确有效的路径或选择。
  
- **服务器配置界面优化**：
  - 对服务器配置的界面进行了细微的改进，用户交互更加清晰友好。

- **增强的文件路径处理**：
  - 在一些文件操作中增加了对路径是否有效的判断，避免路径错误导致的问题。

### 修复的 Bug

- **修复服务器文件目录查找问题**：
  - 解决了某些情况下，找不到正确的 `server.jar` 文件的问题。现在会更准确地查找和提示。
  
- **修复启动命令中的路径错误**：
  - 修正了当路径中包含空格时，启动命令无法正确执行的问题。

### 其他改进

- **改进配置文件存储**：
  - 配置文件的保存与读取过程得到了优化，用户的服务器配置现在可以更可靠地保存和恢复。
  
- **更新依赖库**：
  - 更新了部分外部依赖库，以提高程序的稳定性和兼容性。

---

## 版本升级说明

1. **Java 选择功能**：在启动服务器时，你将被要求选择是否使用自定义的 Java 路径。如果没有自定义 Java，你可以选择使用系统默认的 Java。
2. **EULA 同意自动处理**：在启动服务器之前，程序会自动检查 `eula.txt` 文件，并确保用户已同意 Mojang 的 EULA。如果没有同意，程序会提示用户是否同意，并在同意后自动设置 `eula=true`。
3. **配置文件存储**：服务器配置将保存在本地 `server_config.json` 文件中，方便你随时调整和保存配置。

---

## 安装和更新

1. **下载最新版本**：
   - 你可以通过我们的官网或 GitHub 页面下载最新的版本。

2. **升级说明**：
   - 只需将新版程序替换掉旧版程序，配置文件和服务器数据将不会丢失。

---

## 使用指南与常见问题解答

### 使用指南

#### 1. 配置服务器

- **第一次使用时**，启动程序后，点击主菜单中的 `[2] 配置服务器`，你将需要输入以下配置项：
  - **服务器路径**：指定 Minecraft 服务端 `.jar` 文件所在的目录。
  - **内存大小**：设置启动时分配给服务器的内存大小，通常格式为 `1024M` 或 `2G`，确保分配的内存不超过系统可用内存。
  - **启动参数**：输入 Java 启动时的额外参数，如优化参数（例如 `-XX:+UseG1GC`）等。

  配置完成后，这些设置将保存在 `server_config.json` 文件中，方便后续使用。

#### 2. 启动服务器

- 配置好服务器后，返回主菜单，选择 `[1] 启动服务器`。
- 如果 `eula.txt` 文件未同意 EULA，系统会提示你是否同意 Mojang 的 EULA。若同意，程序会自动将 `eula=false` 改为 `eula=true`，然后继续启动服务器。
- 程序将根据你配置的路径和内存启动服务器。你可以选择使用系统默认的 Java 路径，或者手动输入自定义的 Java 路径。

#### 3. 修改服务器设置

- 在主菜单中，选择 `[3] 服务器文件`，你将进入服务器文件管理界面，可以查看和修改以下内容：
  - **模组列表**：查看当前服务器安装的所有模组。
  - **插件列表**：查看服务器的插件列表。
  - **主配置文件**：修改 `server.properties` 配置文件，包括端口号、游戏模式、正版验证等设置。

#### 4. 翻译功能

- 选择主菜单中的 `[5] 翻译`，你可以将输入的文本翻译成多种语言，包括：
  - 英语（`en`）
  - 俄语（`ru`）
  - 法语（`fra`）
  - 德语（`de`）

#### 5. 下载 Minecraft 服务端

- 在主菜单中选择 `[6] 下载Minecraft服务端`，程序会列出支持的所有 Minecraft 服务端，选择你需要的版本进行下载。

### 常见问题解答

#### 1. **如何处理 EULA 问题？**
- 在启动服务器时，如果 `eula.txt` 文件未同意 EULA（即 `eula=false`），程序会自动检测并提示你是否同意 Mojang 的 EULA 条款。如果你选择同意，程序会自动将 `eula=false` 修改为 `eula=true`，然后继续启动服务器。

#### 2. **我可以指定自己的 Java 路径吗？**
- 是的，程序允许你在启动时选择使用系统默认的 Java 路径，或者输入自定义的 Java 路径。这意味着你可以选择特定版本的 Java 来启动服务器，以确保兼容性和性能。

#### 3. **如何配置服务器内存？**
- 在配置服务器时，程序会要求你输入启动时的内存大小。内存可以使用例如 `1024M` 或 `2G` 的格式，确保输入的内存大小不会超过系统的物理内存。若不清楚合适的内存值，可以参考 Minecraft 官方推荐的内存配置。

#### 4. **如何查看和修改 `server.properties` 文件？**
- 你可以通过主菜单中的 `[3] 服务器文件` 进入服务器文件管理界面，选择修改 `server.properties` 文件。你可以修改游戏模式、端口号、是否开启正版验证等设置。

#### 5. **服务器文件找不到怎么办？**
- 如果系统无法自动找到服务器文件（`server.jar`），程序会提示你提供服务器文件所在的路径。确保你已正确下载并解压了 Minecraft 服务端文件。如果你不确定服务器文件的位置，可以尝试检查文件目录或重新下载。

#### 6. **如何下载 Minecraft 服务端？**
- 在主菜单中选择 `[6] 下载Minecraft服务端`，程序会列出支持的服务器类型和版本，选择需要的服务端和版本后，程序将自动从支持的源下载 Minecraft 服务端。

#### 7. **如何查看和修改模组或插件？**
- 在主菜单中选择 `[3] 服务器文件`，你将能够查看服务器安装的所有模组和插件。如果需要修改或添加新的模组/插件，可以直接操作该目录下的文件。

#### 8. **程序提示路径错误怎么办？**
- 如果路径无效或文件不存在，程序会提示错误并要求你输入正确的路径。确保输入的路径格式正确，并且文件或文件夹确实存在。

---

## 致谢

感谢各位用户的支持与反馈！EasyMCSL 将持续更新和优化，以提供更好的使用体验。如有任何问题或建议，欢迎提交 issue 或联系开发者。


## 开源协议

本项目采用 **GNU General Public License v3.0 (GPL-3.0)** 协议，详细信息如下：

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc.
https://www.gnu.org/licenses/gpl-3.0.html

Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

TERMS AND CONDITIONS

    Definitions.

    "This License" refers to the GNU General Public License.
    "The Program" refers to the software that you are modifying or distributing.
    "You" refers to the person or entity exercising rights under this License.

    You may copy, modify, and distribute the Program provided that all modifications are licensed under GPL-3.0.
    You must make the source code available for all copies and modifications you distribute.
    If you distribute the Program or modifications, you must do so under this same license.

