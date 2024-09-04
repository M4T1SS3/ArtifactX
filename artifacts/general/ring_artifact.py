import numpy as np
import cv2
from artifacts.artifact import Artifact

class RingArtifact(Artifact):
    def __init__(self, severity=1.0, ring_count=5, intensity=0.5, noise_factor=0.02, blur_sigma=1.0, random_center=False, center_offset_range=0.1):
        super().__init__(severity)
        self.ring_count = ring_count  # Number of rings
        self.intensity = intensity  # Intensity of the rings
        self.noise_factor = noise_factor  # Factor for introducing randomness in ring boundaries
        self.blur_sigma = blur_sigma  # Sigma for Gaussian blur to simulate imperfections
        self.random_center = random_center  # Flag to enable random ring center
        self.center_offset_range = center_offset_range  # Max offset for random center (percentage of image size)

    def apply_effect(self, image):
        # Get image dimensions
        height, width = image.shape
        
        # Define a tighter range for center placement
        offset_boundary = 0.3  # Center should stay within 30% of the object region in both directions
        
        if self.random_center:
            # Randomize the center within a more controlled boundary closer to the center of the object
            center_x = int(width // 2 + np.random.uniform(-offset_boundary * width, offset_boundary * width))
            center_y = int(height // 2 + np.random.uniform(-offset_boundary * height, offset_boundary * height))
        else:
            center_x, center_y = width // 2, height // 2
        
        # Create an empty artifact image
        artifact_image = np.zeros_like(image, dtype=np.float32)
        
        max_radius = np.sqrt(center_x**2 + center_y**2)
        
        for i in range(1, self.ring_count + 1):
            radius = (i / self.ring_count) * max_radius
            
            # Random variation in ring intensity and thickness
            ring_intensity = self.intensity * np.random.uniform(0.8, 1.2)
            ring_thickness = np.random.uniform(0.5, 1.5) * self.severity

            for y in range(height):
                for x in range(width):
                    distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    
                    # Add noise to the radius
                    radius_with_noise = radius + np.random.uniform(-self.noise_factor * radius, self.noise_factor * radius)
                    
                    # Create a ring by applying a Gaussian function with random thickness
                    ring_value = np.exp(-((distance_from_center - radius_with_noise)**2) / (2 * (ring_thickness**2)))
                    artifact_image[y, x] += ring_intensity * ring_value

        # Normalize the artifact image and apply blur
        artifact_image = np.clip(artifact_image, 0, 1)
        artifact_image = cv2.GaussianBlur(artifact_image, (0, 0), self.blur_sigma)

        # Combine the artifact with the original image
        final_image = (1 - artifact_image) * image + artifact_image * 255
        
        return np.clip(final_image, 0, 255).astype(np.uint8)
