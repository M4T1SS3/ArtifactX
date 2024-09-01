import numpy as np

from disortion.distortion import Distortion

class BarrelDistortion(Distortion):
    def __init__(self, severity=0.5):
        super().__init__(severity)

    def apply_effect(self, image):
        height, width = image.shape[:2]
        center_x, center_y = width // 2, height // 2

        new_image = np.zeros_like(image)
        for y in range(height):
            for x in range(width):
                # Normalize coordinates to the center
                normalized_x = (x - center_x) / width
                normalized_y = (y - center_y) / height

                # Apply barrel distortion formula
                r = np.sqrt(normalized_x**2 + normalized_y**2)
                theta = np.arctan2(normalized_y, normalized_x)
                r_distorted = r * (1 + self.severity * r**2)

                # Map back to image coordinates
                x_distorted = int(center_x + r_distorted * np.cos(theta) * width)
                y_distorted = int(center_y + r_distorted * np.sin(theta) * height)

                if 0 <= x_distorted < width and 0 <= y_distorted < height:
                    new_image[y, x] = image[y_distorted, x_distorted]

        return new_image
