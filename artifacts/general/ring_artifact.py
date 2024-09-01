import numpy as np

from artifacts.artifact import Artifact

class RingArtifact(Artifact):
    def __init__(self, severity=1.0, ring_count=5, intensity=0.5):
        super().__init__(severity)
        self.ring_count = ring_count  # Number of rings to simulate
        self.intensity = intensity  # Intensity of the ring artifact

    def apply_effect(self, image):
        # Get image dimensions directly from the image passed to the method
        height, width = image.shape
        
        # Generate the center of the image
        center_x, center_y = width // 2, height // 2
        
        # Create an empty artifact image
        artifact_image = np.zeros_like(image, dtype=np.float32)
        
        # Determine the maximum radius (from the center to the furthest corner)
        max_radius = np.sqrt(center_x**2 + center_y**2)
        
        # Generate ring artifact patterns
        for i in range(1, self.ring_count + 1):
            radius = (i / self.ring_count) * max_radius
            for y in range(height):
                for x in range(width):
                    distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    # Avoid numerical issues by setting a minimum value for severity
                    safe_severity = max(self.severity, 1e-10)
                    # Create a ring by applying a Gaussian function around the radius
                    ring_value = np.exp(-((distance_from_center - radius)**2) / (2 * (safe_severity**2)))
                    artifact_image[y, x] += self.intensity * ring_value

        # Normalize the artifact image to ensure the effect stays within bounds
        artifact_image = np.clip(artifact_image, 0, 1)

        # Combine the artifact with the original image
        final_image = (1 - artifact_image) * image + artifact_image * 255
        
        return np.clip(final_image, 0, 255).astype(np.uint8)
