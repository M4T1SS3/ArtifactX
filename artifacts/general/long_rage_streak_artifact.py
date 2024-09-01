import numpy as np
from scipy.ndimage import sobel
from artifacts.artifact import Artifact

class LongRangeStreakArtifact(Artifact):
    def __init__(self, streak_intensity=0.3):
        super().__init__()
        self.streak_intensity = streak_intensity

    def apply_effect(self, image):
        # Detect edges using a Sobel filter
        edges = sobel(image)

        # Find coordinates of strong edges
        edge_coords = np.argwhere(edges > edges.mean() + edges.std())

        # Create an empty image for the streaks
        streak_image = np.zeros_like(image)

        # Simulate streaks by drawing lines across the image
        for coord in edge_coords:
            y, x = coord
            streak_image[y, :] = self.streak_intensity  # Horizontal streaks
            streak_image[:, x] = self.streak_intensity  # Vertical streaks

        # Combine the original image with the streak image
        streaked_image = np.clip(image + streak_image, 0, 1)

        return streaked_image
