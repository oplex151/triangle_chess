
class ChessError(Exception):
    pass

class InvalidMoveError(ChessError):
    def __init__(self, message='Invalid move'):
        super().__init__(message)

class OutOfBoardError(ChessError):
    def __init__(self, message='Out of board'):
        super().__init__(message)

class SessionException(Exception):
    def __init__(self, message='session expired!'):
        super().__init__(message)
