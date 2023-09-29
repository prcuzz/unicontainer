def analyze_line(line):
    if "resumed>)" in line:
        return
    else:
        pid = line.split(' ', 1)[0]
        rest_of_the_line = line.split(' ', 1)[1]
        syscall = rest_of_the_line.split('(', 1)[0]
        return pid, syscall


def image_splitting(strace_output):
    file_syscall=["access","open"]

    with open(strace_output, 'r', encoding='utf-8') as f:
        line = f.readline()
        while (line):
            analyze_line(line)
            if(syscall is exec):
                create_a_new_file_group()
            elif(syscall in file_syscall):
                add_this_file_into_corresponding_file_group()
            elif(syscall is clone):

            else:
                pass
            line = f.readline()


if __name__ == '__main__':
    strace_output = "./imagemagick_strace_output"
    image_splitting(strace_output)
