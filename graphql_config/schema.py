import strawberry
from sqlalchemy import text
from typing import List

from graphql_config.types import Reading, ReadingRecord
from config.db import SessionLocal


@strawberry.type
class Query:
    @strawberry.field
    def get_readings_by_range(
        self, table: str, desde: str, hasta: str
    ) -> List[ReadingRecord]:
        session = SessionLocal()
        try:
            sql = text(f"""
                SELECT * FROM {table}
                WHERE timestamp BETWEEN :desde AND :hasta
                ORDER BY timestamp ASC
            """)
            result = session.execute(
                sql, {"desde": desde, "hasta": hasta}
            ).mappings().all()  # ✅ Usamos .mappings() para acceder como dict

            readings = []
            for row in result:
                reading_items = []
                for i in range(1, 11):
                    name = row.get(f"name_{i}")
                    if name:
                        reading_items.append(Reading(
                            name=name,
                            value=row.get(f"channel_{i}", 0),
                            unit=row.get(f"unit_{i}", ""),
                            status=row.get(f"state_{i}", "")
                        ))
                readings.append(ReadingRecord(
                    timestamp=str(row["timestamp"]),  # por si es datetime
                    readings=reading_items
                ))
            return readings
        finally:
            session.close()


schema = strawberry.Schema(query=Query)
