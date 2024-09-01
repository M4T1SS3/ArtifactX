import numpy as np

from masks.mask import Mask

class PolygonalMask(Mask):
    def __init__(self, image, num_vertices_range=(3, 8), intensity_range=(0.8, 1.0), num_shapes=1, relative_size=None):
        super().__init__(image, num_shapes, relative_size)
        self.num_vertices_range = num_vertices_range
        self.intensity_range = intensity_range

    def _is_point_in_polygon(self, x, y, vertices):
        num_vertices = len(vertices)
        inside = False
        x0, y0 = vertices[0]
        for i in range(1, num_vertices + 1):
            x1, y1 = vertices[i % num_vertices]
            if y > min(y0, y1):
                if y <= max(y0, y1):
                    if x <= max(x0, x1):
                        if y0 != y1:
                            x_intercept = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                        if x0 == x1 or x <= x_intercept:
                            inside = not inside
            x0, y0 = x1, y1
        return inside

    def apply_mask(self):
        mask = np.zeros_like(self.image, dtype=float)
        for _ in range(self.num_shapes):
            mask_size = self.get_random_size()
            intensity = np.random.uniform(self.intensity_range[0], self.intensity_range[1])
            num_vertices = np.random.randint(self.num_vertices_range[0], self.num_vertices_range[1])

            center_x = np.random.randint(mask_size, self.width - mask_size)
            center_y = np.random.randint(mask_size, self.height - mask_size)

            angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
            vertices = [
                (int(center_x + mask_size * np.cos(angle)),
                 int(center_y + mask_size * np.sin(angle)))
                for angle in angles
            ]

            for y in range(self.height):
                for x in range(self.width):
                    if self._is_point_in_polygon(x, y, vertices):
                        mask[y, x] = intensity

        return mask
