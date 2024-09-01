import numpy as np
from artifacts.artifact import Artifact
from filter.noise.noise_simulator import NoiseSimulator

class MaskedNoiseArtifact(Artifact):
    def __init__(self, mask, noise_type='gaussian', intensity=0.5):
        super().__init__()
        self.mask = mask
        self.noise_type = noise_type
        self.intensity = intensity
        self.noise_simulator = NoiseSimulator()

    def apply_effect(self, image):
        # Apply noise using the mask
        final_image = self.noise_simulator.apply_noise(image, self.noise_type, self.intensity, self.mask)

        return final_image
