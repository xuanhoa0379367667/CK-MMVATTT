import socket
import threading
import customtkinter as ctk
from tkinter import simpledialog
from He_mat_RSA import generate_rsa_keys, text_to_number, encrypt, decrypt, number_to_text


class ClientApp:
    def __init__(self, username, server_host='localhost', server_port=12345):
        self.username = username
        self.server_host = server_host
        self.server_port = server_port
        self.public_key, self.private_key = generate_rsa_keys(1024)

        # Kết nối tới server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        # Cài đặt giao diện
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title(f"Chat - {self.username}")
        self.root.geometry("600x600")

        # Khu vực hiển thị tin nhắn
        self.chat_area = ctk.CTkTextbox(self.root, height=200, width=550, state='disabled', wrap='word', corner_radius=8)
        self.chat_area.pack(pady=10)

        # Khu vực hiển thị chi tiết RSA
        ctk.CTkLabel(self.root, text="Chi tiết RSA:", font=("Arial", 14, "bold")).pack(pady=(5, 0))
        self.rsa_area = ctk.CTkTextbox(self.root, height=100, width=550, state='disabled', wrap='word', corner_radius=8)
        self.rsa_area.pack(pady=5)
        self.show_rsa_details()

        # Khu vực nhập tin nhắn
        ctk.CTkLabel(self.root, text="Nhập tên người nhận:", font=("Arial", 12)).pack()
        self.recipient_entry = ctk.CTkEntry(self.root, width=400, height=30, corner_radius=8)
        self.recipient_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Nhập tin nhắn:", font=("Arial", 12)).pack()
        self.input_area = ctk.CTkEntry(self.root, width=400, height=30, corner_radius=8)
        self.input_area.pack(pady=5)

        # Nút gửi tin nhắn
        self.send_button = ctk.CTkButton(self.root, text="Gửi", command=self.send_message_ui, corner_radius=8)
        self.send_button.pack(pady=5)

        # Nút nhận tin nhắn
        self.receive_button = ctk.CTkButton(self.root, text="Nhận tin nhắn", command=self.receive_messages_ui, corner_radius=8)
        self.receive_button.pack(pady=5)

        # Đăng ký khóa công khai
        self.register_key()

        self.root.mainloop()

    def register_key(self):
        """Đăng ký khóa công khai với server."""
        threading.Thread(target=self._register_key_thread, daemon=True).start()

    def _register_key_thread(self):
        request = f"REGISTER|{self.username}|{self.public_key}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(4096).decode()
        self.update_chat(f"[Server] {response}")

    def send_message_ui(self):
        """Gửi tin nhắn từ giao diện."""
        recipient = self.recipient_entry.get().strip()
        message_text = self.input_area.get().strip()

        if not recipient or not message_text:
            self.update_chat("[Lỗi] Vui lòng nhập tên người nhận và nội dung tin nhắn.")
            return

        threading.Thread(target=self.send_message, args=(recipient, message_text), daemon=True).start()

    def send_message(self, recipient_username, message_text):
        """Gửi tin nhắn mã hóa đến người nhận."""
        recipient_key = self.get_public_key(recipient_username)
        if not recipient_key:
            return

        message_number = text_to_number(message_text)
        ciphertext = encrypt(message_number, recipient_key)

        request = f"SEND_MESSAGE|{self.username}|{recipient_username}|{ciphertext}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(4096).decode()
        self.update_chat(f"[Server] {response}")

    def get_public_key(self, recipient_username):
        """Lấy khóa công khai của người nhận."""
        request = f"GET_KEY|{recipient_username}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(4096).decode()
        if response.startswith("[Server]"):
            self.update_chat(response)
            return None
        return eval(response)

    def receive_messages_ui(self):
        """Nhận tin nhắn từ giao diện."""
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """Nhận và giải mã tin nhắn từ server."""
        request = f"GET_MESSAGES|{self.username}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(4096).decode()

        if response.startswith("[Server]") or response == "[]":
            self.update_chat("[Server] Không có tin nhắn mới.")
            return

        try:
            messages = eval(response)
            for sender, ciphertext in messages:
                decrypted_message_number = decrypt(int(ciphertext), self.private_key)
                decrypted_text = number_to_text(decrypted_message_number)
                self.update_chat(f"{sender}: {decrypted_text}")
        except Exception as e:
            self.update_chat(f"[Lỗi] Khi giải mã tin nhắn: {e}")

    def show_rsa_details(self):
        """Hiển thị chi tiết khóa RSA."""
        n, e = self.public_key
        _, d = self.private_key
        details = f"n = {n}\ne = {e}\nd = {d}"
        self.rsa_area.configure(state='normal')
        self.rsa_area.insert("end", details)
        self.rsa_area.configure(state='disabled')

    def update_chat(self, message):
        """Cập nhật giao diện chat."""
        self.chat_area.configure(state='normal')
        self.chat_area.insert("end", f"{message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see("end")


def get_username():
    """Hiển thị hộp thoại nhập tên người dùng."""
    root = ctk.CTk()
    root.withdraw()
    username = simpledialog.askstring("Đăng nhập", "Nhập tên người dùng:")
    return username


if __name__ == "__main__":
    username = get_username()
    if username:
        ClientApp(username)
    else:
        print("Tên người dùng không được bỏ trống!")
