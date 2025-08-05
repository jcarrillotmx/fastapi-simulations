import strawberry
from typing import List


@strawberry.type
class Reading:
    name: str
    value: float
    unit: str
    status: str


@strawberry.type
class ReadingRecord:
    timestamp: str
    readings: List[Reading]
