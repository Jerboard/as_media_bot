from enum import Enum


class AdminStatus(str, Enum):
    EDIT = "edit_message"
    SEND = "send_message"
