import numpy as np
import cv2

#Smoothing
def median(filename, k_size=3):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	blurred = cv2.medianBlur(img, k_size)

	return [img, blurred]

def denoise(filename, filter_strength=20):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	denoised = cv2.fastNlMeansDenoising(img, h=filter_strength)

	return [img, denoised]

def equalizeHist(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	equalized = cv2.equalizeHist(img)

	return [img, equalized]

def CLAHE(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	clahe = cv2.createCLAHE()
	equalized = clahe.apply(img)

	return [img, equalized]

def logTransform(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	#Se convierte la imagen a CV_32F
	transformed = np.float32(img)
	#Se le suma 1 por la formula c log(r + 1)
	transformed = transformed + 1
	#Se le aplica el logaritmo
	transformed = cv2.log(transformed)
	#Se escalan los valores, de nuevo a 8 bits
	transformed = cv2.convertScaleAbs(transformed)
	#Se normalizan los valores a 0-255
	cv2.normalize(src=transformed, dst=transformed, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

	return [img, transformed]

def gammaCorrection(filename, pow_value=3):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	transformed = img / 255.0
	transformed = cv2.pow(transformed, pow_value)
	transformed = np.uint8(transformed*255)

	return [img, transformed]

def cannyEdge(filename, t_1, t_2, aperture=3, l2gradient=False):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	
	transformed = np.copy(img)
	cv2.Canny(img, t_2, t_1, transformed, aperture, l2gradient)

	return [img, transformed]

def sobel(filename, dx=1, dy=1, k_size=3, delta=0):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	transformed = np.copy(img)
	cv2.Sobel(src=img, ddepth=-1, dx=dx, dy=dy, dst=transformed, ksize=k_size, delta=delta, borderType=cv2.BORDER_REPLICATE)

	ret, transformed = cv2.threshold(transformed,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	return [img, transformed]