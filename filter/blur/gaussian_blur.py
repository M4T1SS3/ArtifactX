import numpy as np
from filter.blur.blur import Blur

import numpy as np
from filter.blur.blur import Blur

class GaussianBlur(Blur):
    def __init__(self, severity=1.0, kernel_size=None):
        super().__init__(severity=severity)  # Initialize the parent class with severity
        if kernel_size is None:
            # Determine kernel size based on severity if not provided
            self.kernel_size = int(5 * self.severity)
            if self.kernel_size % 2 == 0:
                self.kernel_size += 1  # Kernel size must be odd
        else:
            self.kernel_size = kernel_size

    def apply_effect(self, image):
        kernel = self._create_gaussian_kernel(self.kernel_size, self.severity)
        return self._apply_convolution(image, kernel)


    def apply_effect(self, image):
        # The effect application logic remains the same
        kernel = self._create_gaussian_kernel(self.kernel_size, self.severity)
        return self._apply_convolution(image, kernel)


    def _apply_blur_logic(self, image):
        kernel = self._create_gaussian_kernel(self.kernel_size, self.severity)
        return self._apply_convolution(image, kernel)

    def _create_gaussian_kernel(self, size, sigma):
        """Creates a Gaussian kernel."""
        ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
        return kernel / np.sum(kernel)

    def _apply_convolution(self, image, kernel):
        """Applies convolution between the image and the kernel."""
        image_padded = np.pad(image, ((self.kernel_size // 2, self.kernel_size // 2),
                                      (self.kernel_size // 2, self.kernel_size // 2)),
                              mode='constant')
        output_image = np.zeros_like(image)

        for x in range(image.shape[1]):  # Loop over every pixel of the image
            for y in range(image.shape[0]):
                # Element-wise multiplication and sum the result
                output_image[y, x] = (kernel * image_padded[y:y + self.kernel_size, x:x + self.kernel_size]).sum()

        return output_image
