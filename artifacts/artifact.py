import numpy as np

class Artifact:
    def __init__(self, severity=1.0):
        self.severity = severity  # General severity level, 1.0 is default
        self.height = None
        self.width = None

    def apply_artifact(self, image):
        self.image = image
        self.height, self.width = image.shape  # Set height and width based on the input image
        return self._apply(image)

    def _apply(self, image):
        raise NotImplementedError("Subclasses must implement this method.")

    def adjust_severity(self, factor):
        """Method to adjust severity based on modality or user settings."""
        self.severity *= factor
