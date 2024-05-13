# ECONNABORTED = 103 #"Connection aborted"

SUCCESS = 200 #"success"
OTHER_ERROR = 500 #"unknown error"
LOGIN_UNEXIST_USER = 501 #"Login failed: User does not exist"
LOGIN_WRONG_PASSWORD = 502 #"Login failed: Wrong password"
ALREADY_LOGIN = 506 #"Already login"
USER_NOT_LOGIN = 507 #"User not login"


REGISTER_EXIST_USER = 503 #"Register failed: User already exists"
REGISTER_FAILED = 504 #"Register failed: Internal server error"

PARAM_ERROR = 505 #"Parameter error"


NOT_JOIN_GAME = 510 #"Not join game"
GAME_CREATE_FAILED = 511 #"Create game failed"
NOT_YOUR_TURN = 512 #"Not your turn"

ROOM_NOT_EXIST = 520 #"Room not exist"
ALREADY_IN_ROOM = 521 #"Already in room"
NOT_IN_ROOM = 522 #"Not in room"
ROOM_NOT_ENOUGH = 523 #"Room not enough"

MOVE_NO_PIECE = 601 #"Move failed: No piece to move"
MOVE_OUT_OF_BOARD = 602 #"Move failed: Move out of board"
MOVE_INVALID = 603 #"Move failed: Invalid way to move"

GAME_END = 701 #"Game end"