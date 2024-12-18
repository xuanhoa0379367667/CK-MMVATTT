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
def isPrime(n, k = 500):  # k là số lần kiểm tra
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

# Tìm số nguyên tố lớn hơn hoặc bằng một giá trị nào đó
def find_prime(bits):
    while True:
        start = random.getrandbits(bits)
        start |= 1  # Đảm bảo số đó là số lẻ
        if isPrime(start):
            return start

# Thuật toán tìm ước chung lớn nhất bằng Euclid mở rộng
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
    if gcd != 1:
        raise ValueError(f"Nghịch đảo không tồn tại vì gcd({n}, {p}) ≠ 1")
    return x % p

# RSA: Sinh khóa, mã hóa, và giải mã
def generate_rsa_keys(bits):
    print(f"1. Sinh 2 số nguyên tố p và q với độ dài {bits} bit:")
    p = find_prime(bits)
    q = find_prime(bits)
    print(f"   p = {p}")
    print(f"   q = {q}")
    
    # Đảm bảo p khác q
    while p == q:
        q = find_prime(bits)
    
    # Bước 2: Tính n và ϕ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    print(f"2. Tính n = p * q và ϕ(n) = (p-1)*(q-1):")
    print(f"   n = {n}")
    print(f"   ϕ(n) = {phi_n}")
    
    # Bước 3: Chọn e sao cho gcd(e, ϕ(n)) = 1
    e = 65537
    if extended_gcd(e, phi_n)[0] != 1:
        raise ValueError("e và ϕ(n) không nguyên tố cùng nhau!")
    print(f"3. Chọn e = {e} sao cho gcd(e, ϕ(n)) = 1.")
    
    # Bước 4: Tính d là nghịch đảo của e modulo ϕ(n)
    d = mod_inverse(e, phi_n)
    print(f"4. Tính d là nghịch đảo của e modulo ϕ(n):")
    print(f"   d = {d}")
    
    # Khóa công khai và khóa bí mật
    public_key = (n, e)
    private_key = (n, d)
    
    return public_key, private_key

# Mã hóa
def encrypt(message, public_key):
    n, e = public_key
    print(f"5. Mã hóa bản rõ {message} với khóa công khai (n={n}, e={e}):")
    ciphertext = power(message, e, n)
    print(f"   Bản mã: {ciphertext}")
    return ciphertext

# Giải mã
def decrypt(ciphertext, private_key):
    n, d = private_key
    print(f"6. Giải mã bản mã {ciphertext} với khóa bí mật (n={n}, d={d}):")
    plaintext = power(ciphertext, d, n)
    print(f"   Bản rõ sau giải mã: {plaintext}")
    return plaintext

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


# Demo sử dụng hệ mật RSA
def rsa_demo():
    bits = 2048  # 1024-bit
    public_key, private_key = generate_rsa_keys(bits)

    # Mã hóa và giải mã một thông điệp
    message_text = "YEUTOQUOCYEUDONGBAO"
    print(f"\nThông điệp gốc: {message_text}")
    message = text_to_number(message_text)
    print(f"Chuyển '{message_text}' thành số: {message}")
    
    ciphertext = encrypt(message, public_key)
    decrypted_message = decrypt(ciphertext, private_key)
    decrypted_text = number_to_text(decrypted_message)

    print(f"\nThông điệp đã mã hóa: {ciphertext}")
    print(f"Thông điệp đã giải mã: {decrypted_text}")

# Chạy demo
rsa_demo()
