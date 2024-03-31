import os
import numpy as np
import cv2


def decomposer_en_binaire(nombre):
    a = nombre % 2
    b = nombre // 2
    return a, b

# insertion
def inserer_code_QR(porteur, cache, C, V):
    height, width = porteur.shape
    P = np.zeros_like(porteur)
    
    for i in range(height):
        for j in range(width):
            region_k = V[i, j]
            if C[region_k] == 0:
                P[i, j] = cache[i, j] + ((1 - cache[i, j]) * 2)
            else:
                P[i, j] = (1 - cache[i, j]) + (cache[i, j] * 2)
        
            if porteur[i, j] == 255:
                P[i, j] = 255 - P[i, j]
    
    return P


# extraction
def extraire_code_QR(Q, C, V):
    height, width = Q.shape
    I1 = np.zeros_like(Q)

    for i in range(height):
        for j in range(width):
            region_k = V[i, j]
            Q_ij = Q[i, j]
            if Q_ij < 4:
                a, b = decomposer_en_binaire(Q_ij)
            else:
                a, b = decomposer_en_binaire(255 - Q_ij)

            I1[i, j] = a if C[region_k] == 0 else b

    return I1 * 255



def my_voronoi(width, height, N):
    germes = np.random.rand(N, 2) * [width, height]
    V = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            distances = np.linalg.norm(germes - np.array([x, y]), axis=1)
            V[y, x] = np.argmin(distances)
    return V


current_directory = os.getcwd()
qr_codes_directory = os.path.join(current_directory, 'qrCodes')  
host_qr_path = os.path.join(qr_codes_directory, 'host_qr.png')  
hidden_qr_path = os.path.join(qr_codes_directory, 'hidden_qr.png')  


img_porteur = cv2.imread(host_qr_path, cv2.IMREAD_GRAYSCALE)
img_cache = (cv2.imread(hidden_qr_path, cv2.IMREAD_GRAYSCALE) > 0).astype(np.uint8) 


if img_porteur.shape != img_cache.shape:
    img_cache = cv2.resize(img_cache, (img_porteur.shape[1], img_porteur.shape[0]), interpolation=cv2.INTER_NEAREST)

N = 10  
V = my_voronoi(img_porteur.shape[1], img_porteur.shape[0], N)

# Partition
C = [0 if i < N/2 else 1 for i in range(N)]

P = inserer_code_QR(img_porteur, img_cache, C, V)
I1 = extraire_code_QR(P, C, V)

augmented_qr_path = os.path.join(qr_codes_directory,'augmented_qr.png')
extracted_qr_path = os.path.join(qr_codes_directory,'extracted_qr.png')

cv2.imwrite(augmented_qr_path, P)
cv2.imwrite(extracted_qr_path, I1)

augmented_qr_path, extracted_qr_path