import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

TMP = Path("/tmp/estudo")
TMP.mkdir(parents=True, exist_ok=True)


def _get_pandas():
    try:
        import pandas as pd
        return pd
    except ImportError:
        return None


def to_csv(data: list[dict[str, Any]], path: str = str(TMP / "dados.csv")) -> str:
    with open(path, "w", newline="", encoding="utf-8") as f:
        if data:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)
    return path


def to_json(data: list[dict[str, Any]], path: str = str(TMP / "dados.json")) -> str:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    return path


def to_parquet(
    data: list[dict[str, Any]], path: str = str(TMP / "dados.parquet")
) -> Optional[str]:
    pd = _get_pandas()
    if not pd:
        return None
    df = pd.DataFrame(data)
    df.to_parquet(path, index=False)
    return path


def read_csv(path: str) -> list[dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_parquet(path: str) -> Optional[list[dict[str, Any]]]:
    pd = _get_pandas()
    if not pd:
        return None
    df = pd.read_parquet(path)
    return df.to_dict(orient="records")


def duckdb_query(query: str, params: Optional[list[Any]] = None) -> Optional[list[dict[str, Any]]]:
    try:
        import duckdb
    except ImportError:
        return None
    conn = duckdb.connect()
    try:
        result = conn.execute(query, params or [])
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception:
        return None
    finally:
        conn.close()


def sqlite_execute(db_path: str, query: str, params: Optional[list[Any]] = None) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(query, params or [])
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def sqlite_import_csv(db_path: str, csv_path: str, table: str) -> int:
    data = read_csv(csv_path)
    if not data:
        return 0

    conn = sqlite3.connect(db_path)
    try:
        columns = ", ".join(data[0].keys())
        placeholders = ", ".join("?" for _ in data[0])
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
        rows = [list(row.values()) for row in data]
        conn.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def duckdb_import_csv(csv_path: str, table: str = "dados") -> Optional[int]:
    try:
        import duckdb
    except ImportError:
        return None
    conn = duckdb.connect()
    try:
        conn.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{csv_path}')")
        result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return result[0] if result else 0
    except Exception:
        return 0
    finally:
        conn.close()
