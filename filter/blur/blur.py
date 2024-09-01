from filter.effect import Effect

class Blur(Effect):
    def __init__(self, severity=1.0):
        self.severity = severity  # General severity level, 1.0 is default
        self.image = None
        self.height = None
        self.width = None

    def apply_effect(self, image):
        self.image = image
        self.height, self.width = image.shape  # Set height and width based on the input image
        return self._apply_blur_logic(image)

    def _apply_blur_logic(self, image):
        # Subclasses should override this method to implement specific blur logic
        raise NotImplementedError("Subclasses must implement this method.")

    def adjust_severity(self, factor):
        """Method to adjust severity based on modality or user settings."""
        self.severity *= factor
