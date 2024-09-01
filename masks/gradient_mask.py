import numpy as np
from .mask import Mask

class GradientMask(Mask):
    def __init__(self, image, gradient_type='linear', direction='horizontal', num_shapes=1):
        super().__init__(image, num_shapes)
        self.gradient_type = gradient_type
        self.direction = direction

    def apply_mask(self):
        mask = np.zeros_like(self.image, dtype=float)
        
        for _ in range(self.num_shapes):
            if self.gradient_type == 'linear':
                if self.direction == 'horizontal':
                    for i in range(self.width):
                        mask[:, i] = i / self.width
                elif self.direction == 'vertical':
                    for i in range(self.height):
                        mask[i, :] = i / self.height

            elif self.gradient_type == 'radial':
                # Randomly select a center for the radial gradient
                center_x = np.random.randint(self.width)
                center_y = np.random.randint(self.height)
                center = (center_x, center_y)
                max_distance = np.sqrt(center[0]**2 + center[1]**2)
                for y in range(self.height):
                    for x in range(self.width):
                        distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
                        mask[y, x] = distance / max_distance

        return mask
