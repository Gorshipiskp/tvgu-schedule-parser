import argparse
import asyncio
import json
from dataclasses import dataclass
from typing import Optional, Coroutine, Any

from misc import Lesson, CustomEncoder, AllGroupsSchedules, Group
from schedule_requests import get_groups_schedules, get_all_groups_by_faculty_key


@dataclass(frozen=True, kw_only=True)
class Args:
    prettify: bool
    output: Optional[str]
    show_warnings: bool


def dump_schedules(schedules: AllGroupsSchedules, output_path: str, prettify: bool) -> None:
    schedules_for_json: dict[str, dict[str, Lesson]] = {
        faculty_code: {
            group.origin_name: schedule
            for group, schedule in group_schedules.items()
        }
        for faculty_code, group_schedules in schedules.items()
    }

    json.dump(
        schedules_for_json,
        open(output_path, "w+", encoding="UTF-8"),
        ensure_ascii=False,
        indent=2 if prettify else None,
        cls=CustomEncoder
    )


async def process_schedule(show_warnings: bool = True) -> AllGroupsSchedules:
    faculties_groups: dict[str, list[Group]] = await get_all_groups_by_faculty_key(show_warnings)

    groups_schedule_requests: list[Coroutine[Any, Any, dict[Group, tuple[Lesson]]]] = [
        get_groups_schedules(groups) for groups in faculties_groups.values()
    ]
    groups_schedules: list[dict[Group, tuple[Lesson]]] = await asyncio.gather(*groups_schedule_requests)

    return dict(zip(faculties_groups.keys(), groups_schedules))


async def main(args: Args) -> None:
    result_schedules: AllGroupsSchedules = await process_schedule(args.show_warnings)

    if args.output is not None:
        dump_schedules(result_schedules, args.output, args.prettify)


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Парсер расписания ТвГУ")

    parser.add_argument("-o", "--output", help="Путь к выходному файлу для экспорта расписаний")
    parser.add_argument("-p", "--prettify", action="store_true", help="Форматированный вывод JSON")
    parser.add_argument("-w", "--warnings", action="store_true", help="Показывать предупреждения")

    args: argparse.Namespace = parser.parse_args()

    return Args(
        prettify=args.prettify,
        output=args.output,
        show_warnings=args.warnings
    )


if __name__ == "__main__":
    # Python >=3.10

    asyncio.run(main(parse_args()))
