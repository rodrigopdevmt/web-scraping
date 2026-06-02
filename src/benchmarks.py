import time
import random
import string
from typing import Any


def _generate_dataset(rows: int) -> list[dict[str, Any]]:
    return [
        {
            "id": i,
            "nome": "".join(random.choices(string.ascii_letters, k=8)),
            "idade": random.randint(18, 80),
            "salario": round(random.uniform(1000, 20000), 2),
            "departamento": random.choice(["TI", "RH", "Vendas", "Marketing", "Financeiro"]),
            "ativo": random.choice([True, False]),
        }
        for i in range(rows)
    ]


def benchmark_groupby(rows: int = 100_000) -> dict[str, float]:
    data = _generate_dataset(rows)
    results: dict[str, float] = {}

    if _has_pandas():
        import pandas as pd

        df = pd.DataFrame(data)
        t0 = time.perf_counter()
        df.groupby("departamento")["salario"].mean()
        results["pandas"] = round(time.perf_counter() - t0, 4)

    if _has_polars():
        import polars as pl

        df = pl.DataFrame(data)
        t0 = time.perf_counter()
        df.group_by("departamento").agg(pl.col("salario").mean())
        results["polars"] = round(time.perf_counter() - t0, 4)

    return results


def benchmark_filter(rows: int = 100_000) -> dict[str, float]:
    data = _generate_dataset(rows)
    results: dict[str, float] = {}

    if _has_pandas():
        import pandas as pd

        df = pd.DataFrame(data)
        t0 = time.perf_counter()
        df[(df["idade"] > 30) & (df["salario"] > 5000)]
        results["pandas"] = round(time.perf_counter() - t0, 4)

    if _has_polars():
        import polars as pl

        df = pl.DataFrame(data)
        t0 = time.perf_counter()
        df.filter((pl.col("idade") > 30) & (pl.col("salario") > 5000))
        results["polars"] = round(time.perf_counter() - t0, 4)

    return results


def benchmark_read_write(rows: int = 100_000) -> dict[str, float]:
    import pandas as pd

    data = _generate_dataset(rows)
    df_pd = pd.DataFrame(data)
    results: dict[str, float] = {}

    t0 = time.perf_counter()
    df_pd.to_csv("/tmp/bench.csv", index=False)
    pd.read_csv("/tmp/bench.csv")
    results["pandas_csv"] = round(time.perf_counter() - t0, 4)

    t0 = time.perf_counter()
    df_pd.to_parquet("/tmp/bench.parquet", index=False)
    pd.read_parquet("/tmp/bench.parquet")
    results["pandas_parquet"] = round(time.perf_counter() - t0, 4)

    if _has_polars():
        import polars as pl

        df_pl = pl.DataFrame(data)
        t0 = time.perf_counter()
        df_pl.write_csv("/tmp/bench_pl.csv")
        pl.read_csv("/tmp/bench_pl.csv")
        results["polars_csv"] = round(time.perf_counter() - t0, 4)

        t0 = time.perf_counter()
        df_pl.write_parquet("/tmp/bench_pl.parquet")
        pl.read_parquet("/tmp/bench_pl.parquet")
        results["polars_parquet"] = round(time.perf_counter() - t0, 4)

    return results


def run_all_benchmarks(rows: int = 100_000) -> dict[str, Any]:
    print(f"Benchmarks com {rows:,} linhas...\n")
    results: dict[str, Any] = {}

    print("[1/3] GroupBy...")
    results["groupby"] = benchmark_groupby(rows)
    print(f"  Pandas: {results['groupby'].get('pandas', 'N/A')}s")
    print(f"  Polars: {results['groupby'].get('polars', 'N/A')}s")

    print("[2/3] Filtro...")
    results["filter"] = benchmark_filter(rows)
    print(f"  Pandas: {results['filter'].get('pandas', 'N/A')}s")
    print(f"  Polars: {results['filter'].get('polars', 'N/A')}s")

    print("[3/3] Leitura/Escrita...")
    results["read_write"] = benchmark_read_write(rows)
    for k, v in results["read_write"].items():
        print(f"  {k}: {v}s")

    return results


def _has_pandas() -> bool:
    try:
        import pandas  # noqa
        return True
    except ImportError:
        return False


def _has_polars() -> bool:
    try:
        import polars  # noqa
        return True
    except ImportError:
        return False
