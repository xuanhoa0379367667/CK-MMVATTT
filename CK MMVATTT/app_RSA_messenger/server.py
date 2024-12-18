import socket
import threading

# Lưu thông tin khóa công khai và tin nhắn
users = {}  # {username: public_key}
messages = {}  # {username: [(sender, ciphertext), ...]}


def handle_client(client_socket, address):
    print(f"[Server] Kết nối mới từ {address}")
    while True:
        try:
            request = client_socket.recv(4096).decode()
            if not request:
                break

            # Xử lý các loại yêu cầu từ client
            if request.startswith("REGISTER"):
                _, username, public_key = request.split("|", 2)
                users[username] = eval(public_key)  # Lưu khóa công khai
                if username not in messages:
                    messages[username] = []  # Khởi tạo danh sách tin nhắn
                client_socket.send(f"[Server] Khóa công khai đã được lưu.".encode())

            elif request.startswith("GET_KEY"):
                _, recipient_username = request.split("|")
                if recipient_username in users:
                    client_socket.send(str(users[recipient_username]).encode())
                else:
                    client_socket.send("[Server] Người dùng không tồn tại.".encode())

            elif request.startswith("SEND_MESSAGE"):
                _, sender_username, recipient_username, ciphertext = request.split("|", 3)
                if recipient_username in messages:
                    messages[recipient_username].append((sender_username, ciphertext))  # Lưu tên người gửi
                    client_socket.send("[Server] Tin nhắn đã được gửi.".encode())
                else:
                    client_socket.send("[Server] Người nhận không tồn tại.".encode())

            elif request.startswith("GET_MESSAGES"):
                _, username = request.split("|")
                if username in messages:
                    client_socket.send(str(messages[username]).encode())  # Gửi danh sách tin nhắn
                    messages[username] = []  # Xóa tin nhắn sau khi gửi
                else:
                    client_socket.send("[Server] Không có tin nhắn.".encode())

        except Exception as e:
            print(f"[Server] Lỗi từ client {address}: {e}")
            break

    client_socket.close()
    print(f"[Server] Ngắt kết nối từ {address}")


def start_server(host="localhost", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[Server] Đang chạy tại {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()


if __name__ == "__main__":
    start_server()
