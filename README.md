/**
# Augmentation Tool

## Purpose:
The Medical Imaging Artifact Simulation and Augmentation Tool is designed to help researchers, developers, and clinicians simulate various artifacts commonly found in medical imaging. These artifacts, such as noise, motion blur, metal artifacts, beam hardening, and partial volume effects, are critical to study because they can significantly impact the performance of diagnostic tools and machine learning models.

## Goals:
- Facilitate Research: Enable medical imaging researchers to create synthetic datasets with realistic artifacts for testing and validation.
- Enhance Machine Learning Models: Provide tools to augment training datasets with realistic artifacts, improving the robustness and generalizability of models.
- Support Clinical Understanding: Help radiologists and clinicians better understand how different artifacts affect imaging quality and diagnosis.
- Aid in Software Development: Assist developers in testing the resilience of medical imaging software and diagnostic tools against common imaging artifacts.

## Implemented Artifacts
This tool simulates various artifacts commonly found in medical imaging. These artifacts can significantly impact image quality and diagnostic accuracy, making them important to study and understand. Below is a description of each type of artifact available in the tool:

1. Beam Hardening Artifact
    - Description: Simulates beam hardening artifacts, which occur when low-energy X-ray photons are absorbed more than high-energy photons as they pass through dense materials like bone or metal. This results in streaks or dark bands around high-density areas.

2. Double Image Artifact
    - Description: Simulates double image artifacts, typically caused by misalignment or shifting during image acquisition. This results in a duplication or ghosting effect where structures in the image appear multiple times in slightly different locations.

3. Edge Deformation Artifact
    - Description: Simulates edge deformation artifacts, which are distortions that occur near the edges of an image. These can be caused by imperfections in the imaging system or errors in the image reconstruction process.

4. Ghosting Artifact
    - Description: Simulates ghosting artifacts, which occur due to patient movement or system instability during imaging. These artifacts result in the appearance of multiple, overlapping copies of structures in the image.

5. Long Range Streak Artifact
    - Description: Simulates long range streak artifacts, which appear as long, linear streaks across the image. These are often caused by errors in the imaging system or external factors that disrupt the imaging process.

6. Masked Noise Artifact
    - Description: Simulates masked noise artifacts, where noise is selectively applied to specific regions of the image. This technique is often used to simulate the effect of noise in medical images while preserving certain critical areas.

7. Metal Artifact
    - Description: Simulates metal artifacts, which occur when metal objects such as implants are present in the body. The high density of metal causes streaks and distortions in the image, making it difficult to accurately visualize surrounding tissues.

8. Motion Artifact
    - Description: Simulates motion artifacts, which result from patient movement during the imaging process. These artifacts typically manifest as blurred or distorted images, making it challenging to accurately interpret the scan.

9. Partial Volume Artifact
    - Description: Simulates partial volume artifacts, which occur when a single voxel (3D pixel) contains tissues of different densities. This leads to averaging effects that cause blurring or incorrect representation of tissue boundaries in the image.

10. Ring Artifact
     - Description: Simulates ring artifacts, which typically appear as concentric rings in the image. These artifacts are usually caused by calibration errors or defects in the detector of the imaging device.

11. Signal Loss Artifact
     - Description: Simulates signal loss artifacts, which occur when there is a sudden loss of signal during image acquisition. This results in areas of the image appearing as blank or black regions where no data was captured.

12. Streak Artifact
     - Description: Simulates streak artifacts, which can be caused by various factors such as the presence of metal, beam hardening, or photon starvation. These artifacts manifest as bright or dark streaks that radiate across the image, obscuring the underlying anatomy.

## Implemented Filters
This tool includes various filters that can be applied to medical images to simulate different effects and conditions. Below is a description of each type of filter available in the tool, categorized into Noise Filters and Blur Filters.

### Noise Filters
Noise filters are used to simulate various types of random noise that can occur during the medical imaging process. These filters are valuable for testing the robustness of image processing algorithms and simulating real-world imaging conditions.

1. Gaussian Noise
    - Description: The Gaussian Noise filter adds random noise to the image following a Gaussian (normal) distribution. This type of noise is typically used to simulate the natural variability in imaging systems, particularly in low-light or low-signal conditions.

2. Poisson Noise
    - Description: The Poisson Noise filter simulates noise that follows a Poisson distribution, which is commonly associated with photon counting processes in imaging techniques such as X-ray or PET scans. This noise type is useful for modeling the stochastic nature of radiation-based imaging.

3. Salt-and-Pepper Noise
    - Description: The Salt-and-Pepper Noise filter introduces random white and black pixels into the image, simulating the effect of sudden and extreme noise. This type of noise is often used to test the robustness of image processing algorithms, as it represents a severe form of corruption in the image data.

4. Noise Simulator
    - Description: The Noise Simulator provides a versatile tool for applying a combination of different noise types to an image. Users can select and customize the level of Gaussian, Poisson, or Salt-and-Pepper noise to create complex noise patterns that mimic real-world conditions in medical imaging.

### Blur Filters
Blur filters are used to reduce detail and soften images, simulating effects like out-of-focus imaging or motion blur. These filters are particularly useful in preparing data for certain types of analysis or in simulating the impact of various imaging conditions.

1. Gaussian Blur
    - Description: The Gaussian Blur filter applies a smoothing effect to the image by convolving it with a Gaussian function. This filter is commonly used to reduce noise and detail, creating a softening effect. It is also useful for simulating the blurring that can occur due to motion or out-of-focus imaging.

## Implemented Masks
Masks in this tool are used to define areas or shapes where filters and artifacts will be applied. By using masks, you can control how and where an effect is introduced in the image, allowing for more realistic and targeted simulations.

1. Organic Shape Mask
    - Description: The Organic Shape Mask allows for the creation of irregular, natural-looking shapes within the image. This mask is particularly useful when you want to apply filters or artifacts to regions that do not follow simple geometric patterns, such as simulating tissue irregularities or lesions.

2. Polygonal Mask
    - Description: The Polygonal Mask creates a mask based on user-defined polygonal shapes. This mask is ideal for targeting specific, well-defined areas of the image, such as applying artifacts to a specific organ or section of tissue that has a clear boundary.

3. Spherical Mask
    - Description: The Spherical Mask generates a spherical region within the image. This is useful for applying effects to round or oval-shaped structures, such as tumors or other spherical anatomical features, ensuring that the filter or artifact is applied uniformly within the spherical area.

4. Gradient Mask
    - Description: The Gradient Mask applies a gradient effect to the mask, creating a smooth transition between the masked and unmasked areas. This is useful for applying filters gradually across the image, simulating effects like gradual blurring or fading that can occur naturally in medical imaging.

5. Object Mask
    - Description: The Object Mask is used to create a mask around a specific object or area of interest within the image. This mask is typically generated based on the characteristics of the object (such as intensity or shape) and is used to target filters or artifacts to that object specifically, leaving the rest of the image unaffected.

6. Mask
    - Description: The general Mask class provides the foundational structure for creating custom masks. It can be extended or customized to create specific masking patterns as needed. This class allows for flexibility in defining how and where effects should be applied within the image.# ArtifactX
