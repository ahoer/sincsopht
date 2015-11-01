from level import Level
from treestat import TreeStat
from directory import Directory
import os
import shutil

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
    def Compare_with(self, target):
        index = 0
        for lvl in self.levels:
            tlvl = target.levels[index]
            index += 1
            for dir in lvl.directories:
                for tdir in tlvl.directories:
                    if dir.name == tdir.name:
                        dir.available = True
                        tdir.available = True
                        for file in dir.files:
                            file.check_attrib(tdir.files)
                        break

##########################################################
    def sync_with(self, target, parameters):
# Way 1: Source to Target
        index = 0
        for lvl in self.levels:
            tlvl = target.levels[index]
            index += 1
            for dir in lvl.directories:
# This solves the problem of the preceding ./ (linux) or .\ (win) in the local path
                if dir.name.find("." + target.separator) == 0:
                    local = dir.name[2:]
                else:
                    local = dir.name

                if not dir.available: # Case 1
                   self.case_1(dir, local, target.root)
                else: # Case 2
                    self.case_2_to_4(dir, local, target.root, parameters)

# Way 2: Target to Source
        index = 0
        for tlvl in target.levels:
            lvl = self.levels[index]
            index += 1
            for tdir in tlvl.directories:
# This solves the problem of the preceding ./ (linux) or .\ (win) in the local path
                if tdir.name.find("." + target.separator) == 0:
                    local = tdir.name[2:]
                else:
                    local = tdir.name

                if not tdir.available: # Case 5
                   self.case_5(tdir, local, target.root, parameters)
                else: # Case 6
                    self.case_6_to_8(tdir, local, target.root, parameters)



##########################################################
    def case_1(self, dir, local, root):
        dest = os.path.join(root, local)
        dir.set_available()
        try:
            shutil.copytree(dir.path, dest)
        except FileExistsError:
            print("Directory {} exists.".format(dir.name))

##########################################################
    def case_2_to_4(self, dir, local, root, parameters):
        for file in dir.files:
            dest = os.path.join(root, local, file.name)
            src = os.path.join(dir.path, file.name)

            if not file.available: # case 3
                shutil.copy(src, dest)
                file.target_file.available = True
            elif file.available: # case 4
                if file.newer: # case 4.1
                    os.replace(src, dest)
                    file.newer = False
                    file.target_file.newer = False
                elif not file.newer: # case 4.2
                    if parameters.bidirectional: # case 4.2.1
                        os.replace(dest, src)
                        file.newer = False
                        file.target_file.newer = False
                    elif parameters.bidirectional and parameters.force: # case 4.2.2.1
                        os.replace(dest, src)
                        file.newer = False
                        file.target_file.newer = False
                    else: # case 4.2.2.2
                        print("Warning: target file:{},\n is newer than source file:{}".format(dest,src))


##########################################################
    def case_5(self, tdir, local, root, parameters):
        dest = os.path.join(root, local)
        if parameters.delete:
            shutil.rmtree(dest)
        else:
            print("Warning: Directory {} is available only on target.\n".format(dest))
            print("Use option -d (-delete) in order to delete obsolete files and directories on tagret.")

##########################################################
    def case_6_to_8(self, tdir, local, root, parameters):
        for file in tdir.files:
            dest = os.path.join(root, local, file.name)
            src = os.path.join(tdir.path, file.name)

            if not file.available: # case 7
                if parameters.delete: # case 7.1
                    os.remove(dest)
                elif not parameters.delete and not parameters.bidirectional: # case 7.2
                    print("Warning: The file {} is available only on target.\n".format(dest))
                    print("Use option -d (-delete) in order to delete obsolete files and directories on tagret.")
                elif not parameters.delete and parameters.bidirectional: # case 7.3
                    shutil.copy(dest, src)


