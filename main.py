import os
from tree import Tree
from systemdata import SystemData

__author__ = 'fernass daoud'

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

source.Compare_with(target)

'''
The synchronisation is performed in two-way mode.
Way 1, Source to Target: Run through levels (source and target in parallel). Run through directories of each level.
1. If a directory on source is not available on target, copy source directory and all included files to target.
2. If a directory on source is available on target, the included files are checked.
3. If file on source is not available on target, copy file from source to target.
4. if file on source is available on target:
4.1 if source file is newer than target one, source file is copied overriding the target
4.2 if source file is older than target one
4.2.1 if --bidirectional, target file is copied overriding source file
4.2.2 if not --bidirectional
4.2.2.1 If --force (the older) source file is copied overriding the (newer) target and log a warning
4.2.2.2 If not --force output an information and pass

Way 2, Target to Source: Run again through levels (source and target in parallel). Run through directories of each level.
5. If a directory on target is not available on source
5.1 If --delete delete directory including all included files (and subdirectories) on target
5.2 If --bidirectional then copy target directory to source including all files and subdirectories
5.3 If not --delete and not --bidirectional output info and pass
6. If a directory on target is available on source, the included files are checked.
7. If file on target is not available on source
7.1 If --delete delete file on target
7.2 If --bidirectional copy target file to source
7.3 If not --delete and not --bidirectional output info and pass
8. if file on target is available on source: this case is covered by Way 1 (no coding required).
'''
source.sync_with(target, parameters)

