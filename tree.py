from level import Level
from treestat import TreeStat
from directory import Directory
import os

__author__ = 'fernass daoud'


class Tree:
    def __init__(self, e_root):
        self.root = e_root
        treestatistics = TreeStat()
        os.chdir(self.root)

        for t in os.walk("."):
            treestatistics.check(t)

        self.separator = treestatistics.sep
        index = 0
#        self.levels = len(treestatistics.levels) * [Level]
        self.levels = list()
        for lvl in treestatistics.levels:
#            i_size = treestatistics.levels[index]
            i_level = Level(lvl)
            self.levels.append(i_level)
            index += 1

##########################################################
    def fill(self):
        os.chdir(self.root)
        for t in os.walk("."):
            lvl = self.get_level(t[0])
# each level contains a list of the hosted directories. Each of these directories contains ONLY files.
# It mustn't know about subdirectories. These are contained in the other levels objects
            i_level = self.levels[lvl - 1]
            path = os.path.join(self.root, os.path.abspath(t[0]))
            i_dir = Directory(path, t[0], t[2])
            i_level.directories.append(i_dir)

        pass




##########################################################
    def get_level(self, path):
        level_num = path.split(self.separator)
        return len(level_num)

##########################################################
    def Compare_with(self, other):
        index = 0
        for lvl in self.levels:
            olvl = other.levels[index]
            index += 1
            for dir in lvl.directories:
                if dir in olvl:
                    dir.available = True
