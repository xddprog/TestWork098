from enum import Enum


class TaskStatuses(str, Enum):
    PENDING = "pending"
    DONE = "done"