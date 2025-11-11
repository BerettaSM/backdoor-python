from backdoor.exceptions.core import ApplicationException


class DisconnectedException(ApplicationException):

    def __init__(self, message: str = "Other end disconnected") -> None:
        super().__init__(message)
