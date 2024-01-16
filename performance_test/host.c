#define _GNU_SOURCE
#include <sys/time.h>
#include <time.h>
#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>


int* thread_func(void* arg) {
    char *argv[] = { "/bin/ls", "-l", NULL };
    char *envp[] = { "PATH=/bin", NULL };
    execve("/bin/ls", argv, envp);

    return 0;
}

int main(int argc, char** argv) {
    void* stack = malloc(1024*1024); // 为子线程分配堆栈空间
	struct timespec timestamp;
	
    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    int flags = CLONE_VM | CLONE_VFORK;
	
    clock_gettime(CLOCK_REALTIME, &timestamp);
    unsigned long long time_1 = timestamp.tv_nsec + timestamp.tv_sec * 1000000000;
	
    pid_t pid = clone(thread_func, stack+1024*1024, flags, NULL); // 创建子线程
	if (pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }
	
    clock_gettime(CLOCK_REALTIME, &timestamp);
    unsigned long long time_2 = timestamp.tv_nsec + timestamp.tv_sec * 1000000000;
	
	printf("花费时间：%llu纳秒\n", time_2 - time_1);

    printf("Parent thread waiting for child...\n");
    // sleep(2);
    waitpid(pid, NULL, 0); // 等待子线程结束
    
    printf("Child thread finished\n");
    free(stack); // 释放堆栈空间
    return 0;
}
