import numpy as np
from scipy.ndimage import gaussian_filter

from artifacts.artifact import Artifact

class PartialVolumeArtifact(Artifact):
    def __init__(self, severity=1.0, blur_intensity=1.0):
        super().__init__(severity)
        self.blur_intensity = blur_intensity  # Controls how much the image is blurred to simulate the artifact

    def apply_effect(self, image):
        # Get image dimensions
        height, width = image.shape

        # Simulate partial volume effect by blurring specific regions of the image
        artifact_image = np.copy(image).astype(np.float32)

        # Generate a mask for regions to be blurred
        mask = np.random.rand(height, width) < (self.severity * 0.3)  # 30% of the area affected by artifact

        # Apply Gaussian blur to the masked regions
        blurred_image = gaussian_filter(artifact_image, sigma=self.blur_intensity * 5)

        # Combine the blurred regions with the original image
        artifact_image[mask] = blurred_image[mask]

        return np.clip(artifact_image, 0, 255).astype(np.uint8)

