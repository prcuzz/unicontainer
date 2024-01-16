#!/bin/sh

elfloader_kernel_image_in_run_app_elfloader=$(pwd)/../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64
elfloader_strace_kernel_image_in_run_app_elfloader=$(pwd)/../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64_strace
my_own_elfloader_kernel_image=$(pwd)/../../../unikraft/elfloader/workdir/build/elfloader_qemu-x86_64
qemu=/home/zzc/Desktop/ZZC/qemu-6.2.0/build/qemu-system-x86_64

cmd=clone_execve_test
# cmd=exec_test
# cmd=/bin/ls
# cmd="php shell_exec-test.php"

# qemu-system-x86_64 -m 2G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=passthrough,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs0 -kernel /home/zzc/Desktop/zzc/my-unikernel/apps/app-elfloader/build/elfloader_qemu-x86_64-default -enable-kvm -cpu host -netdev tap,id=hnet0,vhost=off,script=/home/zzc/Desktop/zzc/my-unikernel/apps/run-app-elfloader/setup/up,downscript=/home/zzc/Desktop/zzc/my-unikernel/apps/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /a"

# qemu-system-x86_64 -m 2G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=passthrough,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs0 -kernel ${app_elfloader_kernel_image} -enable-kvm -cpu host -netdev tap,id=hnet0,vhost=off,script=../../../unikraft/run-app-elfloader/setup/up,downscript=../../../unikraft/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /b"

# for test
${qemu} -kernel ${my_own_elfloader_kernel_image} -nographic -m 4G -append "${cmd}" -fsdev local,id=myid,path=$(pwd)/file-system,security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max -enable-kvm

# /php -t ./ -S 0.0.0.0:8080, for debug
# qemu-system-x86_64 -m 4G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=none,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs1 -kernel ${my_own_elfloader_kernel_image} -cpu max -netdev tap,id=hnet0,vhost=off,script=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/up,downscript=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -s -S -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /php -t ./ -S 0.0.0.0:8080"

# /php -t ./ -S 0.0.0.0:8080
# qemu-system-x86_64 -m 4G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=none,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs1 -kernel ${my_own_elfloader_kernel_image} -cpu max -netdev tap,id=hnet0,vhost=off,script=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/up,downscript=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /php -t ./ -S 0.0.0.0:8080"
