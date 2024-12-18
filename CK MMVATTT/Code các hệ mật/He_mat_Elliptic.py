import random
# Coefficients of the elliptic curve y^2 = x^3 + ax + b mod p
a = 0xFFFFFFFFFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFC
b = 0xE87579C11079F43DD824993C2CEE5E

p = 2**128 - 2**97 - 1 # Large prime number

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Tonelli-Shanks algorithm for computing square roots mod p
def tonelli_shanks(n, p):
    assert mod_exp(n, (p - 1) // 2, p) == 1, "No square root exists"
    if p % 4 == 3:
        return mod_exp(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while mod_exp(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = mod_exp(z, q, p)
    t = mod_exp(n, q, p)
    r = mod_exp(n, (q + 1) // 2, p)
    while t != 1:
        t2 = t
        i = 0
        for i in range(1, m):
            t2 = mod_exp(t2, 2, p)
            if t2 == 1:
                break
        b = mod_exp(c, 2 ** (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p
    return r

# Check for existence of square root mod p
def mod_sqrt(n, p):
    if n % p == 0:
        return 0
    if mod_exp(n, (p - 1) // 2, p) != 1:
        return None
    return tonelli_shanks(n, p)

points = []

def k_th_random_point_on_curve(a, b, p, k):
    count = 0  # Biến đếm số điểm đã tìm thấy
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        y = mod_sqrt(y_squared, p)
        if y is not None:
            count += 1  # Tăng biến đếm
            if count == k:  # Nếu đã tìm thấy điểm thứ k
                return (x, y)  # Trả về điểm (x, y)
    return None  # Nếu không tìm thấy đủ điểm nào

# Addition of two points P and Q on the elliptic curve
def elliptic_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    
    # If point y = 0 or the symmetric point (P + (-P) = O)
    if x1 == x2 and (y1 == (-y2 % p) or y1 == 0):
        return None  # P + (-P) = O (infinity point)
    
    if P == Q:
        # Doubling points: P + P
        lam = ((3 * x1**2 + a) * mod_exp(2 * y1, p-2, p)) % p
    else:
        # Common addition: P + Q
        lam = ((y2 - y1) * mod_exp(x2 - x1, p-2, p)) % p
    
    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

# Scalar multiplication on the elliptic curve
def elliptic_multiply(P, s, a, p):
    Q = None  # Starting from infinity point
    R = P
    s = s  # Make sure the value of s is within the valid range of points on the curve
    
    while s > 0:
        if s % 2 == 1:
            Q = elliptic_add(Q, R, a, p)
        R = elliptic_add(R, R, a, p)  # Double the point R
        s //= 2
    
    return Q

# Check with any point P on the curve
x = 0x161FF7528B899B2D0C28607CA52C5B86
y = 0xCF5AC8395BAFEB13C02DA292DDED7A

P = (x, y)

# Bước 1: Chọn khóa bí mật và tính M = t * P
t = 123456789
M = elliptic_multiply(P, t, a, p)
print(f"Bước 1: Chọn khóa bí mật t = {t}")
print(f"Kết quả M = t * P = {M}")

# Bước 2: Thiết lập khóa công khai s = 2^31 - 1 và tính B = s * P
s = 2**31 - 1
B = elliptic_multiply(P, s, a, p)
print(f"Bước 2: Khóa công khai s = {s}")
print(f"Kết quả B = s * P = {B}")

# Bước 3a: Chọn số ngẫu nhiên k < 10^9
k = 987654321
print(f"Bước 3a: Số ngẫu nhiên k = {k}")

# Bước 3b: Tính M1 = k * P
M1 = elliptic_multiply(P, k, a, p)
print(f"Bước 3b: Mã hóa, M1 = k * P = {M1}")

# Bước 3c: Tính M2 = M + k * B
kB = elliptic_multiply(B, k, a, p)
M2 = elliptic_add(M, kB, a, p)
print(f"Bước 3c: Mã hóa, M2 = M + k * B = {M2}")

# Bước giải mã
# Bước 4: Tính lại M từ M1 và M2
M1_negative = (M1[0], -M1[1] % p)
decoded_M = elliptic_add(M2, elliptic_multiply(M1_negative, s, a, p), a, p)
print(f"Bước 4: Giải mã, tính lại M từ M1 và M2")
print(f"Kết quả M (sau giải mã) = {decoded_M}")

# Kiểm tra nếu quá trình giải mã khớp với M ban đầu
if decoded_M == M:
    print("Giải mã thành công, M khớp với giá trị ban đầu.")
else:
    print("Giải mã thất bại, M không khớp với giá trị ban đầu.")
