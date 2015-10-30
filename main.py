import os
from tree import Tree
from systemdata import SystemData

__author__ = 'fernass daoud'

#source_root = "/home/daoud/tmp/test1"
#source_root = "C:\\Users\\ferna\\Documents\\tmp\\test1"
# target_root = "C:\\Users\\ferna\\Documents\\tmp\\test2"

parameters = SystemData()
parameters.commandline()

''' initialise the tree object, i.e. generate a tree with as much levels as required (as acquired the treestatistics)
and set the correct size of each level (attribute levels), i.e. the number of the directories of each
level (of type Directory)'''
source = Tree(parameters.source)
target = Tree(parameters.target)

''' The fill methods runs through the directory tree and establishes following data model:
tree object, hier the instance source, which includes
list of level objects. A level object includes all directory objects of same tree level.
A directory object contains the own local path (important to be local) and a list of all file objects in this directory
The directory object doesn't need to know about the own subdirectories thanks to the level concept
The file object contains the own name and the os file attributes to be compared

Level 0                             Root
                                  /     \
Level 1                         foo     bar
                               /  \     /  \
Level 2                      bla  blu  pip  pap
'''
source.fill()
target.fill()

pass

