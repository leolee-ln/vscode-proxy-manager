# 安装说明

## 系统级安装（推荐）

### 安装步骤

```bash
# 1. 克隆或下载项目
git clone https://github.com/leolee-ln/vscode-proxy-manager.git
cd vscode-proxy-manager

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行安装脚本（需要 sudo 权限）
./install.sh
```

### 安装后的文件位置

- **命令**: `/usr/local/bin/vscode-proxy` (软链接)
- **脚本**: `项目目录/vscode-proxy.sh`
- **Python 程序**: `项目目录/manage_vscode_proxy.py`
- **系统配置**: `/etc/vscode-proxy/proxy.conf`

### 使用

安装后可以在任何位置使用：

```bash
vscode-proxy enable   # 启用代理
vscode-proxy disable  # 禁用代理
vscode-proxy status   # 查看状态
```

### 修改配置

```bash
sudo vim /etc/vscode-proxy/proxy.conf
```

### 卸载

```bash
./uninstall.sh
```

---

## 本地使用（开发/测试）

如果不想系统级安装，可以直接使用：

```bash
# 1. 创建配置文件
cp config.yaml.example config.yaml
vim config.yaml

# 2. 直接运行
./vscode-proxy.sh enable
./vscode-proxy.sh disable
./vscode-proxy.sh status
```

---

## 配置文件说明

### 系统级配置文件

- **位置**: `/etc/vscode-proxy/proxy.conf`
- **用途**: 系统级安装后使用
- **优先级**: 最高
- **修改**: 需要 sudo 权限

### 项目配置文件

- **位置**: `项目目录/config.yaml`
- **用途**: 本地开发/测试
- **优先级**: 当系统配置不存在时使用
- **修改**: 普通用户权限

### 配置文件命名说明

- `proxy.conf` - 系统级配置，符合 `/etc` 目录命名规范
- `config.yaml` - 项目级配置，开发友好

---

## 常见问题

### Q: 为什么需要 sudo 权限？

A: 需要 sudo 权限用于：
1. 创建 `/usr/local/bin/vscode-proxy` 软链接
2. 创建 `/etc/vscode-proxy/` 目录
3. 复制配置文件到 `/etc/vscode-proxy/proxy.conf`

### Q: 安装后配置文件在哪里？

A: `/etc/vscode-proxy/proxy.conf`

### Q: 如何更新配置？

A: `sudo vim /etc/vscode-proxy/proxy.conf`

### Q: 卸载后配置文件会被删除吗？

A: 卸载脚本会询问是否删除配置文件，你可以选择保留。

### Q: 可以在不同服务器上使用不同的配置吗？

A: 可以。每个服务器的 `/etc/vscode-proxy/proxy.conf` 可以独立配置。

---

## 未来计划

- [ ] 支持用户级安装（`~/.local/bin/` 和 `~/.config/vscode-proxy/`）
