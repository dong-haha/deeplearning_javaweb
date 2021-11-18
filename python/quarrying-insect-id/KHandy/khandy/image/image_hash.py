import cv2
import numpy as np


def calc_image_ahash(image):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (8, 8))

    meanval = cv2.mean(resized)[0]
    hashval = int(0)
    for i in range(8):
        for j in range(8):
            mask = int(resized[i,j] - meanval >= 1e-5)
            hashval |= mask << (i * 8 + j)
    return hashval

    
def calc_image_phash(image):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (32, 32))

    dft = cv2.dft(resized.astype(np.float32))
    meanval = cv2.mean(dft[:8,:8])[0]
    hashval = int(0)
    for i in range(8):
        for j in range(8):
            mask = int(dft[i,j] - meanval >= 1e-5)
            hashval |= mask << (i * 8 + j)
    return hashval

    
def calc_image_dhash(image):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(image, (9, 8))

    hashval = int(0)
    for i in range(8):
        for j in range(8):
            mask = int(resized[i,j] > resized[i,j+1])
            hashval |= mask << (i * 8 + j)
    return hashval
    
    
    