#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <time.h>

#define SOCKET_PATH "/tmp/test_socket"
#define MESSAGE "hello"
#define NUM_MESSAGES 50

int main() {
    int sock = 0, valread;
    struct sockaddr_un serv_addr;
    char sendBuff[1024] = {0};

    if ((sock = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sun_family = AF_UNIX;
    strncpy(serv_addr.sun_path, SOCKET_PATH, sizeof(serv_addr.sun_path) - 1);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Failed to connect to server");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < NUM_MESSAGES; i++) {
        strcpy(sendBuff, MESSAGE);
        send(sock, sendBuff, strlen(sendBuff), 0);
    }

    close(sock);
    printf("Sender: All messages sent.\n");
    return 0;
}
