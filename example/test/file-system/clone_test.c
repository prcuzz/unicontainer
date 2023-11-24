#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void* thread_func(void* arg) {
    printf("Child thread started\n");
    return NULL;
}

int main(int argc, char** argv) {
    void* stack = malloc(1024*1024); // 为子线程分配堆栈空间
    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    
    // int flags = CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | CLONE_SYSVSEM | CLONE_SETTLS;
    int flags = CLONE_VFORK;
    pid_t pid = clone(thread_func, stack+1024*1024, flags, NULL); // 创建子线程
    
    if (pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }
    
    printf("Parent thread waiting for child...\n");
    // sleep(2);
    waitpid(pid, NULL, 0); // 等待子线程结束
    
    printf("Child thread finished\n");
    free(stack); // 释放堆栈空间
    return 0;
}
