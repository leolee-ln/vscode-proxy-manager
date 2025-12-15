# 贡献指南

感谢您对 VSCode Proxy Manager 项目的关注！本文档提供了参与贡献的指导和说明。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请在 GitHub 上创建 issue，并包含以下信息：

- 清晰、描述性的标题
- 详细的复现步骤
- 期望的行为 vs 实际的行为
- 您的环境信息（操作系统、Python 版本、VSCode 版本）
- 相关的日志或错误信息

### 功能建议

欢迎提出功能建议！请创建 issue 并包含：

- 清晰的功能描述
- 使用场景以及为什么这个功能有用
- 如果有的话，您的实现思路

### Pull Request 流程

1. Fork 本仓库
2. 为您的功能/修复创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. 进行修改：
   - 遵循现有的代码风格
   - 为复杂逻辑添加注释
   - 如需要，更新文档

4. 测试您的修改：
   ```bash
   # 测试主要功能
   ./vscode-proxy.sh status
   ./vscode-proxy.sh enable
   ./vscode-proxy.sh disable
   
   # 或直接使用 Python
   python manage_vscode_proxy.py status
   python manage_vscode_proxy.py enable
   python manage_vscode_proxy.py disable
   ```

5. 提交您的修改：
   ```bash
   git add .
   git commit -m "Add: 简要描述您的修改"
   ```

6. 推送到您的 fork 并提交 pull request

### 代码风格指南

- Python 代码遵循 PEP 8 规范
- 使用有意义的变量名和函数名
- 为所有函数和类添加文档字符串
- 保持函数简洁专注
- 适当使用类型提示

### 提交信息指南

格式：`<类型>: <描述>`

类型：
- `Add`：新功能
- `Fix`：Bug 修复
- `Update`：更新现有功能
- `Refactor`：代码重构
- `Docs`：文档修改
- `Test`：添加或更新测试

示例：
```
Add: 支持 SOCKS 代理
Fix: 修复备份文件删除问题
Docs: 更新安装说明
```

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/leolee-ln/vscode-proxy-manager.git
   cd vscode-proxy-manager
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 创建测试配置：
   ```bash
   cp config.yaml.example config.yaml
   ```

## 测试

在提交 PR 之前，请测试：

1. 所有命令行选项都能正常工作
2. 配置文件加载能优雅地处理错误
3. 备份功能按预期工作
4. 工具在不同 Python 版本（3.6+）上都能运行

## 有疑问？

随时创建 issue 提出您的问题或疑虑。

## 许可协议

贡献即表示您同意您的贡献将采用 MIT 许可协议。
