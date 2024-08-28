import socket
import threading

def handle_client(client_socket, target_host, target_port):
    # 连接到目标主机
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))
    
    while True:
        # 从客户端接收数据
        client_data = client_socket.recv(4096)
        if not client_data:
            break
        # 将数据转发给目标服务器
        target_socket.send(client_data)
        
        # 从目标服务器接收响应
        target_response = target_socket.recv(4096)
        if not target_response:
            break
        # 将响应转发给客户端
        client_socket.send(target_response)
    
    # 关闭连接
    client_socket.close()
    target_socket.close()

def proxy_server(local_host, local_port, target_host, target_port):
    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    server_socket.bind((local_host, local_port))
    # 开始监听
    server_socket.listen(5)
    
    print(f'[*] Listening on {local_host}:{local_port}')
    
    while True:
        # 接受客户端连接
        client_socket, addr = server_socket.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        
        # 创建线程处理客户端请求
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()

def main():
    # 设置转发参数
    local_host = '127.0.0.1'  # 宿主机地址
    local_port = 6379  # 宿主机端口，可以根据需要更改
    target_host = '192.168.122.2'  # 第一台虚拟机IP
    target_port = 6379  # 第一台虚拟机上的Redis端口
    
    # 启动代理服务器
    proxy_server(local_host, local_port, target_host, target_port)

if __name__ == "__main__":
    main()

