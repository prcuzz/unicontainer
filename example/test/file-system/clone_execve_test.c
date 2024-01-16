#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/wait.h>
#include<sys/time.h>



void* thread_func(void* arg) {
    printf("Child thread started\n");
    return NULL;
}

int thread_func_1() {
    // char *argv[] = { "/bin/ls", "/", NULL };
    char *argv[] = { "/hello", NULL };
    char *envp[] = { "PATH=/bin", NULL };
    execve(argv[0], argv, envp);
    return 0;
}

int main(int argc, char** argv) {
    __suseconds_t time_use = 0;
    struct timeval start;
    struct timeval end;


    void* stack = malloc(1024*1024); // 为子线程分配堆栈空间
    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    
    printf("Parent thread waiting for child...\n");

    // int flags = CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_THREAD | CLONE_SYSVSEM | CLONE_SETTLS | CLONE_VFORK;
    // int flags = CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SETTLS | CLONE_VFORK | SIGCHLD;
    int flags = CLONE_VM | CLONE_VFORK | SIGCHLD;
    gettimeofday(&start,NULL);
    pid_t pid = clone(thread_func_1, stack + 1024 * 1024, flags, NULL); // 创建子线程
    gettimeofday(&end,NULL);

    if (pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }

    waitpid(pid, NULL, 0);  // 等待子线程结束

    time_use=(end.tv_sec-start.tv_sec)*1000000+(end.tv_usec-start.tv_usec); //微秒
    printf("time_use is %ld ms\n",time_use);

    printf("Child thread finished\n");
    free(stack); // 释放堆栈空间
    return 0;
}
