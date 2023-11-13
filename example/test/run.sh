run_app_elfloader_kernel_image=$(pwd)/../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64
run_app_elfloader_plain_kernel_image=$(pwd)/../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64_plain
elfloader_kernel_image=$(pwd)/../../../unikraft/elfloader/workdir/build/elfloader_qemu-x86_64
cmd=clone
#cmd=exec_test
#cmd=/bin/ls

#qemu-system-x86_64 -m 2G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=passthrough,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs0 -kernel /home/zzc/Desktop/zzc/my-unikernel/apps/app-elfloader/build/elfloader_qemu-x86_64-default -enable-kvm -cpu host -netdev tap,id=hnet0,vhost=off,script=/home/zzc/Desktop/zzc/my-unikernel/apps/run-app-elfloader/setup/up,downscript=/home/zzc/Desktop/zzc/my-unikernel/apps/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /a"

#qemu-system-x86_64 -m 2G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=passthrough,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs0 -kernel ${app_elfloader_kernel_image} -enable-kvm -cpu host -netdev tap,id=hnet0,vhost=off,script=../../../unikraft/run-app-elfloader/setup/up,downscript=../../../unikraft/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /b"

qemu-system-x86_64 -kernel ${elfloader_kernel_image} -nographic -m 256M -append ${cmd} -fsdev local,id=myid,path=$(pwd)/file-system,security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max -enable-kvm
