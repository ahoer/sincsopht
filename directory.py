from file import File

__author__ = 'fernass daoud'

class Directory:
    def __init__(self, path, e_name, e_files):
        self.name = e_name
        self.files = list()
        for i in e_files:
            i_file = File(path, i)

            self.files.append(i_file)
        pass

##########################################################
    def __iter__(self):
        pass

##########################################################
    def __next__(self):
        pass

##########################################################
    def fill(self):
        pass
