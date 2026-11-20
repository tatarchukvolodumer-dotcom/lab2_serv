users: dict[int, dict] = {}
categories: dict[int, dict] = {}
records: dict[int, dict] = {}

_counters = {
    "user": 1,
    "category": 1,
    "record": 1,
}


def get_next_id(entity: str) -> int:
    current_id = _counters[entity]
    _counters[entity] += 1
    return current_id