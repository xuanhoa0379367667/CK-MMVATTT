import customtkinter as ctk
from tkinter import messagebox
from He_mat_RSA import generate_rsa_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt, text_to_number, number_to_text
from He_mat_ElGamal import generate_elgamal_keys, encrypt as elgamal_encrypt, decrypt as elgamal_decrypt, text_to_number, number_to_text
from He_mat_Elliptic import elliptic_multiply

def handle_encryption():
    system = selected_system.get()
    byte_length = int(entry_bytes.get())
    message = entry_message.get()

    if not byte_length or not message:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập số byte và văn bản!")
        return

    output_text.delete("1.0", "end")  # Xóa kết quả cũ

    try:
        if system == "RSA":
            public_key, private_key = generate_rsa_keys(byte_length)
            num_message = text_to_number(message)
            ciphertext = rsa_encrypt(num_message, public_key)
            decrypted_message = rsa_decrypt(ciphertext, private_key)
            result_text = (
                f"=== RSA ===\n"
                f"Khóa công khai: n = {public_key[0]}, e = {public_key[1]}\n"
                f"Khóa bí mật: d = {private_key[1]}\n"
                f"Bản mã: {ciphertext}\n"
                f"Bản giải mã: {number_to_text(decrypted_message)}\n"
            )
        elif system == "ElGamal":
            public_key, private_key = generate_elgamal_keys(byte_length)
            num_message = text_to_number(message)
            ciphertext = elgamal_encrypt(num_message, public_key)
            decrypted_message = elgamal_decrypt(ciphertext, private_key, public_key)
            result_text = (
                f"=== ElGamal ===\n"
                f"Khóa công khai: p = {public_key[0]}, g = {public_key[1]}, y = {public_key[2]}\n"
                f"Khóa bí mật: x = {private_key}\n"
                f"Bản mã: (c1 = {ciphertext[0]}, c2 = {ciphertext[1]})\n"
                f"Bản giải mã: {number_to_text(decrypted_message)}\n"
            )
        elif system == "ECC":
            base_point = (1, 2)  # Điểm cơ sở mô phỏng
            secret_key = 123  # Số ngẫu nhiên mô phỏng
            result_point = elliptic_multiply(base_point, secret_key, 0, 97)
            result_text = (
                f"=== ECC ===\n"
                f"Điểm cơ sở: {base_point}\n"
                f"Khóa bí mật: {secret_key}\n"
                f"Điểm kết quả: {result_point}\n"
            )
        output_text.insert("1.0", result_text)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Giao diện CustomTkinter
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Ứng dụng Mã hóa")
root.geometry("800x700")

# Biến lựa chọn hệ mật
selected_system = ctk.StringVar(value="RSA")

# Giao diện
ctk.CTkLabel(root, text="Chọn hệ mã hóa", font=("Arial", 16)).pack(pady=5)
menu = ctk.CTkOptionMenu(root, values=["RSA", "ElGamal", "ECC"], variable=selected_system)
menu.pack(pady=5)

ctk.CTkLabel(root, text="Nhập số byte (độ dài khóa):", font=("Arial", 14)).pack(pady=5)
entry_bytes = ctk.CTkEntry(root, placeholder_text="VD: 1024", font=("Arial", 14), width=400)
entry_bytes.pack(pady=5)

ctk.CTkLabel(root, text="Nhập nội dung văn bản:", font=("Arial", 14)).pack(pady=5)
entry_message = ctk.CTkEntry(root, placeholder_text="Nhập văn bản cần mã hóa", font=("Arial", 14), width=400)
entry_message.pack(pady=5)

btn_encrypt = ctk.CTkButton(root, text="Thực hiện mã hóa", command=handle_encryption, font=("Arial", 14), width=200)
btn_encrypt.pack(pady=10)

output_text = ctk.CTkTextbox(root, height=400, font=("Courier", 12), width=700)
output_text.pack(pady=10)

root.mainloop()
