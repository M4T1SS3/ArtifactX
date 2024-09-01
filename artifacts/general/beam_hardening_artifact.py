import numpy as np
from scipy.ndimage import gaussian_filter

from artifacts.artifact import Artifact

class BeamHardeningArtifact(Artifact):
    def __init__(self, severity=1.0, streak_intensity=0.5, cupping_intensity=0.5):
        super().__init__(severity)
        self.streak_intensity = streak_intensity  # Intensity of the streak artifacts
        self.cupping_intensity = cupping_intensity  # Intensity of the cupping artifacts

    def apply_effect(self, image):
        # Get image dimensions
        height, width = image.shape
        
        # Simulate dense objects by selecting bright regions in the image
        dense_mask = image > (image.mean() + image.std())
        
        # Create streak artifacts
        streak_image = np.zeros_like(image, dtype=np.float32)

        # Introduce streaks between dense regions
        for i in range(height):
            for j in range(width):
                if dense_mask[i, j]:
                    # Create streaks horizontally
                    streak_image[i, :] += self.streak_intensity * dense_mask[i, j]
                    # Create streaks vertically
                    streak_image[:, j] += self.streak_intensity * dense_mask[i, j]

        # Apply Gaussian blur to smooth streaks
        streak_image = gaussian_filter(streak_image, sigma=5)
        
        # Apply cupping artifact by darkening the center relative to the edges
        cupping_image = np.zeros_like(image, dtype=np.float32)
        center_x, center_y = width // 2, height // 2
        max_distance = np.sqrt(center_x**2 + center_y**2)

        for y in range(height):
            for x in range(width):
                distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                # Cupping effect stronger towards the center
                cupping_image[y, x] = self.cupping_intensity * (1 - distance_from_center / max_distance)

        # Normalize cupping effect to the image intensity
        cupping_image *= image.max()

        # Combine the artifacts with the original image
        artifact_image = np.clip(image + streak_image - cupping_image, 0, 255)

        return artifact_image.astype(np.uint8)

