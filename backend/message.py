SUCCESS = 200 #"success"
OTHER_ERROR = 500 #"unknown error"
LOGIN_UNEXIST_USER = 501 #"Login failed: User does not exist"
LOGIN_WRONG_PASSWORD = 502 #"Login failed: Wrong password"
REGISTER_EXIST_USER = 503 #"Register failed: User already exists"
REGISTER_FAILED = 504 #"Register failed: Internal server error"

PARAM_ERROR = 505 #"Parameter error"

NOT_JOIN_GAME = 510 #"Not join game"
GAME_CREATE_FAILED = 511 #"Create game failed"

MOVE_NO_PIECE = 601 #"Move failed: No piece to move"
MOVE_OUT_OF_BOARD = 602 #"Move failed: Move out of board"
MOVE_INVALID = 603 #"Move failed: Invalid way to move"
