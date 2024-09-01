import numpy as np

from masks.mask import Mask

class SphericalMask(Mask):
    def __init__(self, image, intensity_range=(0.5, 1.0), num_shapes=1, relative_size=None):
        super().__init__(image, num_shapes, relative_size)
        self.intensity_range = intensity_range

    def apply_mask(self):
        mask = np.zeros_like(self.image, dtype=float)
        for _ in range(self.num_shapes):
            mask_size = self.get_random_size()  # Size relative to the image dimensions
            intensity = np.random.uniform(self.intensity_range[0], self.intensity_range[1])
            center_x = np.random.randint(mask_size, self.width - mask_size)
            center_y = np.random.randint(mask_size, self.height - mask_size)

            for x in range(self.width):
                for y in range(self.height):
                    distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                    if distance < mask_size:
                        mask[y, x] = intensity

        return mask
