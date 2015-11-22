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
            i_level = Level(lvl)
            self.levels.append(i_level)
            index += 1

##########################################################
    def fill(self):
        os.chdir(self.root)
        for t in os.walk("."):
            lvl = self.get_level(t[0].replace("\\", "/"))
# each level contains a list of the hosted directories. Each of these directories contains ONLY files.
# It mustn't know about subdirectories. These are contained in the other levels objects
            i_level = self.levels[lvl - 1]
            local = t[0].replace("\\", "/")
            path = os.path.join(self.root, os.path.abspath(local)).replace("\\", "/")
            path = path.replace("\\", "/")
            i_dir = Directory(path, local, t[2])
            i_level.directories.append(i_dir)

        pass

##########################################################
    def get_level(self, path):
        level_num = path.split(self.separator)
        return len(level_num)

##########################################################
    def check_level(self, index):
        if index < len(self.levels):
            return self.levels[index]
        else:
            return None


##########################################################
    def Compare_with(self, target):
        index = -1
        for lvl in self.levels:
            index += 1
            tlvl = target.check_level(index)
            if tlvl is None:
                self.set_level(index, False)
                continue

            for dir in lvl.directories:
                for tdir in tlvl.directories:
                    if dir.name == tdir.name:
                        dir.available = True
                        tdir.available = True
                        for file in dir.files:
                            file.check_attrib(tdir.files)
                        break

##########################################################
    def set_level(self, index, flag):
        self.levels[index].set_directories(flag)

##########################################################
    def sync_with(self, target, parameters, log):
        self.log = log
# Way 1: Source to Target
        index = 0
        for lvl in self.levels:
            tlvl = target.check_level(index)  # if target level is not available None is returned
            index += 1
            for dir in lvl.directories:
# This solves the problem of the preceding ./ (linux) or .\ (win) in the local path
                if dir.name.find("." + target.separator) == 0:
                    local = dir.name[2:]
                else:
                    local = dir.name

                if not dir.available:  # Case 1
                    self.case_1(dir, local, target.root, parameters)
                else:  # Case 2
                    self.case_2_to_4(dir, local, target.root, parameters)

# Way 2: Target to Source
        index = 0
        for tlvl in target.levels:
            lvl = self.check_level(index)
            index += 1
            for tdir in tlvl.directories:
# This solves the problem of the preceding ./ (linux) or .\ (win) in the local path
                if tdir.name.find("." + target.separator) == 0:
                    local = tdir.name[2:]
                else:
                    local = tdir.name

                if not tdir.available:  # Case 5
                    self.case_5(tdir, local, target.root, parameters)
                else:  # Case 6
                    self.case_6_to_8(tdir, local, target.root, parameters)



##########################################################
    def case_1(self, dir, local, root, parameters):
        dest = os.path.join(root, local).replace("\\", "/")
        dir.set_available()
        try:
            shutil.copytree(dir.path, dest)
            message = "Copy directory {} incl. all subdirectories".format(dir.name)
            self.log.emit(message, parameters.verbose, "normal")
        except FileExistsError:
            message = "Directory {} exists. Do nothing".format(dir.name)
#            print("info: ", message)
            self.log.emit(message, parameters.verbose, "normal")

##########################################################
    def case_2_to_4(self, dir, local, root, parameters):
        for file in dir.files:
            dest = os.path.join(root, local, file.name).replace("\\", "/")
            src = os.path.join(dir.path, file.name).replace("\\", "/")

            if not file.available:  # case 3
                shutil.copy(src, dest)
                message = "Copy not available file from {} to {} ".format(src, dest)
                self.log.emit(message, parameters.verbose, "normal")
            elif file.available: # case 4
                if file.newer is None:
                    pass
                elif file.newer:  # case 4.1
                    shutil.copy(src, dest)
                    message = "Copy file from {} to {} ".format(src, dest)
                    self.log.emit(message, parameters.verbose, "normal")
                    file.newer = False
                    file.target_file.newer = False
                elif not file.newer:  # case 4.2
                    if parameters.bidirectional:  # case 4.2.1
                        shutil.copy(dest, src)
                        message = "Copy file from {} to {} ".format(dest, src)
                        self.log.emit(message, parameters.verbose, "normal")
                        file.newer = False
                        file.target_file.newer = False
                    elif not parameters.bidirectional and parameters.force:  # case 4.2.2.1
                        shutil.copy(src, dest)
                        message = "Copy older file from {} to {} ".format(src, dest)
                        self.log.emit(message, parameters.verbose, "warning")
                        file.newer = False
                        file.target_file.newer = False
                    elif not parameters.bidirectional and not parameters.force:  # case 4.2.2.2
                        message = "Nothing copied. Target file:{}, is newer than source file:{}".format(dest, src)
#                        print("warning: ", message)
                        self.log.emit(message, parameters.verbose, "warning")


##########################################################
    def case_5(self, tdir, local, troot, parameters):
        dest = os.path.join(troot, local).replace("\\", "/")
        src = os.path.join(self.root, local).replace("\\", "/")
        if parameters.delete:  # case 5.1
            try:
                shutil.rmtree(dest)
                message = "Deleting directory {}".format(dest)
                self.log.emit(message, parameters.verbose, "warning")
            except FileNotFoundError:
                message = "Directory {} already deleted".format(dest)
                self.log.emit(message, parameters.verbose, "normal")
            except:
                message = "Directory {} not found".format(dest)
                self.log.emit(message, parameters.verbose, "error")
        elif parameters.bidirectional:  # case 5.2
            try:
                shutil.copytree(dest, src)
                message = "Copy directory from {} to {}".format(dest, src)
                self.log.emit(message, parameters.verbose, "normal")
            except FileExistsError:
                message = "Directory {} is already available. Do nothing.".format(src)
#                print("info: ",message)
                self.log.emit(message, parameters.verbose, "normal")
            except:
                message = "Problem with copying the directory {}. Stop.".format(src)
#                print("error: ", message)
                self.log.emit(message, parameters.verbose, "error")
        else:  # case 5.3
            message = "Copy nothing. Directory {} is available only on target.".format(dest)
#            print("warning: ", message)
            self.log.emit(message, parameters.verbose, "normal")

##########################################################
    def case_6_to_8(self, tdir, local, troot, parameters):
        for file in tdir.files:
            dest = os.path.join(tdir.path, file.name).replace("\\", "/")
            src = dest.replace(troot, self.root)

            if not file.available:  # case 7
                if parameters.delete:  # case 7.1
                    os.remove(dest)
                    message = "Delete target file {}.".format(dest)
                    self.log.emit(message, parameters.verbose, "warning")
                elif parameters.bidirectional:  # case 7.2
                    shutil.copy(dest, src)
                    message = "Copy file from {} to {}".format(dest, src)
                    self.log.emit(message, parameters.verbose, "normal")
                elif not parameters.delete and not parameters.bidirectional:  # case 7.3
                    message = "Do Nothing. File {} is available only on target.".format(dest)
                    self.log.emit(message, parameters.verbose, "warning")
