import numpy as np
import cv2

#Smoothing
def median(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	blurred = cv2.medianBlur(img, 5)

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 400, 400)
	cv2.imshow('Original', img)

	cv2.namedWindow('Blurred', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Blurred', 400, 400)
	cv2.imshow('Blurred', blurred)
	cv2.waitKey(0)

	return

def denoise(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	denoised = cv2.fastNlMeansDenoising(img, h=20)

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 600, 600)
	cv2.imshow('Original', img)

	cv2.namedWindow('Denoised', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Denoised', 600, 600)
	cv2.imshow('Denoised', denoised)
	cv2.waitKey(0)

	return

def equalizeHist(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	equalized = cv2.equalizeHist(img)

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 400, 400)
	cv2.imshow('Original', img)

	cv2.namedWindow('Equalized', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Equalized', 400, 400)
	cv2.imshow('Equalized', equalized)
	cv2.waitKey(0)

	return

def CLAHE(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	clahe = cv2.createCLAHE()
	equalized = clahe.apply(img)

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 400, 400)
	cv2.imshow('Original', img)

	cv2.namedWindow('Equalized', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Equalized', 400, 400)
	cv2.imshow('Equalized', equalized)
	cv2.waitKey(0)

	return

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

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 400, 400)
	cv2.imshow('Original', img)

	cv2.namedWindow('Transformed', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Transformed', 400, 400)
	cv2.imshow('Transformed', transformed)
	cv2.waitKey(0)

	return

def gammaCorrection(filename):
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

	transformed = img / 255.0
	transformed = cv2.pow(transformed, 3)
	transformed = np.uint8(transformed*255)

	cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Original', 400, 400)
	cv2.imshow('Original', img)

	cv2.namedWindow('Transformed', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Transformed', 400, 400)
	cv2.imshow('Transformed', transformed)
	cv2.waitKey(0)

	return