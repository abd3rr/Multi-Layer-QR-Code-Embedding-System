import os
import numpy as np
import cv2

def decomposer_en_binaire(nombre):
    a = nombre % 2
    b = nombre // 2
    return a, b

def inserer_multiple_qr(host_qr, hidden_qrs, n):
    height, width = host_qr.shape
    P = np.zeros((height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            if host_qr[i, j] == 0:
                P[i, j] = sum(hidden_qrs[k][i, j] << k for k in range(n))
            else:
                P[i, j] = 255 - sum(hidden_qrs[k][i, j] << k for k in range(n))
    
    return P

def extraire_multiple_qr(Q, n):
    height, width = Q.shape
    extracted_imgs = [np.zeros((height, width), dtype=np.uint8) for _ in range(n)]

    for i in range(height):
        for j in range(width):
            if Q[i, j] >= 2**(n+1):
                for k in range(n):
                    extracted_imgs[k][i, j] = (Q[i, j] >> k) & 1
            else:
                Q_val = 255 - Q[i, j]
                for k in range(n):
                    extracted_imgs[k][i, j] = (Q_val >> k) & 1

    return extracted_imgs


current_directory = os.getcwd()
qr_codes_directory = os.path.join(current_directory, 'qrCodes')
host_qr_path = os.path.join(qr_codes_directory, 'host_qr.png')
host_qr = cv2.imread(host_qr_path, cv2.IMREAD_GRAYSCALE)


hidden_qrs = []
for i in range(1, 6):
    hidden_qr_path = os.path.join(qr_codes_directory, f'hidden_qr{i}.png')
    hidden_qr = cv2.imread(hidden_qr_path, cv2.IMREAD_GRAYSCALE)
    hidden_qrs.append((hidden_qr > 0).astype(np.uint8))





n = 5  # nombre hidden qr codes 
P = inserer_multiple_qr(host_qr, hidden_qrs, n)

augmented_qr_path = os.path.join(qr_codes_directory, 'augmented_qr_multiple.png')
cv2.imwrite(augmented_qr_path, P)

extracted_imgs = extraire_multiple_qr(P, n)

for i, img in enumerate(extracted_imgs):
    extracted_qr_path = os.path.join(qr_codes_directory, f'extracted_qr{i+1}.png')
    cv2.imwrite(extracted_qr_path, img * 255)  
