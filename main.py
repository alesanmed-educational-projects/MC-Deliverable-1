import numpy as np
import cv2

img = cv2.imread('resources/noisy.png', cv2.IMREAD_GRAYSCALE)

print(img.shape)

cv2.namedWindow('Foto', cv2.WINDOW_NORMAL)
cv2.imshow('Foto', img)
cv2.waitKey(0)
cv2.destroyAllWindows()