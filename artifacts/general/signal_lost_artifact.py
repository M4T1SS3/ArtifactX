import numpy as np
from artifacts.artifact import Artifact

class SignalLossArtifact(Artifact):
    def __init__(self, signal_loss_factor=0.1):
        super().__init__()
        self.signal_loss_factor = signal_loss_factor

    def apply_effect(self, image):
        signal_loss_mask = np.random.rand(*image.shape) < self.signal_loss_factor
        signal_lost_image = np.where(signal_loss_mask, image * 0.5, image)
        return signal_lost_image
