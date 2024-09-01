import numpy as np
from artifacts.artifact import Artifact

class Distortion(Artifact):
    def __init__(self, severity=1.0):
        super().__init__(severity)

    def apply_effect(self, image):
        raise NotImplementedError("Subclasses must implement the `apply_effect` method.")
