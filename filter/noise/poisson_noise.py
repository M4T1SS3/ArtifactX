import numpy as np

def add_poisson_noise(image, intensity=0.5):
    """
    Adds Poisson noise to an image with a continuous intensity level.

    Parameters:
    - image: Input image
    - intensity: Intensity of the noise (0.0 to 1.0)

    Returns:
    - Noisy image
    """
    factor = 0.5 + (intensity * 1.5)  # Map intensity to a scaling factor

    image_normalized = image / 255.0 * factor
    noisy_image = np.random.poisson(image_normalized * 255.0) / 255.0
    return np.clip(noisy_image * 255.0, 0, 255).astype(np.uint8)
