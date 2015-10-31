import os

__author__ = 'fernass daoud'


class File:
    def __init__(self, path, e_file):
        self.path = path
        self.available = False # flag to be set during comparison of files in directory objects
        self.newer = False # flag to indicate if source or target file is newer

#        (self.mode, self.ino, self.dev, self.nlink, self.uid, self.gid, self.size, self.atime, self.mtime, self.ctime) \
#            = os.stat(e_file)
        try:
            (self.mode, self.ino, self.dev, self.nlink, self.uid, self.gid, self.size, self.atime, self.mtime, self.ctime) \
            = os.stat(os.path.join(self.path, e_file))
        except:
            test1 = os.access(e_file, os.F_OK)
            path1 = os.path.basename(e_file)

            path1 = os.path.abspath(e_file)
            test11 = os.access(path1, os.F_OK)
            path2 = "/home/daoud/tmp/test1/test_walk/" + e_file
            test12 = os.access(path2, os.F_OK)

            test2 = os.access(e_file, os.R_OK)
            test3 = os.access(e_file, os.W_OK)
            test4 = os.access(e_file, os.X_OK)

            pass
        self.name = e_file


##########################################################
    def check_name(self, e_files):
        for e_file in e_files:
            if self.name == e_file.name:
                self.available = True
                e_file.available = True
                if self.mtime >= e_file.mtime:
                    self.newer = True