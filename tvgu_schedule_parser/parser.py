import asyncio
from typing import Coroutine, Any

from .misc import AllGroupsSchedules, Group, Lesson
from .schedule_requests import get_groups_schedules, get_all_groups_by_faculty_key


async def get_all_tvgu_schedules(show_warnings: bool = True) -> AllGroupsSchedules:
    faculties_groups: dict[str, list[Group]] = await get_all_groups_by_faculty_key(show_warnings)

    groups_schedule_requests: list[Coroutine[Any, Any, dict[Group, tuple[Lesson]]]] = [
        get_groups_schedules(groups) for groups in faculties_groups.values()
    ]
    groups_schedules: list[dict[Group, tuple[Lesson]]] = await asyncio.gather(*groups_schedule_requests)

    return dict(zip(faculties_groups.keys(), groups_schedules))
