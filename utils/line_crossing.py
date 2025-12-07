class LineCounter:
    def __init__(self, y_line):
        self.y_line = y_line
        self.passed = set()

    def check(self, track_id, y_center):
        if y_center > self.y_line and track_id not in self.passed:
            self.passed.add(track_id)
            return True
        return False
