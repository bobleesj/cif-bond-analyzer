from enum import Enum


class TernaryConfig(Enum):
    X_SHIFT = 0.0
    Y_SHIFT = 0.0
    TAGS_IN_FIRST_EXTRA_LINE = ["lt", "ht", "hp", "hp1", "hp2", "hp3"]
    TAGS_IN_SECOND_EXTRA_LINE = ["trig", "ht_trig"]
    TAGS_IN_THIRD_EXTRA_LINE = [""]
