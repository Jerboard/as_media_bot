from enum import Enum


class BaseCB(str, Enum):
    CLOSE = "close"


class AdminCB(str, Enum):
    EDIT = "admin_edit_message"
    SEND_START = "admin_send_message_start"
    SELECT_GROUP = "admin_select_group"
    WAIT = "admin_wait_msg"
    BACK = "admin_back"
    DOCUMENT = "admin_document"
