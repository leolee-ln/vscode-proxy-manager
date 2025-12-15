#!/bin/bash
# VSCode代理管理器运行脚本

# 获取脚本真实路径（解析软链接）
SCRIPT_REAL_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_REAL_PATH")"

# 配置文件路径（按优先级查找）
if [ -f "/etc/vscode-proxy/proxy.conf" ]; then
    # 系统级配置（最高优先级）
    CONFIG_FILE="/etc/vscode-proxy/proxy.conf"
elif [ -f "${SCRIPT_DIR}/config.yaml" ]; then
    # 项目目录配置（开发/测试用）
    CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
else
    echo "警告: 未找到配置文件，将使用默认配置"
    echo "系统配置: /etc/vscode-proxy/proxy.conf"
    echo "项目配置: ${SCRIPT_DIR}/config.yaml"
    echo ""
    CONFIG_FILE=""
fi

# 从配置文件读取Python解释器路径
PYTHON_PATH=$(grep -A1 'interpreter:' "$CONFIG_FILE" | tail -1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# 清理Python路径（移除可能的引号）
PYTHON_PATH=$(echo "$PYTHON_PATH" | sed "s/^['\"]//;s/['\"]$//")

# 如果配置中未指定Python路径，则使用系统默认
if [ -z "$PYTHON_PATH" ] || [ "$PYTHON_PATH" = '""' ] || [ "$PYTHON_PATH" = "''" ]; then
    PYTHON_PATH="python3"
fi

# 检查Python是否可用
if ! command -v "$PYTHON_PATH" &> /dev/null; then
    echo "错误: Python解释器 '$PYTHON_PATH' 不可用"
    echo "请修改 config.yaml 中的 python.interpreter 配置"
    exit 1
fi

# 传递所有参数给Python脚本
echo "使用Python: $PYTHON_PATH"
echo "配置文件: $CONFIG_FILE"
echo ""

# 执行Python脚本（使用绝对路径）
if [ -n "$CONFIG_FILE" ]; then
    exec "$PYTHON_PATH" "${SCRIPT_DIR}/manage_vscode_proxy.py" --config "$CONFIG_FILE" "$@"
else
    exec "$PYTHON_PATH" "${SCRIPT_DIR}/manage_vscode_proxy.py" "$@"
fi