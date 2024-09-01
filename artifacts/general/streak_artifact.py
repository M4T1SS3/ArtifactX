import numpy as np
from artifacts.artifact import Artifact

class StreakArtifact(Artifact):
    def __init__(self, streak_factor=0.3):
        super().__init__()
        self.streak_factor = streak_factor

    def apply_effect(self, image):
        streaked_image = np.copy(image)
        num_streaks = int(self.streak_factor * 100)

        for _ in range(num_streaks):
            # Randomly select start and end points of the streaks
            x1, y1 = np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])
            x2, y2 = np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])

            # Compute line points for the streak
            rr, cc = np.linspace(y1, y2, num=500).astype(int), np.linspace(x1, x2, num=500).astype(int)

            # Introduce a streak by brightening or darkening the line
            streak_intensity = np.random.uniform(-0.5, 0.5)  # Increased intensity for more visible streaks
            for i in range(len(rr)):
                if 0 <= rr[i] < image.shape[0] and 0 <= cc[i] < image.shape[1]:
                    streaked_image[rr[i], cc[i]] = np.clip(streaked_image[rr[i], cc[i]] + streak_intensity * 255, 0, 255)

        return streaked_image
