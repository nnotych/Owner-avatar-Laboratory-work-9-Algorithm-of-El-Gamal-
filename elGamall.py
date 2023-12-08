import random

def is_prime(n, k=5):
    """Перевірка, чи є число простим, за допомогою тесту Рабіна-Міллера."""
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=1024):
    """Генерація простого числа за допомогою тесту Рабіна-Міллера."""
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 == 0:
            candidate += 1
        if is_prime(candidate):
            return candidate

def primitive_root(p):
    """Знаходження первісного кореня за модулем p."""
    if p == 2:
        return 1
    phi = p - 1
    for g in range(2, p):
        if pow(g, phi // 2, p) == 1:
            continue
        return g

def gen_key(q):
    """Генерація закритого ключа."""
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

def power(a, b, c):
    """Модульна експонентація."""
    result = 1
    a = a % c
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % c
        b //= 2
        a = (a * a) % c
    return result

def encrypt_char(char, s):
    """Шифрування одного символу."""
    return s * ord(char)

def encrypt(msg, q, h, g):
    """Асиметричне шифрування."""
    k = gen_key(q)  # Закритий ключ для відправника
    s = power(h, k, q)
    p = power(g, k, q)
    en_msg = [encrypt_char(char, s) for char in msg]

    return en_msg, p

def decrypt(en_msg, p, key, q):
    """Дешифрування."""
    h = power(p, key, q)
    dr_msg = [chr(int(char / h)) for char in en_msg]
    return dr_msg

def print_encrypted_message(en_msg):
    """Вивід зашифрованого повідомлення."""
    print("Зашифроване повідомлення:")
    for char in en_msg:
        print(char, end=' ')
    print()

def main():
    msg = 'Nikita'
    print("Оригінальне повідомлення:", msg)

    q = generate_prime()
    g = primitive_root(q)

    key = gen_key(q)  # Закритий ключ для отримувача
    h = power(g, key, q)
    print("g використовується:", g)
    print("g^a використовується:", h)

    en_msg, p = encrypt(msg, q, h, g)
    dr_msg = decrypt(en_msg, p, key, q)
    dmsg = ''.join(dr_msg)
    print("Розшифроване повідомлення:", dmsg)

    print_encrypted_message(en_msg)

if __name__ == '__main__':
    main()
