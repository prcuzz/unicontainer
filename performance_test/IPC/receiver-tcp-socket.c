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
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    int received_messages = 0;
    struct timespec start, end;

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    // Set socket options
    //if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
    //    perror("Failed to set socket options");
    //    exit(EXIT_FAILURE);
    //}

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Failed to bind socket");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("Failed to listen on socket");
        exit(EXIT_FAILURE);
    }

    printf("Receiver: Waiting for connection...\n");

    // Accept incoming connection from sender
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("Failed to accept connection");
        exit(EXIT_FAILURE);
    }

    clock_gettime(CLOCK_MONOTONIC, &start);

    while (received_messages < NUM_MESSAGES) {
        valread = read(new_socket, buffer, 1024);
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

    close(new_socket);
    close(server_fd);

    return 0;
}
