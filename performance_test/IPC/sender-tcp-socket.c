#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>

#define PORT 8080
#define MESSAGE "hello"
#define NUM_MESSAGES 1

int main() {
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char sendBuff[1024] = {0};

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, "172.44.0.2", &serv_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        exit(EXIT_FAILURE);
    }

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
