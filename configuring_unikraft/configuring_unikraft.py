import re
import os
import glob
import shutil


def modify_syscall_lib_config(lib_list):
    environ_config = \
        """CONFIG_LIBPOSIX_ENVIRON=y

#
# Compiled-in environment variables
#
CONFIG_LIBPOSIX_ENVIRON_ENVP0="PATH=/bin"
CONFIG_LIBPOSIX_ENVIRON_ENVP0_NOTEMPTY=y
CONFIG_LIBPOSIX_ENVIRON_ENVP1=""
CONFIG_LIBPOSIX_ENVIRON_ENVP2=""
CONFIG_LIBPOSIX_ENVIRON_ENVP3=""
CONFIG_LIBPOSIX_ENVIRON_ENVP4=""
CONFIG_LIBPOSIX_ENVIRON_ENVP5=""
CONFIG_LIBPOSIX_ENVIRON_ENVP6=""
CONFIG_LIBPOSIX_ENVIRON_ENVP7=""
CONFIG_LIBPOSIX_ENVIRON_ENVP8=""
CONFIG_LIBPOSIX_ENVIRON_ENVP9=""
CONFIG_LIBPOSIX_ENVIRON_ENVP10=""
CONFIG_LIBPOSIX_ENVIRON_ENVP11=""
CONFIG_LIBPOSIX_ENVIRON_ENVP12=""
CONFIG_LIBPOSIX_ENVIRON_ENVP13=""
CONFIG_LIBPOSIX_ENVIRON_ENVP14=""
CONFIG_LIBPOSIX_ENVIRON_ENVP15=""
# end of Compiled-in environment variables
"""

    event_config = \
        """CONFIG_LIBPOSIX_EVENT=y
# CONFIG_LIBPOSIX_EVENT_DEBUG is not set
"""

    futex_config = \
        """CONFIG_LIBPOSIX_FUTEX=y
# CONFIG_LIBPOSIX_FUTEX_DEBUG is not set
# CONFIG_LIBPOSIX_FUTEX_TEST is not set
"""

    socket_config = \
        """CONFIG_HAVE_NW_STACK=y
CONFIG_LIBVIRTIO_NET=y
CONFIG_LIBPOSIX_SOCKET=y
# CONFIG_LIBPOSIX_SOCKET_PRINT_ERRORS is not set
"""

    user_config = \
        """CONFIG_LIBPOSIX_USER=y
CONFIG_LIBPOSIX_USER_UID=0
CONFIG_LIBPOSIX_USER_GID=0
CONFIG_LIBPOSIX_USER_USERNAME="root"
CONFIG_LIBPOSIX_USER_GROUPNAME="root"
"""

    signal_config = \
        """CONFIG_LIBUKSIGNAL=y
"""

    libparam_config = \
        """CONFIG_LIBUKLIBPARAM=y
"""

    netdev_config = \
        """CONFIG_LIBUKNETDEV=y
CONFIG_LIBUKNETDEV_MAXNBQUEUES=1
CONFIG_LIBUKNETDEV_DISPATCHERTHREADS=y
# CONFIG_LIBUKNETDEV_STATS is not set
"""

    mpi_config = \
    """CONFIG_LIBUKMPI=y
CONFIG_LIBUKMPI_MBOX=y
"""

    lwip_config = \
        """CONFIG_LIBLWIP=y
# CONFIG_LWIP_RELEASE212 is not set
# CONFIG_LWIP_LATEST21X is not set
CONFIG_LWIP_UNIKRAFT21X=y
    
#
# Netif drivers
#
# CONFIG_LWIP_LOOPIF is not set
CONFIG_LWIP_UKNETDEV=y
# CONFIG_LWIP_UKNETDEV_POLLONLY is not set
CONFIG_LWIP_UKNETDEV_SCRATCH=64
# end of Netif drivers
    
CONFIG_LWIP_AUTOIFACE=y
# CONFIG_LWIP_NOTHREADS is not set
CONFIG_LWIP_THREADS=y
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_32 is not set
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_64 is not set
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_128 is not set
CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_256=y
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_512 is not set
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_1024 is not set
# CONFIG_LWIP_STACKTHREAD_MBOX_SIZE_2048 is not set
CONFIG_LWIP_STACKTHREAD_MBOX_SIZE=256
CONFIG_LWIP_HEAP=y
# CONFIG_LWIP_POOLS is not set
CONFIG_LWIP_NETIF_EXT_STATUS_CALLBACK=y
CONFIG_LWIP_NETIF_STATUS_PRINT=y
CONFIG_LWIP_LOOPBACK=y
CONFIG_LWIP_IPV4=y
# CONFIG_LWIP_IPV6 is not set
    
#
# IP Configuration
#
CONFIG_LWIP_IP_REASS_MAX_PBUFS=10
# end of IP Configuration
    
CONFIG_LWIP_UDP=y
CONFIG_LWIP_TCP=y
CONFIG_LWIP_TCP_MSS=1460
CONFIG_LWIP_WND_SCALE=y
# CONFIG_LWIP_TCP_KEEPALIVE is not set
# CONFIG_LWIP_TCP_TIMESTAMPS is not set
CONFIG_LWIP_NUM_TCPCON=64
CONFIG_LWIP_NUM_TCPLISTENERS=64
CONFIG_LWIP_ICMP=y
# CONFIG_LWIP_IGMP is not set
# CONFIG_LWIP_SNMP is not set
# CONFIG_LWIP_DHCP is not set
CONFIG_LWIP_DNS=y
CONFIG_LWIP_DNS_MAX_SERVERS=2
CONFIG_LWIP_DNS_TABLE_SIZE=32
CONFIG_LWIP_SOCKET=y
CONFIG_LWIP_UDP_RECVMBOX_FACTOR=2
CONFIG_LWIP_TCP_RECVMBOX_FACTOR=2
# CONFIG_LWIP_DEBUG is not set
"""

    # 复制文件.config.helloworld为.config
    shutil.copyfile('.config.helloworld', '.config')

    # 读取.config文件并替换特定行内容
    file_path = '.config'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith('# CONFIG_LIBPOSIX_ENVIRON') and "posix-environ" in lib_list:
                file.write(environ_config)
            elif line.startswith('# CONFIG_LIBPOSIX_EVENT') and "posix-event" in lib_list:
                file.write(event_config)
            elif line.startswith('# CONFIG_LIBPOSIX_FUTEX') and "posix-futex" in lib_list:
                file.write(futex_config)
            elif line.startswith('# CONFIG_LIBPOSIX_SOCKET') and "posix-socket" in lib_list:
                file.write(socket_config)
            elif line.startswith('# CONFIG_LIBLWIP') and "posix-socket" in lib_list:
                file.write(lwip_config)
            elif line.startswith('# CONFIG_LIBUKMPI') and "posix-socket" in lib_list:
                file.write(mpi_config)
            elif line.startswith('# CONFIG_LIBUKNETDEV') and "posix-socket" in lib_list:
                file.write(netdev_config)
            elif line.startswith('# CONFIG_LIBUKLIBPARAM') and "posix-socket" in lib_list:
                file.write(libparam_config)
            elif line.startswith('# CONFIG_LIBPOSIX_USER') and "posix-user" in lib_list:
                file.write(user_config)
            elif line.startswith('# CONFIG_LIBUKSIGNAL') and "uksignal" in lib_list:
                file.write(signal_config)
            else:
                file.write(line)

    print("配置文件生成完毕")

def modify_selectable_basic_lib_config():
    devfs_config = \
    """CONFIG_LIBDEVFS=y
# CONFIG_LIBDEVFS_AUTOMOUNT is not set
# CONFIG_LIBDEVFS_DEV_NULL is not set
# CONFIG_LIBDEVFS_DEV_ZERO is not set
# CONFIG_LIBDEVFS_DEV_STDOUT is not set
"""

    shutil.copyfile('.config', '.config_0')

    # 读取.config文件并替换特定行内容
    file_path = '.config_0'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if "CONFIG_LIBDEVFS is not set" in line:
                file.write(devfs_config)
            else:
                file.write(line)

# 输入 strace 的一行结果，输出对应的 syscall
def analyze_line(line):
    syscall = None

    if re.match(r"(\d)+(\s)+[a-z_]+\(", line):
        rest_of_the_line = line.split()[1]
        syscall = rest_of_the_line.split('(', 1)[0]

    return syscall


def read_exportsyms_file(folder_path):
    file_path = os.path.join(folder_path, 'exportsyms.uk')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    else:
        return []


def analyze_lib(lib_path):
    folders_dict = {}
    for folder_name in os.listdir(lib_path):
        folder_path = os.path.join(lib_path, folder_name)
        if os.path.isdir(folder_path):
            folders_dict[folder_name] = read_exportsyms_file(folder_path)
    return folders_dict


def configuring_unikraft(strace_output_file, unikraft_path):
    syscall_list = []
    with open(strace_output_file, 'r', encoding='utf-8') as f:  # 打开 strace 输出文件
        line = f.readline()
        while (line):
            syscall = analyze_line(line)
            if "access" in line and ":memory:" in line:
                syscall = "futex"              # 处理 access(":memory:", F_OK) 的情况
            if (syscall not in syscall_list) and (syscall is not None):
                syscall_list.append(syscall)  # 把用到的 syscall 都放进 syscall_list
            line = f.readline()

    lib_path = unikraft_path + "/lib"
    lib_syscall_dict = analyze_lib(lib_path)

    lib_list = []
    for syscall in syscall_list:
        for lib, content in lib_syscall_dict.items():
            if syscall in content:
                if lib not in lib_list:
                    lib_list.append(lib)
                break
    if "futex" in syscall_list:
        lib_list.append("posix-futex")

    print("需要添加的库有：", lib_list)

    modify_syscall_lib_config(lib_list)


if __name__ == '__main__':
    strace_output_file = "/home/zzc/Desktop/zzc/unicontainer/strace_output/imagemagick_strace_output"
    unikraft_path = "../../unikraft/elfloader/workdir/unikraft"
    configuring_unikraft(strace_output_file, unikraft_path)
