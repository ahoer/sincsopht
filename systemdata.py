from argparse import ArgumentParser
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
        parser.add_argument("-s", "--source", dest="source", required=True, help="name of source directory")
        parser.add_argument("-t", "--target", dest="target", required=True, help="name of target directory")
        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
        parser.add_argument("-f", "--force", dest="force", action="store_true", \
                help="in case of unidirectional synchronisation the newer files on target, \
                will be overriden by source files")

        exclusive1 = parser.add_mutually_exclusive_group()
        exclusive1.add_argument("-bi", "--bidirectional", dest="bidirectional", action="store_true", \
                help="flag indicating if synchronisation to be in both directions, i.e. source and target are \
                identical after operation. In this case the --delete option is ignored")
        exclusive1.add_argument("-d", "--delete", dest="delete", action="store_true", \
                help="in case of unidirectional synchronisation the directories and files on target, \
                that are not available on source, will be deleted")


        args = parser.parse_args()

        self.source = args.source
        self.target = args.target
        self.bidirectional = args.bidirectional
        self.force = args.force
        if self.bidirectional and self.force:
            self.force = False
            print("When the option -bi (--bidirectional) is set, -f (--force) is deactivated")
        self.delete = delete = args.delete
        self.verbose = args.verbose
