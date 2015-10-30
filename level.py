__author__ = 'fernass daoud'
from directory import Directory


class Level:
    def __init__(self, e_size):
#        self.directories = e_size * [None]
        self.directories = list()
        pass

    def size_level(self, e_dim):
        self.directories = e_dim * [Directory]
        return None



##########################################################
    def fill(self, dirs, files):
        pass


##########################################################
    def __contains__(self, item):
        for dir in self.directories:
            if dir.name == item.name:
                for file in dir.files:
                    file.check_name(item.files)
                item.available = True
                return True
        return False


##########################################################
'''    def __iter__(self):
        self.index = 0
        return self


##########################################################
    def __next__(self):
        self.index += 1
        if self.index < len(self.directories):
            return self.directories[self.index]
        else :
            raise StopIteration
'''
