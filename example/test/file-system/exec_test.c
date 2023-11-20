#include <unistd.h>

int main() {
    char *argv[] = { "/bin/ls", "-l", NULL };
    char *envp[] = { "PATH=/bin", NULL };
    execve("/bin/ls", argv, envp);
    return 0;
}

