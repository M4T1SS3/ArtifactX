import numpy as np
from artifacts.artifact import Artifact

class GhostingArtifact(Artifact):
    def __init__(self, ghosting_factor=0.2):
        super().__init__()
        self.ghosting_factor = ghosting_factor

    def apply_effect(self, image):
        shift_amount = int(self.ghosting_factor * image.shape[1])
        ghosted_image = image + np.roll(image, shift_amount, axis=1) * 0.5
        return np.clip(ghosted_image, 0, 255)
