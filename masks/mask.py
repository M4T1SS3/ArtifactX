import numpy as np

class Mask:
    def __init__(self, image, num_shapes=1, relative_size=None):
        self.image = image
        self.height, self.width = image.shape
        self.num_shapes = num_shapes
        self.relative_size = relative_size if relative_size else (0.02, 0.05)  # Smaller default size range

    def apply_mask(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def add_masks(self, *masks):
        combined_mask = np.zeros_like(self.image, dtype=float)
        for mask in masks:
            combined_mask = np.clip(combined_mask + mask, 0, 1)
        return combined_mask

    def multiply_masks(self, *masks):
        combined_mask = np.ones_like(self.image, dtype=float)
        for mask in masks:
            combined_mask = combined_mask * mask
        return combined_mask

    def get_random_size(self):
        min_size_ratio, max_size_ratio = self.relative_size
        min_size = int(min(self.height, self.width) * min_size_ratio)
        max_size = int(min(self.height, self.width) * max_size_ratio)
        # Enforce a minimum size to avoid very tiny shapes
        min_size = max(5, min_size)
        max_size = max(min_size + 1, max_size)
        return np.random.randint(min_size, max_size)

    def adjust_shape_to_bounds(self, vertices):
        """
        Ensures that the generated shape fits within the image bounds.
        It scales down the shape if it's too large and repositions it if necessary.
        """
        # Calculate bounding box
        min_x, min_y = np.min(vertices, axis=0)
        max_x, max_y = np.max(vertices, axis=0)
        width, height = max_x - min_x, max_y - min_y

        # Scale the shape down if it doesn't fit
        if width > self.width or height > self.height:
            scale_factor = min(self.width / width, self.height / height)
            vertices *= scale_factor

        # Recalculate the bounding box after scaling
        min_x, min_y = np.min(vertices, axis=0)
        max_x, max_y = np.max(vertices, axis=0)
        width, height = max_x - min_x, max_y - min_y

        # Ensure that the width and height fit within the image bounds
        if self.width > width and self.height > height:
            offset_x = np.random.randint(0, max(1, self.width - width))
            offset_y = np.random.randint(0, max(1, self.height - height))

            vertices[:, 0] += offset_x - min_x
            vertices[:, 1] += offset_y - min_y
        else:
            # If the shape still doesn't fit, center it within the bounds
            offset_x = (self.width - width) // 2 - min_x
            offset_y = (self.height - height) // 2 - min_y
            vertices[:, 0] += offset_x
            vertices[:, 1] += offset_y

        return vertices
