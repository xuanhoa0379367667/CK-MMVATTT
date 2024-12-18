import random

# Tính (a^b) mod p bằng lũy thừa nhanh
def power(a, b, p):
    result = 1
    a = a % p
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % p
        b = b // 2
        a = (a * a) % p
    return result

# Kiểm tra số nguyên tố bằng thử nghiệm Miller-Rabin
def is_prime(n, k=500):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    d = n - 1
    while d % 2 == 0:
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True

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
    
    # Nếu gcd(n, p) != 1, thì nghịch đảo không tồn tại
    if gcd != 1:
        raise ValueError(f"Nghịch đảo không tồn tại vì gcd({n}, {p}) ≠ 1")
    
    # Nghịch đảo modulo là giá trị x (có thể cần điều chỉnh để x dương)
    return x % p

# Hàm sinh số nguyên tố có bits bits
def generate_large_prime(bits):
    while True:
        start = random.getrandbits(bits)
        start |= 1  # Đảm bảo số đó là số lẻ
        if is_prime(start):
            return start

# Hàm kiểm tra tính nguyên thủy
def is_primitive_root(g, p):
    # Tính q từ p
    q = (p - 1) // 2
    
    # Kiểm tra điều kiện nguyên thủy
    if power(g, q, p) == 1 or power(g, 2, p) == 1:
        return False
    return True

# Hàm tìm phần tử nguyên thủy nhỏ nhất
def find_smallest_primitive_root(p):
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None

def find_coprime(p_minus_1):
    """Tìm số k nguyên tố cùng nhau với (p-1)"""
    while True:
        k = random.randint(2, p_minus_1 - 1)
        gcd, _, _ = extended_gcd(k, p_minus_1)
        if gcd == 1:
            return k

def elgamal_keygen(p, alpha):
    """Tạo khóa công khai và khóa riêng"""
    a = random.randint(2, p-2)  # Khóa riêng
    beta = power(alpha, a, p)     # Khóa công khai
    return a, beta


def elgamal_encrypt(p, alpha, beta, m):
    """Mã hóa thông điệp"""
    k = random.randint(2, p-2)
    y1 = power(alpha, k, p)           # y1 = alpha^k mod p
    y2 = (m * power(beta, k, p)) % p  # y2 = (m * beta^k) mod p
    return y1, y2

def elgamal_decrypt(p, a, y1, y2):
    """Giải mã thông điệp"""
    s = power(y1, a, p)            # s = y1^a mod p
    s_inv = mod_inverse(s, p)         # Nghịch đảo của s mod p
    m = (y2 * s_inv) % p         # m = (y2 * s_inv) mod p
    return m

# Chuyển văn bản thành số theo hệ cơ số 26
def text_to_number(text):
    number = 0
    base = 26
    for char in text:
        number = number * base + (ord(char) - ord('A'))  # 'A' = 0, 'B' = 1, ...
    return number

# Chuyển số thành văn bản
def number_to_text(number):
    base = 26
    text = ""
    while number > 0:
        number, remainder = divmod(number, base)
        text = chr(remainder + ord('A')) + text
    return text

def elgamal_sign(p, alpha, a, x):
    """Tạo chữ ký ElGamal cho thông điệp x"""
    p_minus_1 = p - 1
    k = find_coprime(p_minus_1)  # Tìm k nguyên tố cùng nhau với p-1
    gamma = power(alpha, k, p)     # gamma = alpha^k mod p
    k_inv = mod_inverse(k, p_minus_1) # k^(-1) mod (p-1)
    delta = ((hash_function(x) - a * gamma) * k_inv) % p_minus_1  # delta = (h(x) - a*gamma) * k^(-1) mod (p-1)
    return k, k_inv, gamma, delta

def elgamal_verify(p, alpha, beta, x, gamma, delta):
    """Xác minh chữ ký ElGamal"""
    left_side = (power(beta, gamma, p) * power(gamma, delta, p)) % p
    right_side = power(alpha, hash_function(x), p)  # alpha^h(x) mod p
    return left_side == right_side

# Hàm băm tạm thời: h(x) = x
def hash_function(x):
    return x

def demo():
    bits = 1024
    # Bước 1: Tạo khóa ElGamal
    p = generate_large_prime(bits)
    g = find_smallest_primitive_root(p)
    a, beta = elgamal_keygen(p, g)

    # Bước 2: Mã hóa bản tin
    message = "YEUTOQUOCYEUDONGBAO"
    m = text_to_number(message)

    # Mã hóa bản tin với khóa công khai của người nhận
    y1, y2 = elgamal_encrypt(p, g, beta, m)

    # Bước 3: Ký bản tin x
    x = hash_function(m)  # Giả sử h(x) = x như yêu cầu
    k, k_inv, gamma, delta = elgamal_sign(p, g, a, x)   

    # Bước 4: Kiểm thử chữ ký
    valid_signature = elgamal_verify(p, g, beta, x, gamma, delta)

    # Bước 5: Xác thực chữ ký
    if valid_signature:
        print("Chữ ký hợp lệ.")
    else:
        print("Chữ ký không hợp lệ.")

    # In ra các bước
    print(f"\nThông tin khóa:")
    print(f"Số nguyên tố p với độ dài {bits} bit:")
    print(f"Khóa riêng a: {a}")
    print(f"Khóa công khai beta: {beta}")

    print(f"\nThông điệp gốc (chuỗi): {message}")
    print(f"Thông điệp gốc (số nguyên): {m}")

    print(f"\nMã hóa:")
    print(f"y1 = {y1} (y1 = g^k mod p)")
    print(f"y2 = {y2} (y2 = m * (beta^k mod p))")

    print(f"\nThông tin chữ ký:")
    print(f"k = {k} (ngẫu nhiên và nguyên tố cùng nhau với p-1)")
    print(f"k_inv = {k_inv} (nghịch đảo của k mod (p-1))")
    print(f"Chữ ký: gamma = {gamma} (gamma = g^k mod p), delta = {delta} (delta = (h(x) - a * gamma) * k^(-1) mod (p-1))")

    print(f"\nKiểm thử chữ ký: {'Đúng' if valid_signature else 'Sai'}")

    decrypted_message_int = elgamal_decrypt(p, a, y1, y2)
    decrypted_message = number_to_text(decrypted_message_int)
    print(f"Thông điệp sau khi giải mã: {decrypted_message}")

# Chạy chương trình

demo()