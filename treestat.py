__author__ = 'fernass daoud'
import sys

class TreeStat():
    def __init__(self):
        self.levels = [0]
        if sys.platform == "win32":
            self.sep = "\\"
        else:
            self.sep = "/"


    def check(self, data):
        last_level = len(self.levels)
        current_level = self.get_level(data[0])

        if last_level < current_level:
            self.levels.append(1)
        elif last_level == current_level:
            self.levels[last_level - 1] += 1
        elif last_level > current_level:
            self.levels[current_level - 1] += 1


    def get_level(self, path):
        level_num = path.split(self.sep)
        return len(level_num)
