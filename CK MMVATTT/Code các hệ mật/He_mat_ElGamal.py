import random

# Tính giá trị (x^y) mod p bằng phương pháp tích lũy thừa nhanh
def power(x, y, p):
    res = 1
    x = x % p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

# Tìm số nguyên tố 
def find_prime(bits):
    while True:
        start = random.getrandbits(bits)
        start |= 1  # Đảm bảo số đó là số lẻ
        if isPrime(start):
            return start

# Hàm kiểm tra nguyên tố
def isPrime(n, k=500):
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

# Thực hiện vòng thử nghiệm Miller-Rabin để kiểm tra tính khả năng nguyên tố
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

# Nghịch đảo của n trong mod p
def mod_inverse(n, p):
    gcd, x, y = extended_gcd(n, p)
    if gcd != 1:
        raise ValueError(f"Nghịch đảo không tồn tại vì gcd({n}, {p}) ≠ 1")
    return x % p

# Euclid mở rộng
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Sinh khóa công khai và khóa bí mật cho ElGamal
def generate_elgamal_keys(bits):
    print(f"1. Khởi tạo")
    print(f"Sinh số nguyên tố p với độ dài {bits} bit:")
    p = find_prime(bits)
    print(f"   p = {p}")

    # Bước 2: Chọn số nguyên ngẫu nhiên g (gốc sinh)
    g = 2  # Trong nhiều trường hợp, g có thể được chọn là 2 hoặc 3
    print(f"Chọn phần tử sinh g = {g}.")

    # Bước 3: Chọn số bí mật x và tính y
    x = random.randint(1, p - 2)  # Chọn x ngẫu nhiên trong [1, p-2]
    y = power(g, x, p)  # Tính y = g^x mod p
    print(f"Chọn khóa riêng x trong khoảng từ 1 đên p-2: x = {x} và tính khóa công khai y = g^x mod p:")
    print(f"   y = {y}")

    # Khóa công khai và khóa bí mật
    public_key = (p, g, y)
    private_key = x
    
    return public_key, private_key

# Mã hóa bằng ElGamal
def encrypt(message, public_key):
    p, g, y = public_key
    k = random.randint(1, p - 2)  # Chọn k ngẫu nhiên trong [1, p-2]
    print("2. Mã khóa")
    print(f"Chọn ngẫu nhiên k trong khoảng từ 1 đến p-2 và k phải khác 0 module p-1:")
    print(f"   k = {k}")
    
    # Tính c1 = g^k mod p
    c1 = power(g, k, p)
    print(f"Tính c1 = g^k mod p:")
    print(f"   c1 = {c1}")
    
    # Tính c2 = (m * y^k) mod p
    c2 = (message * power(y, k, p)) % p
    print(f"Tính c2 = (m * y^k) mod p:")
    print(f"   c2 = {c2}")
    
    return c1, c2

# Giải mã bằng ElGamal
def decrypt(ciphertext, private_key, public_key):
    c1, c2 = ciphertext
    p = public_key[0]
    print(f"3. Giải mã bản mã (c1, c2) = ({c1}, {c2}) với khóa bí mật x = {private_key}:")
    
    # Tính m = c2 * (c1^(-x mod p)) mod p
    s = power(c1, private_key, p)  # s = c1^x mod p
    m = (c2 * mod_inverse(s, p)) % p  # m = c2 * s^(-1) mod p
    print(f"   Bản rõ sau giải mã: m = {m}")
    
    return m

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

# Demo sử dụng hệ mật ElGamal
def elgamal_demo():
    bits = 1024  # số bit số nguyên tố
    public_key, private_key = generate_elgamal_keys(bits)

    # Mã hóa và giải mã một thông điệp
    message_text = "YEUTOQUOCYEUDONGBAO"
    print(f"\nThông điệp gốc: {message_text}")
    message = text_to_number(message_text)
    print(f"Chuyển '{message_text}' thành số: {message}")

    ciphertext = encrypt(message, public_key)
    decrypted_message = decrypt(ciphertext, private_key, public_key)
    decrypted_text = number_to_text(decrypted_message)

    print(f"\nThông điệp đã mã hóa: {ciphertext}")
    print(f"Thông điệp đã giải mã: {decrypted_text}")

# Chạy demo
elgamal_demo()
