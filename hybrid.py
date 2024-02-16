import sys
import cv2
import numpy as np

def cross_correlation_2d(img, kernel):
    
    '''Given a kernel of arbitrary m x n dimensions, with both m and n being
    odd, compute the cross correlation of the given image with the given
    kernel, such that the output is of the same dimensions as the image and that
    you assume the pixels out of the bounds of the image to be zero. Note that
    you need to apply the kernel to each channel separately, if the given image
    is an RGB image.

    Inputs:
        img:    Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
        kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
                equal).
    '''

    height, width = img.shape[:2]
    if len(img.shape) == 3:
        num_channels = img.shape[2]
    else:
        num_channels = 1


    # Get kernel dimensions
    kernel_height, kernel_width = kernel.shape

    # Calculate padding
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Pad the image
    padded_img = np.pad(img, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='constant')

    # Initialize output image
    output_img = np.zeros_like(img)

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Apply the kernel to each channel separately
            for c in range(num_channels):
                # Compute the cross correlation
                output_img[y, x, c] = np.sum(padded_img[y:y+kernel_height, x:x+kernel_width, c] * kernel)

    return output_img
    '''

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''

def convolve_2d(img, kernel):
    '''Use cross_correlation_2d() to carry out a 2D convolution.

    Inputs:
    img:    Either an RGB image (height x width x 3) or a grayscale image
        (height x width) as a numpy array.
    kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
        equal).
    '''
    return cross_correlation_2d(img, kernel[::-1, ::-1])

    '''
    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''


def gaussian_blur_kernel_2d(sigma, height, width):
    '''Return a Gaussian blur kernel of the given dimensions and with the given
    sigma. Note that width and height are different.

    Input:
        sigma:  The parameter that controls the radius of the Gaussian blur.
                Note that, in our case, it is a circular Gaussian (symmetric
                across height and width).
        width:  The width of the kernel.
        height: The height of the kernel.

    '''
    gauss_kernel = np.zeros((height, width))
    h = np.linspace(-height / 2 + 1, height / 2, height)
    w = np.linspace(-width / 2 + 1, width / 2, width)

    for x, x1 in enumerate(h):
        for y, y1 in enumerate(w):
            gauss_kernel[x,y] = 1 / (2 * np.pi * (sigma ** 2)) * np.exp(-(x1 ** 2 + y1 ** 2)/(2 * (sigma ** 2)))
    
    norm_gauss = gauss_kernel * 1 / np.sum(gauss_kernel)
    
    return norm_gauss

    '''

    Output:
        Return a kernel of dimensions height x width such that convolving it
        with an image results in a Gaussian-blurred image.
    '''



def low_pass(img, sigma, size):
    '''Filter the image as if its filtered with a low pass filter of the given
    sigma and a square kernel of the given size. A low pass filter supresses
    the higher frequency components (finer details) of the image.
    '''
    return convolve_2d(img, gaussian_blur_kernel_2d(sigma, size, size))
    '''
    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''


def high_pass(img, sigma, size):
    '''Filter the image as if its filtered with a high pass filter of the given
    sigma and a square kernel of the given size. A high pass filter suppresses
    the lower frequency components (coarse details) of the image.
    '''
    return img - low_pass(img, sigma, size)

    '''
    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''

def create_hybrid_image(img1, img2, sigma1, size1, high_low1, sigma2, size2,
        high_low2, mixin_ratio, scale_factor):
    '''This function adds two images to create a hybrid image, based on
    parameters specified by the user.'''
    high_low1 = high_low1.lower()
    high_low2 = high_low2.lower()

    if img1.dtype == np.uint8:
        img1 = img1.astype(np.float32) / 255.0
        img2 = img2.astype(np.float32) / 255.0

    if high_low1 == 'low':
        img1 = low_pass(img1, sigma1, size1)
    else:
        img1 = high_pass(img1, sigma1, size1)

    if high_low2 == 'low':
        img2 = low_pass(img2, sigma2, size2)
    else:
        img2 = high_pass(img2, sigma2, size2)

    img1 *=  (1 - mixin_ratio)
    img2 *= mixin_ratio
    hybrid_img = (img1 + img2) * scale_factor
    return (hybrid_img * 255).clip(0, 255).astype(np.uint8)

