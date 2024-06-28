from enum import Enum


class ExpenseCategory(Enum):
    DEFAULT = "Select a category"
    LEISURE = "Leisure"
    EDUCATION = "Education"
    UTILITIES = "Utilities"
    MISC = "Miscellaneous"