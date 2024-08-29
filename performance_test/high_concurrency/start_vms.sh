#!/bin/bash

# 定义QEMU和其它变量
qemu="qemu-system-x86_64"
cmd="sleep"
my_own_elfloader_kernel_image="$(pwd)/../../../unikraft/elfloader/workdir/build/elfloader_qemu-x86_64"

# 检查是否提供了虚拟机数量参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 <number_of_vms>"
    exit 1
fi

# 获取要启动的虚拟机数量
num_vms=$1

# 启动虚拟机
for ((i=1; i<=num_vms; i++)); do
    # 构建启动命令
    vm_cmd="${qemu} -kernel ${my_own_elfloader_kernel_image} -nographic -m 4G -append \"${cmd}\" -fsdev local,id=myid,path=$(pwd)/../../example/test/file-system,security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max -enable-kvm &> /dev/null &"
    
    # 执行启动命令
    eval "$vm_cmd"
    
    # 输出成功信息
    echo "Virtual machine $i started successfully in the background."
done

# 输出当前内存使用情况
free -h
