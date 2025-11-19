from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Callable, Iterable, Sequence

import psycopg2


Transformer = Callable[[dict[str, object]], dict[str, object]]


@dataclass
class DomainConfig:
    table: str
    key_columns: Sequence[str]
    column_order: Sequence[str]
    transformer: Transformer | None = None


def read_csv_records(path: str | Path) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    with Path(path).open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cleaned = {k: (v.strip() if isinstance(v, str) and v.strip() else None) for k, v in row.items()}
            rows.append(cleaned)
    return rows


def chunk(records: Sequence[dict[str, object]], size: int = 100) -> Iterable[Sequence[dict[str, object]]]:
    for start in range(0, len(records), size):
        yield records[start : start + size]


def upsert_records(conn_uri: str, config: DomainConfig, records: Sequence[dict[str, object]]) -> None:
    if not records:
        return
    columns_sql = ", ".join(config.column_order)
    placeholders = ", ".join(["%s"] * len(config.column_order))
    update_sets = ", ".join([f"{col}=excluded.{col}" for col in config.column_order if col not in config.key_columns])
    conflict = ", ".join(config.key_columns)
    statement = f"INSERT INTO {config.table} ({columns_sql}) VALUES ({placeholders}) ON CONFLICT ({conflict}) DO UPDATE SET {update_sets}" if update_sets else f"INSERT INTO {config.table} ({columns_sql}) VALUES ({placeholders}) ON CONFLICT ({conflict}) DO NOTHING"

    with psycopg2.connect(conn_uri) as conn:
        with conn.cursor() as cur:
            for batch in chunk(records):
                params = [tuple(record.get(col) for col in config.column_order) for record in batch]
                cur.executemany(statement, params)


def load_domain(csv_path: str | Path, conn_uri: str, config: DomainConfig) -> int:
    records: list[dict[str, object]] = read_csv_records(csv_path)
    if config.transformer:
        records = [config.transformer(record.copy()) for record in records]
    upsert_records(conn_uri, config, records)
    return len(records)


def normalize_bool(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "t", "1", "yes", "y"}:
        return True
    if normalized in {"false", "f", "0", "no", "n"}:
        return False
    return None


def normalize_upper(value: object) -> str | None:
    if not value:
        return None
    return str(value).strip().upper()


def normalize_title(value: object) -> str | None:
    if not value:
        return None
    return str(value).strip().title()


def normalize_lower(value: object) -> str | None:
    if not value:
        return None
    return str(value).strip().lower()


def normalize_phone(value: object) -> str | None:
    if not value:
        return None
    chars = [ch for ch in str(value).strip() if ch.isdigit() or ch == "+"]
    return "".join(chars) if chars else None


def parse_date(value: object) -> datetime.date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_decimal(value: object) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (ValueError, ArithmeticError):
        return None


def parse_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


def count_rows(conn_uri: str, table: str) -> int:
    with psycopg2.connect(conn_uri) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            result = cur.fetchone()
            return int(result[0]) if result else 0