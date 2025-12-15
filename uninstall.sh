#!/bin/bash
# VSCode Proxy Manager 卸载脚本
# 用于从系统中卸载 vscode-proxy 命令

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

INSTALL_DIR="/usr/local/bin"
LINK_NAME="vscode-proxy"
LINK_PATH="${INSTALL_DIR}/${LINK_NAME}"

echo "=========================================="
echo "  VSCode Proxy Manager 卸载程序"
echo "=========================================="
echo ""

# 检查软链接是否存在
if [ ! -e "$LINK_PATH" ]; then
    echo -e "${YELLOW}! 未找到安装的 vscode-proxy 命令${NC}"
    echo "可能已经被卸载或从未安装"
    exit 0
fi

# 检查是否是软链接
if [ ! -L "$LINK_PATH" ]; then
    echo -e "${RED}错误: ${LINK_PATH} 存在但不是软链接${NC}"
    echo "为了安全，请手动删除该文件"
    exit 1
fi

# 显示当前链接信息
echo "当前安装信息:"
echo "  位置: ${LINK_PATH}"
echo "  指向: $(readlink -f "$LINK_PATH")"
echo ""

# 确认卸载
read -p "确定要卸载 vscode-proxy 命令吗？(y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "卸载已取消"
    exit 0
fi

# 检查是否需要 sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}注意: 需要 sudo 权限来卸载${NC}"
    echo ""
fi

# 删除软链接
echo "→ 删除软链接..."
if sudo rm "$LINK_PATH"; then
    echo -e "${GREEN}✓${NC} 软链接已删除"
else
    echo -e "${RED}✗ 删除失败${NC}"
    exit 1
fi

echo ""

# 询问是否删除配置文件
SYSTEM_CONFIG_DIR="/etc/vscode-proxy"
SYSTEM_CONFIG_FILE="${SYSTEM_CONFIG_DIR}/proxy.conf"

if [ -f "$SYSTEM_CONFIG_FILE" ]; then
    echo ""
    read -p "是否同时删除系统配置文件 ${SYSTEM_CONFIG_FILE}？(y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "→ 删除配置文件..."
        if sudo rm -f "$SYSTEM_CONFIG_FILE"; then
            echo -e "${GREEN}✓${NC} 配置文件已删除"
        fi
        
        # 如果目录为空，也删除目录
        if [ -d "$SYSTEM_CONFIG_DIR" ] && [ -z "$(ls -A $SYSTEM_CONFIG_DIR)" ]; then
            if sudo rmdir "$SYSTEM_CONFIG_DIR"; then
                echo -e "${GREEN}✓${NC} 配置目录已删除"
            fi
        fi
    else
        echo "配置文件已保留: ${SYSTEM_CONFIG_FILE}"
    fi
fi

echo ""
echo "=========================================="
echo -e "${GREEN}卸载成功！${NC}"
echo "=========================================="
echo ""
echo "vscode-proxy 命令已从系统中移除"
echo "项目文件仍保留在原位置，你仍然可以使用："
echo "  ./vscode-proxy.sh enable"
echo ""
