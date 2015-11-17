from file import File
import os

__author__ = 'fernass daoud'


class Directory:
    def __init__(self, path, e_name, e_files):
        self.name = e_name
        self.path = path
        self.available = False  # flag to be set during comparison of directory names
        self.files = list()
        for i in e_files:
            i_file = File(path, i)

            self.files.append(i_file)
        pass

##########################################################
    def set_available(self):
        self.available = True
        for file in self.files:
            file.available = True

##########################################################
    def __iter__(self):
        pass

##########################################################
    def __next__(self):
        pass

##########################################################
    def fill(self):
        pass

##########################################################
    def __contains__(self, item):
        pass

##########################################################
'''    def get_name(self):
        return self.name

##########################################################
    def set_name(self, e_name):
        self.name = e_name

############### PROPERTY ATTRIBUTES ######################
    name = property(get_name, set_name)
'''
