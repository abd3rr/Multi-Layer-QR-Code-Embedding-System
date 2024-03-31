import os
import numpy as np
import cv2

def decomposer_en_binaire(nombre):
    a = nombre % 2
    b = nombre // 2
    return a, b

def my_voronoi_3(width, height):
    # 3 random seeds
    germes = np.random.rand(3, 2) * [width, height]
    V = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            distances = np.linalg.norm(germes - np.array([x, y]), axis=1)
            V[y, x] = np.argmin(distances)
    return V

def inserer_code_QR_secure(porteur, hidden_qrs, V):
    height, width = porteur.shape
    P = np.zeros_like(porteur)
    for i in range(height):
        for j in range(width):
            region = V[i, j]
            P[i, j] = sum(hidden_qrs[k][i, j] << k for k in range(4))  # 4 images
            if porteur[i, j] == 255:
                P[i, j] = 255 - P[i, j]
    return P

def extraire_code_QR_secure(Q, V, n):
    height, width = Q.shape
    extracted_imgs = [np.zeros((height, width), dtype=np.uint8) for _ in range(n)]
    permutations = {
        0: (0, 1, 2, 3),
        1: (1, 3, 2, 0),
        2: (2, 0, 3, 1),
    }
    for i in range(height):
        for j in range(width):
            region = V[i, j]
            perm = permutations[region]
            Q_val = Q[i, j] if Q[i, j] < 2**(n+1) else 255 - Q[i, j]
            for k in range(n):
                extracted_imgs[k][i, j] = (Q_val >> k) & 1
    return extracted_imgs
# loading host
current_directory = os.getcwd()
qr_codes_directory = os.path.join(current_directory, 'qrCodes')
host_qr_path = os.path.join(qr_codes_directory, 'host_qr.png')
host_qr = cv2.imread(host_qr_path, cv2.IMREAD_GRAYSCALE)

# loading hiddens
hidden_qrs = []
for i in range(1, 5):
    hidden_qr_path = os.path.join(qr_codes_directory, f'hidden_qr{i}.png')
    hidden_qr = cv2.imread(hidden_qr_path, cv2.IMREAD_GRAYSCALE)
    if hidden_qr is None or host_qr.shape != hidden_qr.shape:
        raise ValueError(f"Hidden QR code image {i} failed to load or mismatched size.")
    hidden_qrs.append((hidden_qr > 0).astype(np.uint8))


V = my_voronoi_3(host_qr.shape[1], host_qr.shape[0])
P_secure = inserer_code_QR_secure(host_qr, hidden_qrs, V)


augmented_qr_secure_path = os.path.join(qr_codes_directory, 'augmented_qr_secure.png')
cv2.imwrite(augmented_qr_secure_path, P_secure)

# extraction
extracted_imgs_secure = extraire_code_QR_secure(P_secure, V, 4)

for i, img in enumerate(extracted_imgs_secure):
    extracted_qr_path = os.path.join(qr_codes_directory, f'extracted_qr_secure{i+1}.png')
    cv2.imwrite(extracted_qr_path, img * 255)  # Convert binary to 0-255 scale for viewing
