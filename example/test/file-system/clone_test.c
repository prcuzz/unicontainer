#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>  
#include <sys/wait.h>
#include <string.h>

#define STACK_SIZE 1024

int thread_func(void* arg) {
    // printf("Executing child process\n");
    // write(1, "Executing child process\n", 25);

    // char *argv[] = { "/bin/ls", NULL };
    // char *envp[] = { "PATH=/bin", NULL };
    // execve("/bin/ls", argv, envp);

    char *message = "Executing child process\n";
    size_t length = strlen(message);
    
    // 使用内联汇编调用系统调用write
    asm volatile (
        "movq $1, %%rax \n"    // 系统调用号为1（write）
        "movq $1, %%rdi \n"    // 文件描述符为1（标准输出）
        "movq %0, %%rsi \n"    // 消息地址作为参数
        "movq %1, %%rdx \n"    // 消息长度作为参数
        "syscall \n"
        :
        : "r" (message), "r" (length)
        : "%rax", "%rdi", "%rsi", "%rdx"
    );



    asm("mov $60, %rax\n\t"  // \n\t表示换行和制表符
    "mov $0, %rdi\n\t"
    "syscall");

    _exit(0);
}

int main(int argc, char** argv) {
    void* stack = malloc(STACK_SIZE*STACK_SIZE); // 为子线程分配堆栈空间

    printf("Parent process waiting for child...\n");

    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    // int flags = CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | CLONE_SYSVSEM | CLONE_SETTLS | CLONE_VFORK;
    // int flags = CLONE_VM | CLONE_FILES | CLONE_FS | CLONE_VFORK;
    int flags = CLONE_VM | CLONE_VFORK | CLONE_FILES | CLONE_FS | CLONE_SETTLS;
    pid_t pid = clone(thread_func, stack+STACK_SIZE*STACK_SIZE, flags, NULL); // 创建子线程

    if (pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }
    
    // sleep(2);
    // waitpid(pid, NULL, 0); // 等待子线程结束
    
    printf("Child thread finished\n");
    free(stack); // 释放堆栈空间
    return 0;
}
