import numpy as np
from masks.mask import Mask

class OrganicShapeMask(Mask):
    def __init__(self, image, num_vertices=12, displacement_strength=0.2, base_decay_factor=0.9, iterations=5, num_shapes=1, relative_size=(0.02, 0.05)):
        super().__init__(image, num_shapes, relative_size)
        
        # Validate and adjust parameters
        self.num_vertices = max(3, num_vertices)  # Ensure at least a triangle
        self.displacement_strength = np.clip(displacement_strength, 0.1, 1.0)  # Prevent too small or large values
        self.base_decay_factor = np.clip(base_decay_factor, 0.8, 0.99)  # Keep decay factor reasonable
        self.iterations = max(1, iterations)  # Ensure at least one iteration

    def create_polygon(self):
        """
        Create an ellipsoidal shape with irregularities.
        """
        radius_x = self.get_random_size()  # Get size relative to image for x-axis
        radius_y = self.get_random_size()  # Get size relative to image for y-axis

        angles = np.linspace(0, 2 * np.pi, self.num_vertices, endpoint=False)
        vertices = np.array([(np.cos(angle) * radius_x, np.sin(angle) * radius_y) for angle in angles])

        # Introduce initial irregularities
        vertices += np.random.normal(scale=0.1, size=vertices.shape) * np.array([radius_x, radius_y])

        return vertices

    def displace_vertices(self, vertices):
        """
        Displace the vertices to create further irregularities.
        """
        num_vertices = len(vertices)
        for _ in range(self.iterations):
            chosen_vertex = np.random.randint(0, num_vertices)
            d = np.random.uniform(0.1, self.displacement_strength)
            displacement_levels = {chosen_vertex: 0}

            # Adjust decay factor based on size
            max_distance = np.max(np.sqrt(np.sum((vertices - vertices.mean(axis=0))**2, axis=1)))
            decay_factor = self.base_decay_factor ** (max_distance / min(self.height, self.width))

            # Update displacement levels for all vertices
            for level in range(1, num_vertices):
                new_displacements = {}
                for vertex, dist_level in displacement_levels.items():
                    if dist_level == level - 1:
                        next_vertex = (vertex + 1) % num_vertices
                        prev_vertex = (vertex - 1 + num_vertices) % num_vertices
                        if next_vertex not in displacement_levels:
                            new_displacements[next_vertex] = level
                        if prev_vertex not in displacement_levels:
                            new_displacements[prev_vertex] = level
                displacement_levels.update(new_displacements)

            for i, level in displacement_levels.items():
                factor = 1 + d * (decay_factor ** level)
                direction = vertices[i] - vertices.mean(axis=0)
                vertices[i] += direction * (factor - 1)

        return vertices

    def apply_mask(self):
        mask = np.zeros_like(self.image, dtype=float)
        for _ in range(self.num_shapes):
            vertices = self.create_polygon()
            vertices = self.displace_vertices(vertices)

            # Adjust shape to fit within image bounds
            vertices = self.adjust_shape_to_bounds(vertices)

            mask = self._draw_polygon(mask, vertices)

        return mask

    def _draw_polygon(self, mask, vertices):
        """
        Draw the polygon on the mask.
        """
        vertices = np.round(vertices).astype(int)
        for i in range(len(vertices)):
            start = vertices[i]
            end = vertices[(i + 1) % len(vertices)]
            self._draw_line(mask, start, end)
        
        self._fill_polygon(mask, vertices)

        return mask

    def _draw_line(self, mask, start, end):
        x1, y1 = start
        x2, y2 = end
        num_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
        x_points = np.linspace(x1, x2, num_points).astype(int)
        y_points = np.linspace(y1, y2, num_points).astype(int)

        x_points = np.clip(x_points, 0, mask.shape[1] - 1)
        y_points = np.clip(y_points, 0, mask.shape[0] - 1)

        mask[y_points, x_points] = 1

    def _fill_polygon(self, mask, vertices):
        x_grid, y_grid = np.meshgrid(np.arange(mask.shape[1]), np.arange(mask.shape[0]))

        is_inside = np.zeros_like(mask, dtype=bool)
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            is_inside ^= ((y1 > y_grid) != (y2 > y_grid)) & (x_grid < (x2 - x1) * (y_grid - y1) / (y2 - y1 + 1e-9) + x1)

        mask[is_inside] = 1
