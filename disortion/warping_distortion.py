import numpy as np
from artifacts.artifact import Artifact

class WarpingDistortion(Artifact):
    def __init__(self, warp_factor=0.5, severity=1.0):
        super().__init__(severity)
        self.warp_factor = warp_factor

    def apply_effect(self, image):
        # Get image dimensions
        h, w = image.shape[:2]

        # Create a mesh grid for pixel coordinates
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        # Apply a warping effect by modifying the mesh grid
        x_warp = x + self.warp_factor * np.sin(2 * np.pi * y / h)
        y_warp = y + self.warp_factor * np.sin(2 * np.pi * x / w)

        # Interpolate the pixel values at the new coordinates
        x_warp = np.clip(x_warp, 0, w - 1).astype(np.float32)
        y_warp = np.clip(y_warp, 0, h - 1).astype(np.float32)

        # Calculate the floor and ceiling of the coordinates
        x_floor = np.floor(x_warp).astype(np.int32)
        y_floor = np.floor(y_warp).astype(np.int32)
        x_ceil = np.ceil(x_warp).astype(np.int32)
        y_ceil = np.ceil(y_warp).astype(np.int32)

        # Calculate interpolation weights
        x_weight = x_warp - x_floor
        y_weight = y_warp - y_floor

        # Perform bilinear interpolation
        top_left = image[y_floor, x_floor]
        top_right = image[y_floor, x_ceil]
        bottom_left = image[y_ceil, x_floor]
        bottom_right = image[y_ceil, x_ceil]

        top = top_left * (1 - x_weight) + top_right * x_weight
        bottom = bottom_left * (1 - x_weight) + bottom_right * x_weight
        warped_image = top * (1 - y_weight) + bottom * y_weight

        # Apply severity to adjust the strength of the warping effect
        final_image = (1 - self.severity) * image + self.severity * warped_image
        return final_image
