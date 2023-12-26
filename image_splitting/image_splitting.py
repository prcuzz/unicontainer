import re
import os
import shutil


def analyze_line(line):
    pid = None
    syscall = None
    first_arg = None
    second_arg = None
    clone_result = False
    child_pid = None

    if "clone resumed" in line:
        # return clone result
        pid = line.split(' ', 1)[0]
        clone_result = True
        child_pid = line.split(' ')[-1].strip('\n')
    elif "resumed" in line:
        # skip other result analysis
        pid = line.split(' ', 1)[0]
    elif re.match(r"(\d)+(\s)+[a-z_]+\(", line):
        pid = line.split()[0]
        rest_of_the_line = line.split()[1]
        syscall = rest_of_the_line.split('(', 1)[0]
        rest_of_the_line = line.split('(', 1)[1]
        if len(rest_of_the_line.split(',')) == 1:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = None
        elif len(rest_of_the_line.split(',')) == 2:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = rest_of_the_line.split(',', 1)[1].split(')', 1)[0].strip()
        elif len(rest_of_the_line.split(',')) >= 3:
            first_arg = rest_of_the_line.split(',', 1)[0].split(')', 1)[0]
            second_arg = rest_of_the_line.split(',', 2)[1].split(')', 1)[0].strip()
        # ToDo: add analysis logic for line with "{" like "7226  rt_sigreturn({mask=[]} <unfinished ...>"

    return pid, syscall, first_arg, second_arg, clone_result, child_pid


def analyze_strace_output(strace_output):
    file_syscall = ["access", "open", "openat"]
    exec_syscall = ["execl", "execlp", "execle", "execv", "execvp", "execve"]
    file_group = []
    pid_group = []

    with (open(strace_output, 'r', encoding='utf-8') as f):  # open strace output file
        line = f.readline()
        while (line):
            pid, syscall, first_arg, second_arg, clone_result, child_pid = analyze_line(line)
            if (syscall and syscall in exec_syscall):
                # remove pid from its parent pid group
                for i in range(len(pid_group)):
                    if pid in pid_group[i]:
                        pid_group[i].remove(pid)
                        break
                # create a new file group and a new pid group
                file_group.append([])
                cnt = len(file_group)
                file_group[cnt - 1].append(first_arg)
                pid_group.append([])
                cnt = len(pid_group)
                pid_group[cnt - 1].append(pid)
            elif (syscall and syscall in file_syscall):
                # add this file into corresponding file group
                for i in range(len(pid_group)):
                    if pid in pid_group[i]:
                        if syscall == "openat":
                            if second_arg not in file_group[i]:
                                file_group[i].append(second_arg)
                        else:
                            if first_arg not in file_group[i]:
                                file_group[i].append(first_arg)
            elif (clone_result == True):
                if_this_child_is_leader = False
                # check if this child is leader
                for i in range(len(pid_group)):
                    if child_pid == pid_group[i][0]:
                        if_this_child_is_leader = True
                        break
                # add this pid into corresponding pid group
                if if_this_child_is_leader is False:
                    for i in range(len(pid_group)):
                        if pid in pid_group[i]:
                            pid_group[i].append(child_pid)
                            break
            else:
                pass
            line = f.readline()

    # print file_group and pid_group
    print(pid_group)
    print(file_group)

    return file_group


def copy_files(src_dir, dst_dir, file_group):
    for file_path in file_group:
        src_path = os.path.join(src_dir, file_path)
        dst_path = os.path.join(dst_dir, file_path)

        if os.path.islink(src_path):
            link_target = os.readlink(src_path)
            if link_target.startswith('/'):
                link_target = link_target[1:]
            else:
                link_target = os.path.join(os.path.dirname(file_path), link_target)
            file_group.append(link_target)
            if os.path.lexists(dst_path) == False:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(src_path, dst_path, follow_symlinks=False)
        elif os.path.isfile(src_path):
            if os.path.lexists(dst_path) == False:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(src_path, dst_path, follow_symlinks=False)


if __name__ == '__main__':
    strace_output = "../strace_output/imagemagick_strace_output"
    file_group = analyze_strace_output(strace_output)
    file_group_1 = []
    for file_list in file_group:
        for file in file_list:
            file = file.strip('"')
            if file[0] == "/":
                file = file[1:]
            file_group_1.append(file)
    src_dir = "/home/zzc/Desktop/zzc/unicontainer/example/imagemagick/imagemagick"
    dst_dir = "/home/zzc/Desktop/zzc/unicontainer/example/imagemagick/file-system"
    copy_files(src_dir, dst_dir, file_group_1)
