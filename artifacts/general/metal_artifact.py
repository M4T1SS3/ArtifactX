import numpy as np
import cv2
from artifacts.artifact import Artifact

class MetalArtifact(Artifact):
    def __init__(self, streak_intensity=10, streak_count=20, severity=1.0, centroids=1, base_gap=5, skip_probability=0.2, object_radius=20):
        super().__init__(severity)  # Initialize with severity
        self.streak_intensity = streak_intensity * self.severity
        self.streak_count = int(streak_count * self.severity)
        self.centroids = centroids
        self.base_gap = base_gap  # Skip every 'n' lines (an integer)
        self.skip_probability = skip_probability  # Probability to skip a line
        self.object_radius = object_radius  # Radius of the white round object

    def apply_effect(self, image):
        """
        Apply the metal artifact to the image using NumPy operations.

        Parameters:
        - image: np.ndarray, the input image on which artifacts are applied.

        Returns:
        - np.ndarray, the image with metal artifacts applied.
        """
        height, width = image.shape  # Update dimensions based on the image
        
        image_with_artifacts = image.copy()
        h, w = image_with_artifacts.shape

        # Generate random centroids
        centroid_positions = [(np.random.randint(0, w), np.random.randint(0, h)) for _ in range(self.centroids)]

        for i in range(self.streak_count):
            # Apply base gap logic (skip every 'base_gap' lines)
            if self.base_gap > 0 and i % self.base_gap == 0:
                continue  # Skip this line

            # Apply additional random skipping based on the probability
            if np.random.rand() < self.skip_probability:
                continue  # Randomly skip this line based on probability

            for cx, cy in centroid_positions:
                angle = (i * 2 * np.pi / self.streak_count) + np.random.uniform(-np.pi / 100, np.pi / 100)

                # Define the end point of the streak based on the angle
                length = max(h, w)  # Make sure the streak can span the entire image
                x2 = int(cx + length * np.cos(angle))
                y2 = int(cy + length * np.sin(angle))

                # Generate coordinates for the line (streak)
                rr, cc = self._line_coords(cx, cy, x2, y2, h, w)

                # Apply the streak directly
                image_with_artifacts[rr, cc] = np.clip(image_with_artifacts[rr, cc] + self.streak_intensity, 0, 255)

        # Draw the white round object at the centroid
        for cx, cy in centroid_positions:
            cv2.circle(image_with_artifacts, (cx, cy), self.object_radius, (255, 255, 255), -1)  # Draw filled circle

        # Blend the artifact with the original image
        alpha = 0.8  # Blending factor for visibility
        final_image = (alpha * image_with_artifacts + (1 - alpha) * image).astype(np.uint8)

        return final_image

    def _line_coords(self, x1, y1, x2, y2, h, w):
        """Generate the coordinates for a line using Bresenham's algorithm."""
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        rr, cc = [], []
        while True:
            if 0 <= x1 < w and 0 <= y1 < h:
                rr.append(y1)
                cc.append(x1)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return np.array(rr), np.array(cc)
