import numpy as np
from artifacts.artifact import Artifact
from filter.blur.gaussian_blur import GaussianBlur

class EdgeDeformationArtifact(Artifact):
    def __init__(self, edge_deformation_factor=0.2):
        super().__init__()
        self.edge_deformation_factor = edge_deformation_factor

    def apply_effect(self, image):
        # Apply Gaussian blur
        blur = GaussianBlur(severity=self.edge_deformation_factor * 10)
        blurred_image = blur.apply_effect(image)
        
        # Create a random deformation mask based on the edge deformation factor
        deformation_mask = np.random.rand(*image.shape) < self.edge_deformation_factor
        
        # Apply the mask to the image
        deformed_image = np.where(deformation_mask, blurred_image, image)
        
        return deformed_image
