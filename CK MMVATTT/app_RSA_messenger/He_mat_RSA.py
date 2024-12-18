### File: He_mat_RSA.py
import random

def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def isPrime(n, k=500):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(k):
        if not miillerTest(d, n):
            return False
    return True

def miillerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def find_prime(bits):
    while True:
        start = random.getrandbits(bits)
        start |= 1
        if isPrime(start):
            return start

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(n, p):
    gcd, x, y = extended_gcd(n, p)
    if gcd != 1:
        raise ValueError(f"No modular inverse for {n} mod {p}")
    return x % p

def generate_rsa_keys(bits):
    p = find_prime(bits)
    q = find_prime(bits)
    while p == q:
        q = find_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi_n)
    return (n, e), (n, d)

def encrypt(message, public_key):
    n, e = public_key
    return power(message, e, n)

def decrypt(ciphertext, private_key):
    n, d = private_key
    return power(ciphertext, d, n)

def text_to_number(text):
    number = 0
    for char in text:
        number = number * 26 + (ord(char) - ord('A')) + 1
    return number

def number_to_text(number):
    text = ""
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        text = chr(remainder + ord('A')) + text
    return text