#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <time.h>

#define SHM_SIZE 1024  // 共享内存大小

int main() {
    key_t key = ftok("/tmp", 'A');  // 创建一个key

    int shmid = shmget(key, SHM_SIZE, IPC_CREAT | 0666);  // 创建共享内存段
    if (shmid == -1) {
        perror("shmget");
        exit(1);
    }

    char *shm_ptr = shmat(shmid, NULL, 0);  // 将共享内存连接到程序地址空间
    if (shm_ptr == (char *)-1) {
        perror("shmat");
        exit(1);
    }

    int i;
    clock_t start_time, end_time;
    double total_time;

    start_time = clock(); // 记录开始时间

    for (i = 0; i < 500; i++) {
        strcpy(shm_ptr, "hello");  // 向共享内存写入消息
        while (*shm_ptr != '*');
    }

    end_time = clock(); // 记录结束时间
    total_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("Total time taken by program A: %f seconds\n", total_time);

    shmdt(shm_ptr);  // 分离共享内存
    shmctl(shmid, IPC_RMID, NULL);  // 删除共享内存段

    return 0;
}
