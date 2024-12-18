import random

# Tính giá trị (x^y) mod p bằng cách sử dụng phương pháp tích lũy thừa nhanh
def power(x, y, p):
    res = 1
    x = x % p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

# Thực hiện vòng thử nghiệm Miller-Rabin để kiểm tra tính khả năng nguyên tố của số n
def miillerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)
    if (x == 1 or x == n - 1):
        return True
    while (d != n - 1):
        x = (x * x) % n
        d *= 2
        if (x == 1):
            return False
        if (x == n - 1):
            return True
    return False

# Hàm kiểm tra nguyên tố
def isPrime(n, k):
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
    d = n - 1
    while (d % 2 == 0):
        d //= 2
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False
    return True

#kiểm tra
k = 500

# Tìm số nguyên tố lớn hơn hoặc bằng một giá trị nào đó
def find_prime(bits):
    while True:
        # Sinh một số ngẫu nhiên với số bit xác định
        start = random.getrandbits(bits)
        # Đảm bảo số đó là số lẻ
        start |= 1
        if isPrime(start, k):
            return start

# Thuật toán tìm ước chung lớn nhất bằng eclip mở rộng
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Nghịch đảo của n trong mod p
def mod_inverse(n, p):
    gcd, x, y = extended_gcd(n, p)
    
    # Nếu gcd(n, p) != 1, thì nghịch đảo không tồn tại
    if gcd != 1:
        raise ValueError(f"Nghịch đảo không tồn tại vì gcd({n}, {p}) ≠ 1")
    
    # Nghịch đảo modulo là giá trị x (có thể cần điều chỉnh để x dương)
    return x % p

# RSA: Sinh khóa, mã hóa, và giải mã
def generate_rsa_keys(bits):
    # Bước 1: Sinh 2 số nguyên tố p và q
    p = find_prime(bits)
    q = find_prime(bits)
    
    # Đảm bảo p khác q
    while p == q:
        q = find_prime(bits)
    
    # Bước 2: Tính n và ϕ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Bước 3: Chọn e sao cho gcd(e, ϕ(n)) = 1
    e = 65537
    if extended_gcd(e, phi_n)[0] != 1:
        raise ValueError("e và ϕ(n) không nguyên tố cùng nhau!")
    
    # Bước 4: Tính d là nghịch đảo của e modulo ϕ(n)
    d = mod_inverse(e, phi_n)
    
    # Khóa công khai và khóa bí mật
    public_key = (n, e)
    private_key = (n, d)
    
    return public_key, private_key

# Mã hóa
def encrypt(message, public_key):
    n, e = public_key
    return power(message, e, n)

# Giải mã
def decrypt(ciphertext, private_key):
    n, d = private_key
    return power(ciphertext, d, n)

# Tạo chữ ký
def signature(message, private_key):
    n, d = private_key
    return power(message, d, n)

# Xác thực chữ ký
def verify(signature, message, public_key):
    n, e = public_key
    return power(signature, e, n) == message

# Chuyển văn bản thành số theo hệ cơ số 26
def text_to_number(text):
    number = 0
    base = 26
    for char in text:
        number = number * base + (ord(char) - ord('A')) + 1  # 'A' = 1, 'B' = 2, ..., 'Z' = 26
    return number

# Chuyển số thành văn bản
def number_to_text(number):
    base = 26
    text = ""
    while number > 0:
        number, remainder = divmod(number - 1, base)  # Trừ 1 để điều chỉnh về 0-index
        text = chr(remainder + ord('A')) + text
    return text

# Demo sơ đồ chữ ký RSA
def rsa_demo():
    bits = 2048  # Số bit để tìm kiếm số nguyên tố

    # Sinh khóa cho A
    public_key_A, private_key_A = generate_rsa_keys(bits)
    
    # Sinh khóa cho B
    public_key_B, private_key_B = generate_rsa_keys(bits)

    # In ra khóa công khai và bí mật của A và B
    print(f"Khóa công khai của A: (n_A={public_key_A[0]}, e_A={public_key_A[1]})")
    print(f"Khóa bí mật của A: (d_A={private_key_A[1]})")
    print(f"Khóa công khai của B: (n_B={public_key_B[0]}, e_B={public_key_B[1]})")
    print(f"Khóa bí mật của B: (d_B={private_key_B[1]})")
    
    # Bản tin A muốn gửi cho B
    message = "YEUTOQUOCYEUDONGBAO"
    print(f"Bản tin A gửi cho B (dạng chữ): {message}")

    # Chuyển bản tin thành số
    message_number = text_to_number(message)
    print(f"Bản tin A gửi cho B (dạng số): {message_number}")
    
    # A mã hóa bản tin để gửi B (sử dụng khóa công khai của B)
    encrypted_message = encrypt(message_number, public_key_B)
    print(f"Bản tin đã mã hóa để gửi B: {encrypted_message}")

    # A tạo chữ ký cho bản tin (sử dụng khóa bí mật của A)
    signature_A = signature(message_number, private_key_A)
    print(f"Chữ ký của A: {signature_A}")

    # B giải mã bản tin nhận được (sử dụng khóa bí mật của B)
    decrypted_message = decrypt(encrypted_message, private_key_B)
    decrypted_text = number_to_text(decrypted_message)
    print(f"Bản tin B giải mã được (dạng số): {decrypted_message}")
    print(f"Bản tin B giải mã được (dạng chữ): {decrypted_text}")

    # B xác thực chữ ký (sử dụng khóa công khai của A)
    is_signature_valid = verify(signature_A, decrypted_message, public_key_A)
    print(f"Kết quả xác thực chữ ký: {'TRUE' if is_signature_valid else 'FALSE'}")

# Chạy demo
rsa_demo()
