run_app_elfloader_kernel_image=../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64
run_app_elfloader_plain_kernel_image=../../../unikraft/run-app-elfloader/app-elfloader_qemu-x86_64_plain
app_elfloader_kernel_image=../../../unikraft/elfloader/workdir/build/elfloader_qemu-x86_64
cmd="identify 1.jpg"
rootfs=$(pwd)/file-system/
#rootfs=/

#qemu-system-x86_64 -kernel ${app_elfloader_kernel_image} -nographic -m 64M -append "/identify 1.jpg" -fsdev local,id=myid,path=${rootfs},security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max --enable-kvm

qemu-system-x86_64 -kernel ${app_elfloader_kernel_image} -nographic -m 64M -append "/identify -format '%w x %h' 1.jpg" -fsdev local,id=myid,path=${rootfs},security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=fs1,disable-modern=on,disable-legacy=off -cpu max --enable-kvm
