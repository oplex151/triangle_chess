# ECONNABORTED = 103 #"Connection aborted"

SUCCESS = 200 #"success"
OTHER_ERROR = 500 #"unknown error"
LOGIN_UNEXIST_USER = 501 #"Login failed: User does not exist"
LOGIN_WRONG_PASSWORD = 502 #"Login failed: Wrong password"
ALREADY_LOGIN = 506 #"Already login"
USER_NOT_LOGIN = 507 #"User not login"
USER_NOT_EXIST = 508 #"User not exist"
NAME_ALREADY_EXIST = 509 #"Name already exist"

REGISTER_EXIST_USER = 503 #"Register failed: User already exists"
REGISTER_FAILED = 504 #"Register failed: Internal server error"
WRONG_OLD_PASSWORD = 513 #"Wrong old password"
BANNED_USER = 514 #"Banned user"
USER_ALREADY_BANNED = 515 #"User already banned"
ROOM_FULL = 516 #"Room full"
REPEAT_DRAW_REQUEST = 517 #"Repeat draw request"
ROOM_PASSWORD_ERROR = 518 #"Room password error"
GAME_ALREADY_START = 519 #"Game already start"

PARAM_ERROR = 505 #"Parameter error"


NOT_JOIN_GAME = 510 #"Not join game"
GAME_CREATE_FAILED = 511 #"Create game failed"
NOT_YOUR_TURN = 512 #"Not your turn"

ROOM_NOT_EXIST = 520 #"Room not exist"
ALREADY_IN_ROOM = 521 #"Already in room"
NOT_IN_ROOM = 522 #"Not in room"
ROOM_NOT_ENOUGH = 523 #"Room not enough"
NOT_HOLDER = 524 #"Not holder"
REMOVE_USER_FAILED = 525 #"Remove user failed"
NOT_ALL_READY = 526 #"Not all ready"

ALLREADY_FRIEND = 530 #"Already friend"
NO_FRIENDS = 531 #"No friends"
NOT_FRIEND = 532 #"Not friend"
ALLREADY_APPLIED = 533 #"Already applied"

NOT_ADMIN = 540 #"Not admin"
NO_APPEALS = 541 #"No appeals"

SESSION_EXPIRED = 550 #"Session expired"

PHONE_NUMBER_ERROR = 560 #"Phone number error"
CATEGORY_NOT_EXIST = 561 #"Category not exist"
FREQUENT_OPERATION = 562 #"Frequent operation"
VERIFICATION_CODE_ERROR = 563 #"Verification code error"

MOVE_NO_PIECE = 601 #"Move failed: No piece to move"
MOVE_OUT_OF_BOARD = 602 #"Move failed: Move out of board"
MOVE_INVALID = 603 #"Move failed: Invalid way to move"

GAME_END = 701 #"Game end"
GAME_ONGOING = 702 #"Game ongoing"