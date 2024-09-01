import numpy as np
from artifacts.artifact import Artifact
from .ghosting_artifact import GhostingArtifact
from .edge_deformation_artifact import EdgeDeformationArtifact
from .signal_lost_artifact import SignalLossArtifact

class MotionArtifact(Artifact):
    def __init__(self, motion_strength=5, ghosting_factor=0.2, edge_deformation_factor=0.2, signal_loss_factor=0.1):
        super().__init__(severity=1.0)
        self.motion_strength = motion_strength
        self.ghosting_factor = ghosting_factor
        self.edge_deformation_factor = edge_deformation_factor
        self.signal_loss_factor = signal_loss_factor

    def apply_effect(self, image):
        self.height, self.width = image.shape  # Update dimensions based on the image
        
        # Apply motion blur
        motion_blurred_image = self.apply_motion_blur(image)

        # Apply ghosting
        ghosting_artifact = GhostingArtifact(self.ghosting_factor)
        ghosted_image = ghosting_artifact.apply_effect(motion_blurred_image)

        # Apply edge deformation
        edge_deformation_artifact = EdgeDeformationArtifact(self.edge_deformation_factor)
        deformed_image = edge_deformation_artifact.apply_effect(ghosted_image)

        # Apply signal loss
        signal_loss_artifact = SignalLossArtifact(self.signal_loss_factor)
        final_image = signal_loss_artifact.apply_effect(deformed_image)

        return final_image

    def apply_motion_blur(self, image):
        kernel_size = self.motion_strength
        kernel = np.zeros((self.height, self.width))

        center = self.width // 2
        half_kernel = kernel_size // 2

        # Create a horizontal motion blur kernel
        for i in range(max(0, center - half_kernel), min(self.width, center + half_kernel)):
            kernel[:, i] = 1 / kernel_size

        # Apply the kernel by convolving it with the image
        motion_blurred_image = np.copy(image)
        for i in range(self.height):
            motion_blurred_image[i, :] = np.convolve(image[i, :], kernel[i, :], mode='same')

        return motion_blurred_image
