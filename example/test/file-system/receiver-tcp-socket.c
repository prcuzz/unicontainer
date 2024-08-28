#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define MAX_BUFFER_SIZE 1024

int main() {
    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        perror("Failed to create socket");
        return -1;
    }

    struct sockaddr_in server_address;
    memset(&server_address, '0', sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(9532);
    inet_pton(AF_INET, "127.0.0.1", &server_address.sin_addr);

    if (bind(server_sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        perror("Bind failed");
        close(server_sock);
        return -1;
    }

    if (listen(server_sock, 5) < 0) {
        perror("Listen failed");
        close(server_sock);
        return -1;
    }

    printf("Server is listening on port 9532...\n");

    struct sockaddr_in client_address;
    socklen_t client_len = sizeof(client_address);
    int client_sock = accept(server_sock, (struct sockaddr*)&client_address, &client_len);
    if (client_sock < 0) {
        perror("Accept failed");
        close(server_sock);
        return -1;
    }

    char buffer[MAX_BUFFER_SIZE] = {0};
    int received = recv(client_sock, buffer, MAX_BUFFER_SIZE - 1, 0);
    if (received < 0) {
        perror("Receive failed");
    } else {
        printf("Received message: %s\n", buffer);
    }

    close(client_sock);
    close(server_sock);
    return 0;
}
