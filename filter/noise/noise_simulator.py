# noise_simulator.py
import numpy as np

from filter.effect import Effect
from .gaussian_noise import add_gaussian_noise
from .salt_and_pepper_noise import add_salt_and_pepper_noise
from .poisson_noise import add_poisson_noise

class NoiseSimulator(Effect):
    def __init__(self, noise_type, intensity=0.5, mask=None):
        self.noise_type = noise_type
        self.intensity = intensity
        self.mask = mask

    def apply_effect(self, image):
        # Apply the chosen noise type
        if self.noise_type == 'gaussian':
            noisy_image = add_gaussian_noise(image, self.intensity)
        elif self.noise_type == 'salt_and_pepper':
            noisy_image = add_salt_and_pepper_noise(image, self.intensity)
        elif self.noise_type == 'poisson':
            noisy_image = add_poisson_noise(image, self.intensity)
        else:
            raise ValueError(f"Unsupported noise type: {self.noise_type}")

        # If a mask is provided, apply noise only to the masked areas
        if self.mask is not None:
            mask = np.clip(self.mask, 0, 1)  # Ensure mask is binary (0 or 1)
            final_image = image * (1 - mask) + noisy_image * mask
        else:
            final_image = noisy_image

        return final_image
