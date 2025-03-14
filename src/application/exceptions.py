
class AppException(Exception):
    pass


class FileException(AppException):
    pass


class FileNameException(FileException):
    pass


class FileStructureException(FileException):
    pass