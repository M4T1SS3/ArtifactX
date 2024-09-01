import numpy as np

def add_gaussian_noise(image, intensity=0.5):
    """
    Adds Gaussian noise to an image with a continuous intensity level.

    Parameters:
    - image: Input image
    - intensity: Intensity of the noise (0.0 to 1.0)

    Returns:
    - Noisy image
    """
    stddev = 0.05 + (intensity * 0.15)  # Map intensity to stddev range

    image_normalized = image / 255.0
    gaussian_noise = np.random.normal(0, stddev, image.shape)
    noisy_image = image_normalized + gaussian_noise
    return np.clip(noisy_image * 255.0, 0, 255).astype(np.uint8)
