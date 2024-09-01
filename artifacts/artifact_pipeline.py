class ArtifactPipeline:
    def __init__(self, image):
        self.image = image
        self.effects = []  # Unified list for both artifacts and filters

    def add_effect(self, effect):
        # Add the effect to the list and immediately apply it
        self.effects.append(effect)
        self.image = effect.apply_effect(self.image)

    def get_final_image(self):
        # Return the final processed image
        return self.image
