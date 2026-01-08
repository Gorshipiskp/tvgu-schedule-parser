import asyncio
from collections import defaultdict
from typing import Union, Any

import aiohttp
from aiohttp import ClientSession, TCPConnector

from config import API_ALL_GROUPS, API_SCHEDULE, PAIRS_SCHEDULE_TYPE, MAX_CONCURRENT_REQUESTS
from misc import parse_group_by_name, Group, UnHandlingGroupException, fetch_json, handle_schedule_response, Lesson


async def get_all_groups_by_faculty_key(show_warnings: bool = False) -> dict[str, list[Group]]:
    try:
        # resp: Response = aiohttp.request(API_ALL_GROUPS)
        async with aiohttp.ClientSession() as session:
            jsonned: dict[str, list[str, str]] = await fetch_json(session, API_ALL_GROUPS)
    except Exception as e:
        raise e

    if "groups" not in jsonned:
        raise Exception(f"Error: {jsonned}")

    all_groups: defaultdict[list] = defaultdict(list)

    for group_req in jsonned["groups"]:
        group_name: str = group_req["groupName"]

        try:
            group: Group = parse_group_by_name(group_name)
        except UnHandlingGroupException:
            if show_warnings:
                print("Неизвестный шаблон группы:", group_name)
            continue

        all_groups[group.faculty_code].append(group)
    return all_groups


async def get_groups_schedules(groups: list[Group]) -> dict[Group, tuple[Lesson]]:
    connector: TCPConnector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)

    async with ClientSession(connector=connector) as session:
        tasks: list[asyncio.Task] = [
            fetch_json(session, API_SCHEDULE.format(group.origin_name, PAIRS_SCHEDULE_TYPE))
            for group in groups
        ]
        schedule_pages: list[dict[str, Union[str, dict[str, Any]]]] = await asyncio.gather(*tasks)

    #  Не беспокоимся: датакласс (Group) с параметром `frozen=True` генерирует `self.__hash__` сам, а значит может
    #  использоваться в качестве ключа словаря
    # `asyncio.gather` сохраняет порядок, несмотря на конкурентность выполнения запросов
    return dict(zip(groups, list(map(handle_schedule_response, schedule_pages))))
