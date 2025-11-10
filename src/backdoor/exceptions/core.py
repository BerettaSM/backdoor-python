class ApplicationException(Exception):
    
    def __str__(self) -> str:
        prefix = "err"
        if not self.args:
            message = "something went wrong"
        else:
            message = ",".join("{}" for _ in self.args).format(*self.args)
        return "{}: {}".format(prefix, message)


class InvalidArgumentException(ApplicationException):
    ...
