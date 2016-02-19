import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import cv2

#Smoothing
def median(filename, k_size=3):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	blurred = cv2.medianBlur(img, k_size)

	return [img, blurred]

def gaussian(filename, k_size, sigma_x, sigma_y):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	blurred = np.copy(img)
	cv2.GaussianBlur(img, (k_size, k_size), sigma_x, blurred, sigma_y, cv2.BORDER_REPLICATE)

	return [img, blurred]

def denoise(filename, filter_strength=20):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	denoised = cv2.fastNlMeansDenoising(img, h=filter_strength)

	return [img, denoised]

def equalizeHist(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	equalized = cv2.equalizeHist(img)

	return [img, equalized]

def CLAHE(filename, clip_limit=2.0):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	clahe = cv2.createCLAHE(clipLimit=clip_limit)
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

def addSaltPepperGaussianNoise():
	img = cv2.imread('resources/testing/process.jpg', cv2.IMREAD_GRAYSCALE)
	
	row,col = img.shape
	s_vs_p = 0.5
	amount = 0.01
	out = img
	# Salt mode
	num_salt = np.ceil(amount * img.size * s_vs_p)
	coords = [np.random.randint(0, i - 1, int(num_salt))
			for i in img.shape]
	out[coords] = 255

	# Pepper mode
	num_pepper = np.ceil(amount* img.size * (1. - s_vs_p))
	coords = [np.random.randint(0, i - 1, int(num_pepper))
			for i in img.shape]
	out[coords] = 0

	out = Image.fromarray(out)
	out.save('resources/testing/process_salt.jpg')

if __name__ == "__main__":
	addSaltPepperGaussianNoise()