import json
from pathlib import Path
from src.storage import to_csv, to_json, read_csv, sqlite_execute, sqlite_import_csv


SAMPLE = [{"nome": "Alice", "idade": 30}, {"nome": "Bob", "idade": 25}]


class TestCSV:
    def test_write_and_read(self):
        path = to_csv(SAMPLE)
        data = read_csv(path)
        assert len(data) == 2
        assert data[0]["nome"] == "Alice"

    def test_empty(self):
        path = to_csv([])
        data = read_csv(path)
        assert data == []


class TestJSON:
    def test_write(self):
        path = to_json(SAMPLE)
        with open(path) as f:
            data = json.load(f)
        assert len(data) == 2
        assert data[0]["nome"] == "Alice"

    def test_empty(self):
        path = to_json([])
        with open(path) as f:
            data = json.load(f)
        assert data == []


class TestSQLite:
    def test_import_and_query(self):
        db = "/tmp/test_estudo.db"
        csv_path = to_csv(SAMPLE)
        sqlite_import_csv(db, csv_path, "pessoas")
        rows = sqlite_execute(db, "SELECT * FROM pessoas ORDER BY nome")
        assert len(rows) == 2
        assert rows[0]["nome"] == "Alice"
        Path(db).unlink(missing_ok=True)
