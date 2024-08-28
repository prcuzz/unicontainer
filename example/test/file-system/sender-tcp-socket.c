#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Failed to create socket");
        return -1;
    }

    struct sockaddr_in server_address;
    memset(&server_address, '0', sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(9532);
    inet_pton(AF_INET, "172.44.0.1", &server_address.sin_addr);

    if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        perror("Connection failed");
        close(sock);
        return -1;
    }

    const char *msg = "ZZC-hello";
    if (send(sock, msg, strlen(msg), 0) < 0) {
        perror("Send failed");
    } else {
        printf("Message sent successfully\n");
    }

    close(sock);
    return 0;
}
