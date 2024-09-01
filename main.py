import numpy as np
import cv2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from artifacts.artifact_pipeline import ArtifactPipeline
from artifacts.general.beam_hardening_artifact import BeamHardeningArtifact
from artifacts.general.metal_artifact import MetalArtifact
from artifacts.general.motion_artifcat import MotionArtifact
from artifacts.general.ring_artifact import RingArtifact
from disortion.barrel_disortion import BarrelDistortion
from disortion.warping_distortion import WarpingDistortion
from disortion.wave_distortion import WaveDistortion
from filter.blur.gaussian_blur import GaussianBlur
from filter.noise.noise_simulator import NoiseSimulator
from masks.object_mask import create_object_mask
from utils.image_utils import normalize_image, convert_to_rgb

def main():
    # Load and process image using OpenCV
    image_path = 'sample.jpeg'
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale

    if image is None:
        raise FileNotFoundError(f"The image file could not be loaded from {image_path}. Please check the file path and try again.")

    # Create a mask of the main object
    mask = create_object_mask(image)

    # Initialize the artifact pipeline with the image
    pipeline = ArtifactPipeline(image)

    # Add effects to the pipeline (artifacts and filters are treated the same)
    pipeline.add_effect(BeamHardeningArtifact(severity=1.0, streak_intensity=0.5, cupping_intensity=0.3))

    # Get the final image after applying all effects

    # Get the final image after applying all effects
    final_image = pipeline.get_final_image()
    final_image = mask * final_image + (1 - mask) * image  # Ensure the effect is only applied to the masked region

    # Normalize and convert to RGB for Plotly display
    image_rgb = convert_to_rgb(normalize_image(image))
    final_image_rgb = convert_to_rgb(normalize_image(final_image))

    # Create a subplot figure
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Original Image", "With Effects Applied"))

    # Add the images to the figure
    fig.add_trace(go.Image(z=image_rgb), row=1, col=1)
    fig.add_trace(go.Image(z=final_image_rgb), row=1, col=2)

    # Update layout to allow interaction
    fig.update_layout(height=600, width=1200, title_text="Medical Image with Effects Applied", showlegend=False)

    # Update axis to disable the axis labels and ticks
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Show the plot
    fig.show()

if __name__ == "__main__":
    main()
