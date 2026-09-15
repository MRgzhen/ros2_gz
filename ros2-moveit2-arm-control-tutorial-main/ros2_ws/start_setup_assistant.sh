#!/bin/bash
# MoveIt Setup Assistant 启动脚本
# 修复问题：HiDPI 200% 缩放屏（2880x1800, Xft.dpi=192）上 Qt5 界面
#   - gripper 组滑块不显示 / 界面文字截断（用 QT_AUTO_SCREEN_SCALE_FACTOR=1 修复）
#   - 3D 视图闪烁（用 LIBGL_ALWAYS_SOFTWARE=1 修复；若觉得 3D 偏卡可删掉这一行）
source /opt/ros/humble/setup.bash
source "$(dirname "$(readlink -f "$0")")/install/setup.bash" 2>/dev/null

export QT_AUTO_SCREEN_SCALE_FACTOR=1
export LIBGL_ALWAYS_SOFTWARE=1

exec ros2 launch moveit_setup_assistant setup_assistant.launch.py "$@"
