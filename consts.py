import re
from typing import TypeAlias, Literal, Final

GroupType: TypeAlias = Literal["master", "regular", "aspirantes"]

GROUP_TYPE_ASPIRANTES: Final[GroupType] = "aspirantes"
GROUP_TYPE_MASTERS: Final[GroupType] = "master"
#  regular - это бакалавриат и специалитет
GROUP_TYPE_REGULAR: Final[GroupType] = "regular"

# GROUPS_TYPES_SIGN: Final[dict[GROUP_TYPE, str]] = {"master": "М", "regular": ""}


GROUP_NAME_PARTS_DEFAULT: Final[tuple[str, ...]] = (
    "is_master_1", "course", "group_number", "is_master_2", "subgroup_letter", "note"
)

#  Паттерны могут быть неточными: через время логика названий групп уточнится
GROUP_NAME_DEFAULT_PATTERN: re.Pattern = re.compile(r"(М)?([0-9])([0-9])(М)?([а-яА-ЯеёЕЁ])?(?:\((.+)\))?")

GROUP_NAME_PARTS_ASPIRANTES: Final[tuple[str, ...]] = (
    "course", "group_number", "note", "subgroup_letter"
)
GROUP_NAME_ASPIRANTES_PATTERN: re.Pattern = re.compile(r"([0-9])([0-9]{2})(?:\(([0-9а-яА-ЯеёЕЁ]+)\))?(?:-(\w+))?")

WeekMark = TypeAlias = Literal["every", "minus", "plus"]

WEEK_MARK_EVERY: Final[WeekMark] = "every"
WEEK_MARK_PLUS: Final[WeekMark] = "plus"
WEEK_MARK_MINUS: Final[WeekMark] = "minus"

SubjectType: TypeAlias = Literal["lecture", "labwork", "practice", "seminar", "unknown"]

SUBJECT_TYPES: Final[dict[SubjectType, list[str]]] = {
    "lecture": ["Лекция"],
    "labwork": ["Лаб. работа"],
    "practice": ["Практика", "Практическое занятие"],
    "seminar": ["Семинар"]
}
