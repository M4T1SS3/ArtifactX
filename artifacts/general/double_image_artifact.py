import numpy as np
from artifacts.artifact import Artifact

class DoubleImageArtifact(Artifact):
    def __init__(self, shift_amount=5, intensity=0.5):
        super().__init__()
        self.shift_amount = shift_amount
        self.intensity = intensity

    def apply_effect(self, image):
        # Shift the image to create a double image effect
        shifted_image = np.roll(image, shift=self.shift_amount, axis=1)  # Horizontal shift
        shifted_image[:, :self.shift_amount] = 0  # Clear the wrapping around the edges

        # Blend the original and shifted images
        double_image = (1 - self.intensity) * image + self.intensity * shifted_image

        return double_image
