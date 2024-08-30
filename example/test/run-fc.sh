#!/bin/sh

config="vmconfig.json"

if test $# -eq 1; then
    config="$1"
fi

rootfs="./file-system"
test -d "$rootfs" || mkdir "$rootfs"

# Clean up any previous instances.
sudo pkill -f qemu-system
sudo pkill -f firecracker
sudo kraft stop --all
sudo kraft rm --all

# Create CPIO archive to be used as the initrd.
old="$PWD"
cd "$rootfs"
find -depth -print | tac | bsdcpio -o --format newc > "$old"/rootfs.cpio
cd "$old"

cat <<EOF > "$config"
{
  "boot-source": {
    "kernel_image_path": "../../../unikraft/elfloader/workdir/build/elfloader_fc-x86_64",
    "boot_args": "elfloader_fc-x86_64 /hello",
    "initrd_path": "rootfs.cpio"
  },
  "drives": [],
  "machine-config": {
    "vcpu_count": 1,
    "mem_size_mib": 1024,
    "smt": false,
    "track_dirty_pages": false
  },
  "cpu-config": null,
  "balloon": null,
  "vsock": null,
  "logger": {
    "log_path": "/tmp/firecracker.log",
    "level": "Debug",
    "show_level": true,
    "show_log_origin": true
  },
  "metrics": null,
  "mmds-config": null,
  "entropy": null
}
EOF

# Remove previously created files.
sudo rm -f /tmp/firecracker.log
> /tmp/firecracker.log
sudo rm -f /tmp/firecracker.socket
firecracker-x86_64 \
        --api-sock /tmp/firecracker.socket \
        --config-file "$config"
