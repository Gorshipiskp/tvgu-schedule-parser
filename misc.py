import re
from dataclasses import dataclass
from json import JSONEncoder
from typing import Optional, Union, Any, TypeAlias

from aiohttp import ClientSession

from config import REQUEST_TIMEOUT, SKIP_BAD_LESSONS
from consts import GROUP_TYPE_ASPIRANTES, GROUP_NAME_PARTS_ASPIRANTES, GroupType, GROUP_TYPE_MASTERS, \
    GROUP_TYPE_REGULAR, GROUP_NAME_ASPIRANTES_PATTERN, GROUP_NAME_DEFAULT_PATTERN, GROUP_NAME_PARTS_DEFAULT, WeekMark, \
    SubjectType, SUBJECT_TYPES


class SkipLessonException(Exception):
    pass


class UnHandlingGroupException(Exception):
    pass


class TimetableNotFoundException(Exception):
    pass


@dataclass(frozen=True, kw_only=True)
class Group:
    origin_name: str
    faculty_code: str
    note: Union[str, None]
    course: Union[int, None]
    type: GroupType
    number: int
    subgroup_letter: Union[str, None]


@dataclass(frozen=True, kw_only=True)
class LessonTime:
    start: int
    end: int


@dataclass(frozen=True, kw_only=True)
class Teacher:
    fullname: str
    role: str


@dataclass(frozen=True, kw_only=True)
class Lesson:
    lesson_number: int
    week_day: int
    week_mark: WeekMark
    time_start: int
    time_end: int
    subject_name: str
    subject_type: SubjectType
    place: str
    teachers: tuple[Teacher]
    subgroup: Optional[str]


AllGroupsSchedules: TypeAlias = dict[str, dict[Group, tuple[Lesson]]]


def group_type_checker(faculty_code: str, name_parts: dict[str, str]) -> GroupType:
    if len(name_parts) == len(GROUP_NAME_PARTS_ASPIRANTES) or faculty_code == "АСП":
        return GROUP_TYPE_ASPIRANTES
    if name_parts.get("is_master_1") or name_parts.get("is_master_2"):
        return GROUP_TYPE_MASTERS
    return GROUP_TYPE_REGULAR


def _parse_group_name(pattern: re.Pattern, pattern_parts: tuple[str, ...], faculty_code: str, group_body: str) -> Group:
    try:
        found: tuple[str, ...] = re.findall(pattern, group_body)[0]
    except IndexError as _:
        raise UnHandlingGroupException(f"Неизвестный шаблон группы: {group_body}")

    if len(found) != len(pattern_parts):
        raise ValueError(f"Неверный шаблон для группы: ({found=}; {pattern_parts=}; {group_body=})")

    parsed: dict[str, str] = dict(zip(pattern_parts, found))

    note: str = parsed["note"]

    return Group(
        origin_name=f"{faculty_code}-{group_body}",
        faculty_code=faculty_code,
        course=int(parsed.get("course")) if parsed.get("course") else None,
        number=int(parsed["group_number"]),
        note=note if note else None,
        type=group_type_checker(faculty_code, parsed),
        subgroup_letter=parsed.get("subgroup_letter") if parsed.get("subgroup_letter") else None,
    )


def parse_group_by_name(group_name: str) -> Group:
    faculty_code, group_body = group_name.split("-", 1)

    if not faculty_code:
        raise ValueError(f"Факультет не определён для {group_name}")

    if faculty_code == "АСП":
        return _parse_group_name(GROUP_NAME_ASPIRANTES_PATTERN, GROUP_NAME_PARTS_ASPIRANTES, faculty_code, group_body)
    else:
        return _parse_group_name(GROUP_NAME_DEFAULT_PATTERN, GROUP_NAME_PARTS_DEFAULT, faculty_code, group_body)


async def fetch_json(session: ClientSession, url: str) -> str:
    async with session.get(url, timeout=REQUEST_TIMEOUT) as response:
        return await response.json()


def handle_lesson_times(lesson_time_data: list[dict[str, str]]) -> dict[int, LessonTime]:
    times: dict[int, LessonTime] = {}

    for lesson_num, lesson_time in enumerate(lesson_time_data):
        start, end = lesson_time.get("start"), lesson_time.get("end")

        if start is None or end is None:
            raise Exception(f"Нет информации о границах времени пары: {lesson_time}")

        start_hour, start_minutes = start.split(":")
        end_hour, end_minutes = end.split(":")

        times[lesson_num] = LessonTime(
            start=int(start_hour) * 60 + int(start_minutes),
            end=int(end_hour) * 60 + int(end_minutes),
        )

    return times


def determine_subject_type(subject_str: str) -> SubjectType:
    for subject_type, type_phrases in SUBJECT_TYPES.items():
        for phrase in type_phrases:
            if phrase.lower() in subject_str.lower():
                return subject_type
    return "unknown"


def clean_subject_name(subject_str: str, subject_type: SubjectType) -> str:
    for subject_type_phrase in SUBJECT_TYPES[subject_type]:
        subject_str = re.sub(
            rf"\s*\({re.escape(subject_type_phrase)}\)\s*", "", subject_str,
            flags=re.IGNORECASE
        )

    return subject_str


def parse_teacher_name(teacher_str: str) -> list[tuple[str, str]]:
    teachers = re.findall(r'([^,(]+?)\s*\(([^()]*(?:\(.*?\)[^()]*)*)\)', teacher_str)

    return [(teacher_name.strip(), teacher_role.strip()) for teacher_name, teacher_role in teachers]


def handle_teachers(teachers_str: str) -> set[Teacher]:
    teachers: set[Teacher] = set()
    teachers_infos: list[tuple[str, str]] = re.findall(r'([^,(]+?)\s*\(([^()]*(?:\(.*?\)[^()]*)*)\)', teachers_str)

    for teacher_info in teachers_infos:
        teachers.add(
            Teacher(
                fullname=teacher_info[0].strip(),
                role=teacher_info[1].strip(),
            )
        )

    return teachers


def handle_lesson(lesson_info: dict[str, Any], times: dict[int, LessonTime]) -> Lesson:
    lesson_number: Optional[int] = lesson_info.get("lessonNumber")
    week_day: Optional[int] = lesson_info.get("weekDay")
    week_mark: Optional[WeekMark] = lesson_info.get("weekMark")

    size_x: Optional[int] = lesson_info.get("sizeX")
    position_x: Optional[int] = lesson_info.get("positionX")

    texts: list[Optional[list[str]]] = lesson_info.get("texts")

    if any(map(lambda x: x is None, [
        lesson_number, week_day, week_mark, size_x, position_x, texts
    ])) or len(texts) < 4:
        if SKIP_BAD_LESSONS:
            raise SkipLessonException
        raise KeyError(f"У пары нет нужной информации: {lesson_info}")

    subgroup: Optional[int] = position_x if size_x == 2 else None

    subject: str = texts[1]
    teachers_str: str = texts[2]
    place: str = texts[3]

    subject_type: SubjectType = determine_subject_type(subject)
    subject_name: str = clean_subject_name(subject, subject_type)

    return Lesson(
        lesson_number=lesson_number,
        week_day=week_day,
        week_mark=week_mark,
        time_start=times[lesson_number].start,
        time_end=times[lesson_number].end,
        subject_name=subject_name,
        subject_type=subject_type,
        place=place,
        teachers=tuple(handle_teachers(teachers_str)),
        subgroup=subgroup,
    )


def handle_schedule_response(json_page: dict[str, Union[str, dict[str, Any]]]) -> Optional[tuple[Lesson]]:
    message: Optional[str] = json_page.get("message")

    if message is not None:
        # В ответе API есть опечатка: вместо "не найдено" написано "на найдено"
        if "расписание на найдено" in message.lower() or "расписание не найдено" in message.lower():
            return None

    lesson_time_data: Optional[list[dict[str, str]]] = json_page.get("lessonTimeData")

    if lesson_time_data is None:
        raise KeyError(f"Нет информации о времени пар у группы: {json_page}")

    lessons_containers: Optional[list[dict[str, Any]]] = json_page.get("lessonsContainers")

    if lessons_containers is None:
        raise KeyError(f"Error: {json_page}")

    times: dict[int, LessonTime] = handle_lesson_times(lesson_time_data)

    #  `set`, чтобы убрать дубликаты
    lessons: set[Lesson] = set()
    for lesson_info in lessons_containers:
        try:
            lesson: Lesson = handle_lesson(lesson_info, times)
        except SkipLessonException:
            continue

        lessons.add(lesson)

    return tuple(lessons)


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
