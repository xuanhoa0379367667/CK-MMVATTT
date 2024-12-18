### File: He_mat_Elliptic.py
def elliptic_multiply(P, s, a, p):
    Q = None
    R = P
    while s > 0:
        if s % 2 == 1:
            Q = elliptic_add(Q, R, a, p)
        R = elliptic_add(R, R, a, p)
        s //= 2
    return Q

def elliptic_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if P == Q:
        lam = ((3 * x1**2 + a) * pow(2 * y1, -1, p)) % p
    else:
        lam = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return x3, y3
