from math import sqrt, pow

import cv2


class Counter:
    forward_count = 0
    backward_count = 0
    paths_cache = {} # Only centers
    count_line_y = 100
    idx_gen = 0
    max_dist = 30
    max_path = 10
    count_line_x = 500
    great_britain = False

    def __init__(self, count_line_y=100, count_line_x=500, max_dist=30, max_path=10, great_britain=False):
        self.great_britain = great_britain
        self.count_line_x = count_line_x
        self.max_path = max_path
        self.max_dist = max_dist
        self.count_line_y = count_line_y
        self.idx_gen = 0

    @staticmethod
    def get_distance(p1, p2):
        return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))

    # (X, Y)
    @staticmethod
    def get_center(contour):
        x, y, w, h = contour
        return int((2 * x + w) / 2), int((2 * y + h) / 2)

    def get_path_key(self, contour):
        center = self.get_center(contour)
        for key, cached_path in self.paths_cache.items():
            if self.get_distance(center, cached_path[-1]) < self.max_dist:
                return key
        return -1

    def check_and_count(self, path_key):
        path = self.paths_cache[path_key]
        if len(path) < 2:
            return False
        last = path[0]
        curr = path[-1]
        # last = path[-2]
        # curr = path[-1]
        if not self.great_britain:
            if curr[1] > self.count_line_y > last[1] and curr[0] > self.count_line_x:
                self.backward_count += 1
                return True
            if curr[1] < self.count_line_y < last[1] and curr[0] < self.count_line_x:
                self.forward_count += 1
                return True
        else:
            if curr[1] > self.count_line_y > last[1] and curr[0] < self.count_line_x:
                self.backward_count += 1
                return True
            if curr[1] < self.count_line_y < last[1] and curr[0] > self.count_line_x:
                self.forward_count += 1
                return True
        return False

    # contours: (x, y, w, h)
    def analyze_contours(self, contours):
        for contour in contours:
            rect = cv2.boundingRect(contour)
            center = self.get_center(rect)
            path_key = self.get_path_key(rect)
            if path_key < 0:
                if not self.great_britain:
                    if (center[1] < self.count_line_y and center[0] < self.count_line_x) or\
                       (center[1] > self.count_line_y and center[0] > self.count_line_x):
                        continue
                else:
                    if (center[1] > self.count_line_y and center[0] < self.count_line_x) or\
                       (center[1] < self.count_line_y and center[0] > self.count_line_x):
                        continue
                self.paths_cache[self.idx_gen] = [center]
                self.idx_gen += 1
            else:
                self.paths_cache[path_key].append(center)
                self.paths_cache[path_key] = self.paths_cache[path_key][-self.max_path:]
                if self.check_and_count(path_key):
                    self.paths_cache.pop(path_key, None)

        return self.paths_cache

