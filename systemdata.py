import sys
import os.path
from argparse import ArgumentParser
from tree import Tree

__author__ = 'fernass daoud'

class SystemData:
    def __init__(self):
        pass

##########################################################
    def commandline(self):
        parser = ArgumentParser(
            description="A platform-independent synchronisation software",
            prog="sincsopht",
            usage="sincsopht -s source -t target [-bi] [-d]",
            add_help=True)
        parser.add_argument("-no-gui", dest="nogui", action="store_true", default=False,
                            help="start graphical user interface")
        parser.add_argument("-s", "--source", dest="source", help="name of source directory")
        parser.add_argument("-t", "--target", dest="target", help="name of target directory")
        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
        parser.add_argument("-f", "--force", dest="force", action="store_true",
                            help="in case of unidirectional synchronisation the "
                                 "newer files on target,will be overriden by source files")

        exclusive1 = parser.add_mutually_exclusive_group()
        exclusive1.add_argument("-bi", "--bidirectional", dest="bidirectional", action="store_true",
                                help="flag indicating if synchronisation to be in both directions, "
                                     "i.e. source and target are identical after operation. "
                                     "In this case the --delete option is ignored")
        exclusive1.add_argument("-d", "--delete", dest="delete", action="store_true",
                                help="in case of unidirectional synchronisation the directories and "
                                     "files on target, that are not available on source, will be deleted")


        args = parser.parse_args()

        self.nogui = args.nogui
        if args.source:
            self.source = args.source.replace("\\","/")
        if args.target:
            self.target = args.target.replace("\\","/")
        self.bidirectional = args.bidirectional
        self.force = args.force
        if self.bidirectional and self.force:
            self.force = False
            print("When the option -bi (--bidirectional) is set, -f (--force) is deactivated")
        self.delete = delete = args.delete
        self.verbose = args.verbose

        if self.nogui and not (self.source and self.target):
            print("When -nogui is selected, both source and target directories must be given")
            sys.exit(0)

##########################################################
    def check_path(self, path):
        return os.path.exists(path)

##########################################################
    def run(self, log):
        if not self.check_path(self.source):
            log.emit("Source directory {} not available, or check permissions!".format(self.source), self.verbose, "error")
            print("Error: Check sincsopht.log")
            sys.exit()
        if not self.check_path(self.target):
            log.emit("Target directory {} not available, or check permissions!".format(self.target), self.verbose, "error")
            print("Error: Check sincsopht.log")
            sys.exit()

        Source = Tree(self.source)
# initialise the tree object, i.e. generate a tree with as much levels as required (as acquired the treestatistics)
# and set the correct size of each level (attribute levels), i.e. the number of the directories of each
# level (of type Directory)
        Target = Tree(self.target)

# The fill methods runs through the directory tree and establishes following data model:
# tree object, hier the instance source, which includes
# list of level objects. A level object includes all directory objects of same tree level.
# A directory object contains the own local path (important to be local) and a list of all file objects in this directory
# The directory object doesn't need to know about the own subdirectories thanks to the level concept
# The file object contains the own name and the os file attributes to be compared
#
# Level 0                             Root
#                                  /     \
# Level 1                         foo     bar
#                               /  \     /  \
# Level 2                      bla  blu  pip  pap

        Source.fill()
        Target.fill()
        Source.Compare_with(Target)


#The synchronisation is performed in two-way mode.
#Way 1, Source to Target: Run through levels (source and target in parallel). Run through directories of each level.
#1. If a directory on source is not available on target, copy source directory and all included files to target.
#2. If a directory on source is available on target, the included files are checked.
#3. If file on source is not available on target, copy file from source to target.
#4. if file on source is available on target:
#4.1 if source file is newer than target one, source file is copied overriding the target
#4.2 if source file is older than target one
#4.2.1 if --bidirectional, target file is copied overriding source file
#4.2.2 if not --bidirectional
#4.2.2.1 If --force (the older) source file is copied overriding the (newer) target and log a warning
#4.2.2.2 If not --force output an information and pass
#
#Way 2, Target to Source: Run again through levels (source and target in parallel). Run through directories of each level.
#5. If a directory on target is not available on source
#5.1 If --delete delete directory including all included files (and subdirectories) on target
#5.2 If --bidirectional then copy target directory to source including all files and subdirectories
#5.3 If not --delete and not --bidirectional output info and pass
#6. If a directory on target is available on source, the included files are checked.
#7. If file on target is not available on source
#7.1 If --delete delete file on target
#7.2 If --bidirectional copy target file to source
#7.3 If not --delete and not --bidirectional output info and pass
#8. if file on target is available on source: this case is covered by Way 1 (no coding required).

        Source.sync_with(Target, self, log)
        print("Success: Check sincsopht.log")
        log.emit("Synchronisation Successful!", self.verbose, "success")