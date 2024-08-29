#!/bin/bash

# 查找所有名为 qemu 的进程并获取它们的 PID
pids=$(pgrep qemu)

# 检查是否有 qemu 进程
if [ -z "$pids" ]; then
    echo "没有找到任何 qemu 进程。"
else
    # 遍历所有找到的 PID 并杀死对应的进程
    for pid in $pids; do
        echo "正在杀死 qemu 进程: $pid"
        kill $pid
    done
fi
