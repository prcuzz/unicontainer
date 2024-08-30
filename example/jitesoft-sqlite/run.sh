#!/bin/sh

run_app_elfloader=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/app-elfloader_qemu-x86_64
my_own_elfloader=/home/zzc/Desktop/zzc/unikraft/elfloader/workdir/build/elfloader_qemu-x86_64

# qemu-system-x86_64 -m 2G -nographic -nodefaults -display none -serial stdio -device isa-debug-exit -fsdev local,security_model=none,id=hvirtio0,path=$(pwd)/file-system/ -device virtio-9p-pci,fsdev=hvirtio0,mount_tag=fs1 -kernel ${my_own_elfloader} -cpu max -netdev tap,id=hnet0,vhost=off,script=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/up,downscript=/home/zzc/Desktop/zzc/unikraft/run-app-elfloader/setup/down -device virtio-net-pci,netdev=hnet0,id=net0 -append "netdev.ipv4_addr=172.44.0.2 netdev.ipv4_gw_addr=172.44.0.1 netdev.ipv4_subnet_mask=255.255.255.0 --  /usr/bin/sqlite3"

qemu-system-x86_64 -kernel ${my_own_elfloader} -nographic -m 256M -append "/usr/bin/sqlite3" -fsdev local,id=myid,path=$(pwd)/file-system,security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max -enable-kvm