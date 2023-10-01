import re


def analyze_line(line):
    if "clone resumed" in line:
        # return clone result
        pid = line.split(' ', 1)[0]
        clone_result = True
        child_pid = line.split(' ')[-1].strip('\n')
        return pid, "clone", None, clone_result, child_pid
    elif "resumed" in line:
        # skip other result analysis
        pid = line.split(' ', 1)[0]
        return pid, None, None, False, None
    elif re.match(r"(\d)+(\s)+[a-z_]+\(", line):
        pid = line.split()[0]
        rest_of_the_line = line.split()[1]
        syscall = rest_of_the_line.split('(', 1)[0]
        rest_of_the_line = line.split('(', 1)[1]
        first_arg = rest_of_the_line.split(',', 1)[0]
        # ToDo: add analysis logic for line with "{" like "7226  rt_sigreturn({mask=[]} <unfinished ...>"
        return pid, syscall, first_arg, False, None
    else:
        return None, None, None, False, None


def image_splitting(strace_output):
    file_syscall = ["access", "open"]
    exec_syscall = ["execl", "execlp", "execle", "execv", "execvp", "execve"]
    file_group = []
    pid_group = []

    with open(strace_output, 'r', encoding='utf-8') as f:  # open strace output file
        line = f.readline()
        while (line):
            pid, syscall, first_arg, clone_result, child_pid = analyze_line(line)
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


if __name__ == '__main__':
    strace_output = "./imagemagick_strace_output"
    image_splitting(strace_output)
