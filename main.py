import random
import numpy as np

def generate_matrices(m):
    n = 2 ** m - 1
    k = n - m
    columns = []
    for i in range(1, 2 ** m):
        binary = bin(i)[2:].zfill(m)
        vec = [int(bit) for bit in reversed(binary)]
        columns.append(vec)
    single = []
    non_single = []
    for vec in columns:
        if sum(vec) == 1:
            single.append(vec)
        else:
            non_single.append(vec)
    #non_single[0], non_single[2] = non_single[2], non_single[0]
    columns = non_single + single
    H = []
    for i in range(m):
        H_row = [vec[i] for vec in columns]
        H.append(H_row)
    P_T = [row[:k] for row in H]
    P = list(zip(*P_T))
    P = [list(row) for row in P]
    G = []
    for i in range(k):
        identity = [1 if j == i else 0 for j in range(k)]
        G.append(identity + P[i])
    return G, H

def encode(u, G):
    k = len(G)
    n = len(G[0])
    codeword = [0] * n
    for j in range(n):
        for i in range(k):
            codeword[j] ^= u[i] * G[i][j]
    return codeword

def add_error(codeword):
    error_pos = random.randint(0, len(codeword) - 1)
    erroneous = codeword.copy()
    erroneous[error_pos] ^= 1
    return erroneous, error_pos

def compute_syndrome(received, H):
    m = len(H)
    syndrome = [0] * m
    for i in range(m):
        for j in range(len(received)):
            syndrome[i] ^= received[j] * H[i][j]
    return syndrome

def find_error(syndrome, H):
    for col in range(len(H[0])):
        if [H[row][col] for row in range(len(H))] == syndrome:
            return col
    return -1

def correct(received, error_pos):
    corrected = received.copy()
    if error_pos != -1:
        corrected[error_pos] ^= 1
    return corrected

m = 11
G, H = generate_matrices(m)
k = len(G)
n = len(G[0])

print("Породжуюча матриця G:")
for row in G:
    print(' '.join(map(str, row)))

"""print("\nПеревірочна матриця H:")
for row in H:
    print(' '.join(map(str, row)))"""

u = [random.randint(0, 1) for _ in range(k)]
print("\nCлово:", u)

codeword = encode(u, G)
print("Кодове слово:    ", codeword)

erroneous, true_error_pos = add_error(codeword)
print("Слово з помилкою:  ", erroneous, f"(Помилка в позиції {true_error_pos})")

syndrome = compute_syndrome(erroneous, H)
print("Синдром:          ", syndrome)

print("Транспонована матриця Н:")
i = -1
for row in np.array(H).transpose():
    i += 1
    if list(row) != list(syndrome):
        print(' '.join(map(str, row)) + "  " + str(i))
    else:
        print(' '.join(map(str, row)) + "  " + str(i) + "  -  позиція помилки")

error_pos = find_error(syndrome, H)
print("Знайдена позиція помилки:", error_pos)

corrected = correct(erroneous, error_pos)
print("Виправлене слово:", corrected)
print("Збіг з початковим:", corrected == codeword)