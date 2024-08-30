#include <stdio.h>
#include <unistd.h>

int main() {
    printf("程序开始休眠...\n");
    sleep(500000);  // 让程序休眠5秒
    printf("休眠结束。\n");
    return 0;
}