import logging

class FileLogger():
    def __init__(self, verbose):
#        super().__init__(filename="sincsopht.log")
        fileHandle = logging.FileHandler(filename="sincsopht.log", mode="w")
        frm = logging.Formatter("[{levelname:8}], {asctime}: {message}", "%d.%m.%Y", style="{")
        fileHandle.setFormatter(frm)
        self.logger = logging.getLogger()
        self.logger.addHandler(fileHandle)
        if verbose:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

    def emit(self, record, tag=""):
        # Append message (record) to the file
        if tag=="normal":
            self.logger.info(record)
        elif tag=="warning":
            self.logger.warning(record)
        elif tag=="error":
            self.logger.error(record)
        elif tag=="success":
            self.logger.info(record)
