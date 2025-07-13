import cv2
import numpy as np

## GreyScale
def greyscale(img):
    img = cv2.imread(img)
    grey_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return grey_img

## Brightness Adjustment
def bright(img,val):
    img = cv2.imread(img)
    bright_img = cv2.convertScaleAbs(img,beta=val)
    return bright_img

## Sharp
def sharp(img):
    img = cv2.imread(img,flags=cv2.IMREAD_COLOR)
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharp_img = cv2.filter2D(img,ddepth=-1,kernel=kernel)
    return sharp_img

## Sepia
def sepia(img):
    img = cv2.imread(img)
    sepia_img = np.array(img,dtype=np.float64)
    sepia_img = cv2.transform(sepia_img,np.matrix([[0.272,0.534,0.131],
                                                   [0.349,0.686,0.168],
                                                   [0.393,0.769,0.189]]))
    sepia_img[np.where(sepia_img>255)] = 255
    sepia_img = np.array(sepia_img,dtype=np.uint8)
    return sepia_img

## HDR Effect
def HDR(img,sig_s,sig_r):
    img = cv2.imread(img)
    hdr_img = cv2.detailEnhance(img,sigma_s=sig_s,sigma_r=sig_r)
    return hdr_img

## Invert
def invert(img):
    img = cv2.imread(img)
    invert_img = cv2.bitwise_not(img)
    return invert_img

## Blur
def blur(img,kernel):
    img = cv2.imread(img)
    blur_img = cv2.blur(img,ksize=(kernel,kernel))
    return blur_img

## Stylization
def style(img,sig_s,sig_r):
    img = cv2.imread(img)
    style_img = cv2.GaussianBlur(img,(3,3),0,0)
    style_img = cv2.stylization(style_img,sigma_s=sig_s,sigma_r=sig_r)
    return style_img

## Sketch
def sketch(img,value):
    # Ensure value is odd and > 0
    if value % 2 == 0:
        value += 1
    if value <= 0:
        value = 3  # default fallback
    img = cv2.imread(img)
    gray_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_invert = 255-gray_img
    img_smoothing = cv2.GaussianBlur(img_invert, (value, value),0)
    inblur_img = 255-img_smoothing
    sketch_img = cv2.divide(gray_img,inblur_img,scale=256.0)
    return sketch_img

## Cartoonify
def cartoon(img):
    img = cv2.imread(img)
    originalmage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
      cv2.ADAPTIVE_THRESH_MEAN_C, 
      cv2.THRESH_BINARY, 9, 9)
    colorImage = cv2.bilateralFilter(originalmage, 9, 250, 250)
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    return cartoonImage

## Textured
def textured(img,s,r):
    img = cv2.imread(img,cv2.COLOR_BGR2RGB)
    sharp_img = cv2.detailEnhance(img,sigma_s=40,sigma_r=0.8)
    tex_gray,tex_color = cv2.pencilSketch(sharp_img, sigma_s=s, sigma_r=r, shade_factor=0.02)
    return tex_color
