# VSCode Proxy Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

一个用于管理 VSCode Remote Server 代理配置的命令行工具。

## 功能特性

- ✅ 快速启用/禁用 VSCode Server 的代理配置
- ✅ 智能检测配置变化，避免重复操作
- ✅ 支持自定义代理主机和端口
- ✅ 自动备份配置文件（支持多版本备份）
- ✅ 仅在配置变化时生成备份，保持备份整洁
- ✅ 灵活的 YAML 配置文件
- ✅ 命令行友好的操作界面
- ✅ 查看当前代理状态
- ✅ 代理密码信息自动隐藏显示

## 应用场景

当你通过 SSH 连接到远程服务器使用 VSCode Remote 时，如果需要为 VSCode Server 配置代理（例如访问插件市场、GitHub Copilot 等），手动编辑 `~/.vscode-server/data/Machine/settings.json` 会比较繁琐。本工具可以帮你快速管理这些配置。

## 安装

### 方式 1: 系统安装（推荐）

```bash
git clone https://github.com/leolee-ln/vscode-proxy-manager.git
cd vscode-proxy-manager
pip install -r requirements.txt

# 安装到系统（需要 sudo 权限）
./install.sh
```

安装后可在任何位置使用 `vscode-proxy` 命令。

### 方式 2: 本地使用（不安装到系统）

```bash
git clone https://github.com/leolee-ln/vscode-proxy-manager.git
cd vscode-proxy-manager
pip install -r requirements.txt

# 直接使用脚本
./vscode-proxy.sh enable
```

## 依赖要求

本工具需要 Python 3.6+ 和以下依赖：

```bash
# 自动安装所有依赖
pip install -r requirements.txt

# 或手动安装
pip install PyYAML
```

## 配置

### 配置文件位置

- **系统级安装**：配置文件位于 `/etc/vscode-proxy/proxy.conf`
- **本地使用**：配置文件位于项目目录的 `config.yaml`

安装脚本会自动将配置文件复制到系统目录。

### 编辑配置

**系统级安装后：**

```bash
sudo vim /etc/vscode-proxy/proxy.conf
```

**本地使用：**

```bash
cp config.yaml.example config.yaml
vim config.yaml
```

### 配置选项

```yaml
proxy:
  host: "localhost"         # 代理主机地址
  port: 7890                # 代理端口
  enabled: true             # 默认是否启用
  proxy_support: "override" # 代理支持模式
  strict_ssl: false         # 是否严格验证 SSL

python:
  interpreter: ""           # Python 解释器路径（留空使用系统默认）

backup:
  enabled: true             # 是否启用备份
  suffix: ".backup"         # 备份文件后缀
  max_backups: 5            # 最大备份文件数量
```

## 使用方法

### 基本命令

```bash
# 如果已通过 install.sh 安装到系统
vscode-proxy enable   # 启用代理
vscode-proxy disable  # 禁用代理
vscode-proxy status   # 查看当前状态

# 或使用 shell 脚本运行（会自动读取 config.yaml 中的 Python 解释器）
./vscode-proxy.sh enable
./vscode-proxy.sh disable
./vscode-proxy.sh status

# 或使用 Python 直接运行
python manage_vscode_proxy.py enable
python manage_vscode_proxy.py disable
python manage_vscode_proxy.py status
```

### 高级用法

```bash
# 指定自定义代理地址和端口
python manage_vscode_proxy.py enable --host 127.0.0.1 --port 8888

# 使用自定义配置文件
python manage_vscode_proxy.py --config /path/to/config.yaml enable

# 自动确认（不提示）
python manage_vscode_proxy.py enable -y

# 使用别名命令
python manage_vscode_proxy.py on    # 等同于 enable
python manage_vscode_proxy.py off   # 等同于 disable
```

### 更新配置

如果修改了配置文件（如更改代理地址或端口），可以直接再次执行 `enable` 命令应用新配置：

```bash
# 1. 修改配置文件
vim /etc/vscode-proxy/proxy.conf    # 系统安装
# 或
vim config.yaml                     # 本地使用

# 2. 应用新配置
vscode-proxy enable

# 工具会自动检测配置变化并显示：
# INFO: 检测到配置变化:
#   ~ http.proxy: http://localhost:7890 → http://localhost:8080
# 确定要启用代理吗？(y/N):
```

**提示**：如果配置未发生变化，工具会显示"代理配置已是最新状态"并直接退出，无需确认。

### 快速设置

**方式 1: 使用安装脚本（推荐）**

```bash
# 安装到系统
./install.sh

# 现在可以在任何位置使用
vscode-proxy enable
vscode-proxy disable
vscode-proxy status

# 卸载（如果需要）
./uninstall.sh
```

**方式 2: 手动创建别名**

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
alias vscode-proxy='/path/to/vscode-proxy-manager/vscode-proxy.sh'
```

然后重新加载配置：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

## 工作原理

### 配置文件查找逻辑

工具按以下优先级查找配置文件：

1. **`/etc/vscode-proxy/proxy.conf`** - 系统级配置（安装后使用）
2. **`项目目录/config.yaml`** - 项目配置（开发/本地使用）
3. **默认配置** - 内置默认值

### 代理配置修改

本工具会修改 `~/.vscode-server/data/Machine/settings.json` 文件中的以下配置项：

```json
{
  "http.proxySupport": "override",
  "http.proxy": "http://localhost:7890",
  "http.proxyStrictSSL": false
}
```

每次修改前会自动创建备份文件，便于恢复。

## 备份管理

- 默认启用自动备份功能
- 备份文件格式：`settings.json.backup.YYYYmmdd_HHMMSS`
- 智能备份：仅在配置实际发生变化时才创建备份
- 自动清理旧备份，保留最近 5 个备份文件
- 可通过配置文件调整备份策略

## 配置变化检测

工具会在执行操作前自动检测配置变化：

- **启用代理时**：
  - 如果配置未发生变化，显示"代理配置已是最新状态"并退出
  - 如果有变化，显示具体变化内容并询问确认
  - 示例输出：
    ```
    INFO: 检测到配置变化:
      ~ http.proxy: http://localhost:7890 → http://localhost:8080
    ```

- **禁用代理时**：
  - 如果已处于禁用状态，显示"代理配置已是禁用状态"并退出
  - 如果需要禁用，询问确认后执行

- **密码隐藏**：
  - 如果代理 URL 包含密码，自动隐藏显示
  - 格式：`http://username:****@host:port`

## 常见问题

### Q: 找不到 settings.json 文件怎么办？

A: 如果文件不存在，工具会自动创建。这通常发生在首次使用 VSCode Remote 时。

### Q: 如何恢复到之前的配置？

A: 备份文件保存在 `~/.vscode-server/data/Machine/` 目录下，手动复制备份文件即可恢复。

### Q: 修改配置文件后如何应用？

A: 直接再次执行 `vscode-proxy enable` 命令即可。工具会自动检测配置变化，显示差异并询问确认。如果配置没有变化，会直接提示并退出。

### Q: 代理设置后不生效？

A: 需要重启 VSCode Remote 连接，或重新加载 VSCode 窗口（Reload Window）。

### Q: 支持哪些代理协议？

A: 目前支持 HTTP 代理。SOCKS 代理需要使用转换工具（如 privoxy）转为 HTTP 代理。

### Q: 为什么系统配置文件叫 proxy.conf 而不是 config.yaml？

A: 为了更好地表达文件用途和符合 Linux 配置文件命名规范：
- `proxy.conf` - 明确表示这是代理配置文件
- 避免与项目中的 `config.yaml` 混淆
- 符合 `/etc` 目录下配置文件的命名习惯（如 `nginx.conf`, `sshd.conf`）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 作者

Nan Li ([@leolee-ln](https://github.com/leolee-ln))

## 更新日志

完整的更新日志请查看 [CHANGELOG.md](CHANGELOG.md)。

### 最新版本

- **v1.0.2** (2025-12-15) - 功能增强：智能配置检测、优化用户体验
- **v1.0.1** (2025-12-15) - Bug 修复版本
- **v1.0.0** (2025-12-15) - 首次发布
