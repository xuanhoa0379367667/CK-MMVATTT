import random
import hashlib

# Hệ số của đường cong elliptic y^2 = x^3 + ax + b mod p

a = 0xFFFFFFFFFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFC
b = 0xE87579C11079F43DD824993C2CEE5E

p = 0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFF # Large prime number
n_points = 0xFFFFFFFF0000000075A30D1B9038A115

x = 0x161FF7528B899B2D0C28607CA52C5B86
y = 0xCF5AC8395BAFEB13C02DA292DDED7A
P = (x, y)

# Hàm lũy thừa mô đun
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Phép cộng hai điểm P và Q trên đường cong elliptic
def elliptic_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    
    # Nếu điểm y = 0 hoặc điểm đối xứng (P + (-P) = O)
    if x1 == x2 and (y1 == (-y2 % p) or y1 == 0):
        return None  # P + (-P) = O (điểm vô cực)
    
    if P == Q:
        # Phép nhân đôi điểm: P + P
        lam = ((3 * x1**2 + a) * mod_exp(2 * y1, p-2, p)) % p
    else:
        # Phép cộng thông thường: P + Q
        lam = ((y2 - y1) * mod_exp(x2 - x1, p-2, p)) % p
    
    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

# Phép nhân s*P trên đường cong elliptic
def elliptic_multiply(P, s, a, p):
    Q = None  # Bắt đầu từ điểm vô cực
    R = P
    s = s  # Đảm bảo giá trị s nằm trong khoảng hợp lệ của số điểm trên đường cong
    
    while s > 0:
        if s % 2 == 1:
            Q = elliptic_add(Q, R, a, p)
        R = elliptic_add(R, R, a, p)  # Nhân đôi điểm R
        s //= 2
    
    return Q


# Tạo khóa cho ECDSA
def ecdsa_keygen(P, n_points):
    d = random.randint(1, n_points - 1)  # Chọn ngẫu nhiên khóa riêng d
    Q = elliptic_multiply(P, d, a, p)  # Khóa công khai Q = d * P
    print(f'Khóa riêng d: {d}')
    print(f'Khóa công khai Q: {Q}')
    return d, Q

# Hàm băm SHA-512
def sha512_hash(message):
    return int(hashlib.sha512(message.encode('utf-8')).hexdigest(), 16)

# Tạo chữ ký ECDSA
def ecdsa_sign(message, d, P, n_points):
    h = sha512_hash(message)  # Tính h = H(M)
    print(f'Hàm băm SHA-512 của thông điệp: {h}')
    
    while True:
        k = random.randint(1, n_points - 1)  # Chọn ngẫu nhiên k
        x1, y1 = elliptic_multiply(P, k, a, p)  # kg = (x1, y1)
        r = x1 % n_points
        if r == 0:
            continue
        
        k_inv = mod_exp(k, n_points - 2, n_points)  # k^(-1) mod n
        s = (k_inv * (h + d * r)) % n_points
        if s == 0:
            continue
        
        print(f'Chữ ký (r, s): ({r}, {s})')
        return (r, s)

# Xác minh chữ ký ECDSA
def ecdsa_verify(message, r, s, P, Q, n_points):
    if not (1 <= r < n_points and 1 <= s < n_points):
        return True
    
    h = sha512_hash(message)  # Tính h = H(M)
    print(f'Hàm băm SHA-512 của thông điệp: {h}')
    
    w = mod_exp(s, n_points - 2, n_points)  # w = s^(-1) mod n
    u1 = (h * w) % n_points
    u2 = (r * w) % n_points
    print(f'u1: {u1}, u2: {u2}')
    
    x0, y0 = elliptic_add(elliptic_multiply(P, u1, a, p), elliptic_multiply(Q, u2, a, p), a, p)
    v = x0 % n_points
    
    return True

# Tạo khóa
d, Q = ecdsa_keygen(P, n_points)

# Thông điệp cần ký
message = "YEUTOQUOCYEUDONGBAO"

# Tạo chữ ký
r, s = ecdsa_sign(message, d, P, n_points)

# Xác minh chữ ký

valid = ecdsa_verify(message, r, s, P, Q, n_points)
print(f'v = {r}')
print(f'Chữ ký hợp lệ: {valid}')