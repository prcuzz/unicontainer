#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void* thread_func(void* arg) {
    printf("Executing child process\n");
    return NULL;
}

int main(int argc, char** argv) {
    void* stack = malloc(1024*1024); // 为子线程分配堆栈空间

    printf("Parent process waiting for child...\n");

    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    // int flags = CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | CLONE_SYSVSEM | CLONE_SETTLS;
    int flags = CLONE_VM | CLONE_VFORK | CLONE_FILES | CLONE_FS;
    // int flags = CLONE_VM | CLONE_FILES | CLONE_FS;
    pid_t pid = clone(thread_func, stack+1024*1024, flags, NULL); // 创建子线程

    if (pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }
    
    // sleep(1);
    // waitpid(pid, NULL, 0); // 等待子线程结束
    
    printf("Child thread finished\n");
    free(stack); // 释放堆栈空间
    return 0;
}
