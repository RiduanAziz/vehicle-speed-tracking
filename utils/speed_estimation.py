import numpy as np

class SpeedEstimator:
    def __init__(self, meters_per_pixel, fps):
        self.positions = {}
        self.meters_per_pixel = meters_per_pixel
        self.fps = fps

    def update(self, track_id, x_center, y_center):
        if track_id not in self.positions:
            self.positions[track_id] = (x_center, y_center)
            return 0

        old_x, old_y = self.positions[track_id]
        pixel_dist = np.sqrt((x_center-old_x)**2 + (y_center-old_y)**2)

        meters = pixel_dist * self.meters_per_pixel
        speed_mps = meters * self.fps
        speed_kmph = speed_mps * 3.6

        self.positions[track_id] = (x_center, y_center)
        return speed_kmph
