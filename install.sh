#!/bin/bash
# VSCode Proxy Manager 安装脚本
# 用于安装 vscode-proxy 命令到系统

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VSCODE_PROXY_SCRIPT="${SCRIPT_DIR}/vscode-proxy.sh"
INSTALL_DIR="/usr/local/bin"
LINK_NAME="vscode-proxy"
LINK_PATH="${INSTALL_DIR}/${LINK_NAME}"

echo "=========================================="
echo "  VSCode Proxy Manager 安装程序"
echo "=========================================="
echo ""

# 检查 vscode-proxy.sh 是否存在
if [ ! -f "$VSCODE_PROXY_SCRIPT" ]; then
    echo -e "${RED}错误: 找不到 vscode-proxy.sh${NC}"
    echo "请确保在项目根目录下运行此脚本"
    exit 1
fi

# 检查是否有 sudo 权限
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}注意: 需要 sudo 权限来安装到 ${INSTALL_DIR}${NC}"
    echo "将使用 sudo 执行安装..."
    echo ""
fi

# 赋予执行权限
echo "→ 赋予 vscode-proxy.sh 执行权限..."
chmod +x "$VSCODE_PROXY_SCRIPT"
echo -e "${GREEN}✓${NC} 执行权限已设置"
echo ""

# 检查是否已经存在软链接
if [ -L "$LINK_PATH" ]; then
    echo -e "${YELLOW}! 发现已存在的软链接: ${LINK_PATH}${NC}"
    
    # 检查链接是否指向当前脚本
    CURRENT_TARGET=$(readlink -f "$LINK_PATH")
    EXPECTED_TARGET=$(readlink -f "$VSCODE_PROXY_SCRIPT")
    
    if [ "$CURRENT_TARGET" = "$EXPECTED_TARGET" ]; then
        echo -e "${GREEN}✓${NC} 软链接已经正确指向当前脚本"
        echo ""
        echo "安装完成！"
        exit 0
    else
        echo "  当前链接指向: $CURRENT_TARGET"
        echo "  期望链接指向: $EXPECTED_TARGET"
        read -p "是否覆盖现有链接？(y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
        echo "→ 删除旧的软链接..."
        sudo rm "$LINK_PATH"
    fi
elif [ -e "$LINK_PATH" ]; then
    echo -e "${RED}错误: ${LINK_PATH} 已存在但不是软链接${NC}"
    echo "请手动处理该文件后重新运行安装脚本"
    exit 1
fi

# 创建软链接
echo "→ 创建软链接到 ${INSTALL_DIR}..."
if sudo ln -s "$VSCODE_PROXY_SCRIPT" "$LINK_PATH"; then
    echo -e "${GREEN}✓${NC} 软链接创建成功"
else
    echo -e "${RED}✗ 软链接创建失败${NC}"
    exit 1
fi

echo ""

# 系统级配置文件设置
SYSTEM_CONFIG_DIR="/etc/vscode-proxy"
SYSTEM_CONFIG_FILE="${SYSTEM_CONFIG_DIR}/proxy.conf"
SOURCE_CONFIG="${SCRIPT_DIR}/config.yaml"

echo "→ 设置系统配置文件..."
if [ -f "$SYSTEM_CONFIG_FILE" ]; then
    echo -e "${YELLOW}! 系统配置文件已存在: ${SYSTEM_CONFIG_FILE}${NC}"
    echo "  跳过配置文件安装"
else
    # 创建配置目录
    if sudo mkdir -p "$SYSTEM_CONFIG_DIR"; then
        echo -e "${GREEN}✓${NC} 配置目录已创建: ${SYSTEM_CONFIG_DIR}"
    else
        echo -e "${RED}✗ 创建配置目录失败${NC}"
        exit 1
    fi
    
    # 复制配置文件（优先使用 config.yaml，其次使用 config.yaml.example）
    EXAMPLE_CONFIG="${SCRIPT_DIR}/config.yaml.example"
    
    if [ -f "$SOURCE_CONFIG" ]; then
        # 优先使用 config.yaml
        if sudo cp "$SOURCE_CONFIG" "$SYSTEM_CONFIG_FILE"; then
            echo -e "${GREEN}✓${NC} 配置文件已安装: ${SYSTEM_CONFIG_FILE}"
            echo "  来源: config.yaml"
            sudo chmod 644 "$SYSTEM_CONFIG_FILE"
        else
            echo -e "${RED}✗ 复制配置文件失败${NC}"
            exit 1
        fi
    elif [ -f "$EXAMPLE_CONFIG" ]; then
        # 如果没有 config.yaml，使用 config.yaml.example
        if sudo cp "$EXAMPLE_CONFIG" "$SYSTEM_CONFIG_FILE"; then
            echo -e "${GREEN}✓${NC} 配置文件已安装: ${SYSTEM_CONFIG_FILE}"
            echo "  来源: config.yaml.example (示例配置)"
            echo -e "${YELLOW}  建议: 编辑配置文件以适配您的环境${NC}"
            sudo chmod 644 "$SYSTEM_CONFIG_FILE"
        else
            echo -e "${RED}✗ 复制配置文件失败${NC}"
            exit 1
        fi
    else
        # 都没有，显示警告但继续（使用默认配置）
        echo -e "${YELLOW}! 未找到配置文件 (config.yaml 或 config.yaml.example)${NC}"
        echo "  工具将使用内置的默认配置"
        echo "  您可以稍后手动创建: ${SYSTEM_CONFIG_FILE}"
    fi
fi

echo ""
echo "=========================================="
echo -e "${GREEN}安装成功！${NC}"
echo "=========================================="
echo ""
echo "配置文件: ${SYSTEM_CONFIG_FILE}"
echo "命令位置: ${LINK_PATH}"
echo ""
echo "现在你可以在任何位置使用以下命令："
echo ""
echo "  vscode-proxy enable   # 启用代理"
echo "  vscode-proxy disable  # 禁用代理"
echo "  vscode-proxy status   # 查看状态"
echo ""
echo "编辑配置："
echo "  sudo vim ${SYSTEM_CONFIG_FILE}"
echo ""
echo "查看更多帮助："
echo "  vscode-proxy --help"
echo ""
