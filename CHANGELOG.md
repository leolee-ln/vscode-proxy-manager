# 更新日志

所有重要的项目变更都会记录在此文件中。

本文件格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.1] - 2025-12-15

### 修复
- 修复 vscode-proxy.sh 无法正确读取配置文件中 Python 解释器路径的问题
- 修复当配置文件不存在时 grep 命令报错的问题
- 改进 YAML 配置解析逻辑，正确提取 `interpreter:` 字段的值

### 改进
- 增强配置文件读取的健壮性
- 添加配置文件存在性检查
- 优化引号和换行符处理

## [1.0.0] - 2025-12-15

### 新增功能
- VSCode Proxy Manager 首次发布
- 支持启用/禁用代理配置
- 自动备份功能，支持版本控制
- YAML 配置文件支持
- 多选项命令行界面
- 当前代理配置状态显示
- Shell 脚本包装器，便于执行
- 完善的错误处理和日志记录
- 系统级安装脚本（install.sh）
- 卸载脚本（uninstall.sh）

### 核心特性
- 快速启用/禁用代理命令
- 自定义代理主机和端口
- 自动配置文件备份（最多保留 5 个版本）
- 用户友好的命令行界面
- 灵活的 YAML 配置
- 多种命令别名（enable/on, disable/off）
- 智能配置文件查找（系统 → 项目 → 默认）

### 文档
- 完整的 README 安装和使用说明
- 示例配置文件（config.yaml.example）
- 详细安装指南（INSTALL.md）
- 贡献指南（CONTRIBUTING.md）
- MIT 开源协议
