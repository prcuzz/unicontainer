import re
import os
import shutil


def analyze_line(line):
    """
    解析一行 strace 输出，提取进程 ID、系统调用、参数等信息。

    参数:
    line (str): 单行的 strace 输出。

    返回:
    tuple: 包含以下信息的元组:
        - pid (str): 进程 ID。
        - syscall (str): 系统调用名称。
        - first_arg (str): 系统调用的第一个参数。
        - second_arg (str): 系统调用的第二个参数。
        - clone_result (bool): 是否是 clone 系统调用的结果。
        - child_pid (str): 子进程的进程 ID（仅当 clone_result 为 True 时返回）。
    """
    pid = None
    syscall = None
    first_arg = None
    second_arg = None
    clone_result = False
    child_pid = None

    if "clone resumed" in line:
        # 当 clone 调用完成时，获取父进程 ID 和子进程 ID
        pid = line.split(' ', 1)[0]
        clone_result = True
        child_pid = line.split(' ')[-1].strip('\n')
    elif "resumed" in line:
        # 忽略其他 resumed 行，只提取进程 ID
        pid = line.split(' ', 1)[0]
    elif re.match(r"(\d)+(\s)+[a-z_]+\(", line):
        # 匹配系统调用行并提取系统调用名称和参数
        pid = line.split()[0]
        rest_of_the_line = line.split()[1]
        syscall = rest_of_the_line.split('(', 1)[0]
        rest_of_the_line = line.split('(', 1)[1]

        # 处理系统调用的参数
        if len(rest_of_the_line.split(',')) == 1:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = None
        elif len(rest_of_the_line.split(',')) == 2:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = rest_of_the_line.split(',', 1)[1].split(')', 1)[0].strip()
        elif len(rest_of_the_line.split(',')) >= 3:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = rest_of_the_line.split(',', 2)[1].split(')', 1)[0].strip()

        # TODO: 添加对包含 "{" 的行的分析逻辑，例如 "7226  rt_sigreturn({mask=[]} <unfinished ...>"

    return pid, syscall, first_arg, second_arg, clone_result, child_pid


def analyze_strace_output(strace_output):
    """
    分析整个 strace 输出文件，提取文件操作和进程信息。

    参数:
    strace_output (str): strace 输出文件的路径。

    返回:
    list: 包含文件路径的列表，按进程组分类。
    """
    file_syscall = ["access", "open", "openat"]  # 文件操作相关的系统调用
    exec_syscall = ["execl", "execlp", "execle", "execv", "execvp", "execve"]  # 执行程序相关的系统调用
    file_group = []  # 用于存储每个进程组的文件列表
    pid_group = []  # 用于存储进程 ID 分组

    with open(strace_output, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            # 分析每一行的系统调用信息
            pid, syscall, first_arg, second_arg, clone_result, child_pid = analyze_line(line)

            if syscall and syscall in exec_syscall:
                # 如果是执行程序的系统调用，处理对应的文件和进程组
                for i in range(len(pid_group)):
                    if pid in pid_group[i]:
                        pid_group[i].remove(pid)
                        break
                file_group.append([])
                cnt = len(file_group)
                file_group[cnt - 1].append(first_arg)
                pid_group.append([])
                cnt = len(pid_group)
                pid_group[cnt - 1].append(pid)

            elif syscall and syscall in file_syscall:
                # 如果是文件操作的系统调用，将文件路径加入对应的文件组
                for i in range(len(pid_group)):
                    if pid in pid_group[i]:
                        if syscall == "openat":
                            if second_arg not in file_group[i]:
                                file_group[i].append(second_arg)
                        else:
                            if first_arg not in file_group[i]:
                                file_group[i].append(first_arg)

            elif clone_result:
                # 处理 clone 系统调用结果，将子进程 ID 添加到对应的进程组中
                if_this_child_is_leader = False
                for i in range(len(pid_group)):
                    if child_pid == pid_group[i][0]:
                        if_this_child_is_leader = True
                        break
                if not if_this_child_is_leader:
                    for i in range(len(pid_group)):
                        if pid in pid_group[i]:
                            pid_group[i].append(child_pid)
                            break
            else:
                pass

            line = f.readline()

    # 输出 pid_group 和 file_group，用于调试
    print(pid_group)
    print(file_group)

    return file_group


def copy_files(src_dir, dst_dir, file_group):
    """
    将文件从源目录复制到目标目录。此函数会处理符号链接，并递归复制链接指向的文件。

    参数:
    src_dir (str): 源目录的路径。
    dst_dir (str): 目标目录的路径。
    file_group (list): 需要复制的文件路径列表，相对于源目录。

    """
    for file_path in file_group:
        # 获取源文件和目标文件的完整路径
        src_path = os.path.join(src_dir, file_path)
        dst_path = os.path.join(dst_dir, file_path)

        if os.path.islink(src_path):  # 如果源文件是符号链接
            link_target = os.readlink(src_path)  # 获取符号链接指向的目标

            # 处理绝对路径的符号链接
            if link_target.startswith('/'):
                # 对于绝对路径的符号链接，去掉第一个'/'
                link_target = link_target[1:]
            else:
                # 对于相对路径的符号链接，转换为相对于源目录的路径
                link_target = os.path.join(os.path.dirname(file_path), link_target)

            # 将链接目标添加到 file_group 中，递归处理链接指向的文件
            file_group.append(link_target)

            # 如果目标路径不存在，创建必要的目录结构
            if not os.path.lexists(dst_path):
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                # 复制符号链接，而不是其内容
                # shutil.copy(src_path, dst_path, follow_symlinks=False)
                try:
                    # 尝试使用 shutil.copy() 复制符号链接
                    shutil.copy(src_path, dst_path, follow_symlinks=False)
                except shutil.SpecialFileError:
                    # 如果复制失败，因为目标是特殊文件，则手动创建符号链接
                    # 此处是为了处理链接目标是/dev/stderr（或类似文件）的特殊情况
                    os.symlink('/'+link_target, dst_path)

        elif os.path.isfile(src_path):  # 如果源文件是常规文件
            # 如果目标路径不存在，创建必要的目录结构
            if not os.path.lexists(dst_path):
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                # 复制文件
                shutil.copy(src_path, dst_path, follow_symlinks=False)


def copy_directory_structure(src_dir, dst_dir):
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # 遍历源目录中的所有条目
    for entry in os.scandir(src_dir):
        # 如果是目录，则递归调用自身来复制该目录及其子目录
        if entry.is_dir():
            new_dst_dir = os.path.join(dst_dir, entry.name)
            copy_directory_structure(entry.path, new_dst_dir)
        # 如果是文件，则忽略
        elif entry.is_file():
            continue


if __name__ == '__main__':
    # 定义 strace 输出文件路径
    strace_output = "../strace_output/nginx_strace_output"

    # 解析 strace 输出文件，获取文件组
    file_group = analyze_strace_output(strace_output)

    # 处理文件组，去掉不必要的字符和根路径
    file_group_1 = []
    for file_list in file_group:
        for file in file_list:
            file = file.strip('"')  # 去掉文件路径中的引号
            if file == "/":
                pass
            elif file[0] == "/":
                file = file[1:]  # 去掉路径开头的 '/'
            file_group_1.append(file)

    # 定义源目录和目标目录路径
    src_dir = "/home/zzc/Desktop/zzc/unicontainer/example/nginx-1.13.1-alpine/file-system"
    dst_dir = "/home/zzc/Desktop/zzc/unicontainer/example/nginx-1.13.1-alpine/image-splitting-test"

    # 复制整个目录结构
    copy_directory_structure(src_dir, dst_dir)

    # 复制文件组中的文件到目标目录
    copy_files(src_dir, dst_dir, file_group_1)
