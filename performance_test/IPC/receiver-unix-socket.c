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
    int server_sock, client_sock, valread;
    struct sockaddr_un address;
    int received_messages = 0;
    struct timespec start, end;
    char buffer[1024]; // Declare the buffer variable

    // Create socket
    if ((server_sock = socket(AF_UNIX, SOCK_STREAM, 0)) == 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    unlink(SOCKET_PATH); // Remove existing socket file, if any

    address.sun_family = AF_UNIX;
    strncpy(address.sun_path, SOCKET_PATH, sizeof(address.sun_path) - 1);

    if (bind(server_sock, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Failed to bind socket");
        exit(EXIT_FAILURE);
    }

    if (listen(server_sock, 5) < 0) {
        perror("Failed to listen on socket");
        exit(EXIT_FAILURE);
    }

    printf("Receiver: Waiting for connection...\n");

    // Accept incoming connection from sender
    if ((client_sock = accept(server_sock, NULL, NULL)) < 0) {
        perror("Failed to accept connection");
        exit(EXIT_FAILURE);
    }

    clock_gettime(CLOCK_MONOTONIC, &start);

    while (received_messages < NUM_MESSAGES) {
        valread = read(client_sock, buffer, 1024);
        if (valread == 0) {
            break;
        }
        if (strcmp(buffer, MESSAGE) == 0) {
            received_messages++;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double elapsed_time = (double)(end.tv_sec - start.tv_sec) + (double)(end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Receiver: All %d messages received in %.6f seconds.\n", NUM_MESSAGES, elapsed_time);

    close(client_sock);
    close(server_sock);

    return 0;
}
