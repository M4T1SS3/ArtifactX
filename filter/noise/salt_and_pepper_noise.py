import numpy as np

def add_salt_and_pepper_noise(image, intensity=0.8):
    """
    Adds salt-and-pepper noise to an image with a continuous intensity level.

    Parameters:
    - image: Input image
    - intensity: Intensity of the noise (0.0 to 1.0)

    Returns:
    - Noisy image
    """
    base_salt_prob = 0.01 + (intensity * 0.02)  # Increase base probability
    base_pepper_prob = base_salt_prob

    image_normalized = image / 255.0
    noisy_image = np.copy(image_normalized)
    total_pixels = image.size

    adjustment_factor = 10000 / total_pixels
    salt_prob = base_salt_prob * adjustment_factor * 10  # Increase the effect of the adjustment factor
    pepper_prob = base_pepper_prob * adjustment_factor * 10

    num_salt = np.ceil(salt_prob * total_pixels).astype(int)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[tuple(coords)] = 1.0

    num_pepper = np.ceil(pepper_prob * total_pixels).astype(int)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[tuple(coords)] = 0.0

    return np.clip(noisy_image * 255.0, 0, 255).astype(np.uint8)
