import cv2
import numpy as np

def normalize_image(image):
    """Normalize image to be in the range [0, 255] and convert to uint8."""
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image.astype(np.uint8)

def convert_to_rgb(image):
    """Convert grayscale image to RGB by stacking the channels."""
    return np.stack((image,) * 3, axis=-1)
