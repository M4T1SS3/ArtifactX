import numpy as np

from disortion.distortion import Distortion

class WaveDistortion(Distortion):
    def __init__(self, amplitude=5, frequency=2, severity=1.0):
        super().__init__(severity)
        self.amplitude = amplitude * severity
        self.frequency = frequency * severity

    def apply_effect(self, image):
        height, width = image.shape[:2]
        new_image = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                # Apply wave distortion formula
                x_offset = int(self.amplitude * np.sin(2 * np.pi * y / self.frequency))
                y_offset = int(self.amplitude * np.sin(2 * np.pi * x / self.frequency))

                # Map coordinates with wave distortion
                x_distorted = x + x_offset
                y_distorted = y + y_offset

                if 0 <= x_distorted < width and 0 <= y_distorted < height:
                    new_image[y, x] = image[y_distorted, x_distorted]

        return new_image
