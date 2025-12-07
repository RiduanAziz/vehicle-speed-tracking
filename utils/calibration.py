class Calibration:
    def __init__(self, real_distance_meters, pixel_distance):
        self.meters_per_pixel = real_distance_meters / pixel_distance

    def get_factor(self):
        return self.meters_per_pixel
