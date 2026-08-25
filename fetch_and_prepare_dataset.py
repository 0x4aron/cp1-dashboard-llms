"""Baixa e normaliza uma cópia local do Open LLM Leaderboard.

Fonte: https://huggingface.co/datasets/open-llm-leaderboard/contents
O script usa a API pública de visualização do Hugging Face e registra a data de
extração. Execute-o novamente somente quando quiser atualizar o recorte.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd


DATASET = "open-llm-leaderboard/contents"
API_URL = "https://datasets-server.huggingface.co/rows"
OUTPUT = Path("data/llm_leaderboard.csv")
METADATA = Path("data/source_metadata.json")
PAGE_SIZE = 100


def fetch_page(offset: int) -> dict:
    query = urlencode(
        {"dataset": DATASET, "config": "default", "split": "train", "offset": offset, "length": PAGE_SIZE}
    )
    with urlopen(f"{API_URL}?{query}", timeout=60) as response:
        return json.load(response)


def fetch_all_rows() -> list[dict]:
    first_page = fetch_page(0)
    total_rows = first_page["num_rows_total"]
    rows = [item["row"] for item in first_page["rows"]]
    print(f"Baixando {total_rows} registros da fonte pública…")

    for offset in range(PAGE_SIZE, total_rows, PAGE_SIZE):
        page = fetch_page(offset)
        rows.extend(item["row"] for item in page["rows"])
        print(f"  {min(offset + PAGE_SIZE, total_rows)}/{total_rows}")
    return rows


def normalize(rows: list[dict]) -> pd.DataFrame:
    raw = pd.DataFrame(rows)
    normalized = pd.DataFrame(
        {
            "model_name": raw["fullname"],
            "organization": raw["fullname"].str.split("/", n=1).str[0],
            "parameters_b": raw["#Params (B)"],
            "average_score": raw["Average ⬆️"],
            "benchmark_ifeval": raw["IFEval"],
            "benchmark_bbh": raw["BBH"],
            "benchmark_math_lvl5": raw["MATH Lvl 5"],
            "benchmark_gpqa": raw["GPQA"],
            "benchmark_musr": raw["MUSR"],
            "benchmark_mmlu_pro": raw["MMLU-PRO"],
            "license": raw["Hub License"].fillna("não informado"),
            "release_date": raw["Upload To Hub Date"],
            "co2_cost_kg": raw["CO₂ cost (kg)"],
            "model_type": raw["Type"],
        }
    )
    numeric = [column for column in normalized.columns if column.startswith("benchmark_")]
    numeric.extend(["parameters_b", "average_score", "co2_cost_kg"])
    for column in numeric:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")
    normalized = normalized.drop_duplicates(subset="model_name")
    return normalized


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    rows = fetch_all_rows()
    dataset = normalize(rows)
    dataset.to_csv(OUTPUT, index=False)
    metadata = {
        "source_dataset": DATASET,
        "source_url": "https://huggingface.co/datasets/open-llm-leaderboard/contents",
        "api_url": API_URL,
        "extracted_at_utc": datetime.now(UTC).isoformat(),
        "raw_records": len(rows),
        "normalized_records": len(dataset),
        "notes": "A base mede benchmarks gerais; não representa validação específica em domínio financeiro.",
    }
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Base salva em {OUTPUT} ({len(dataset)} linhas).")
    print(f"Metadados salvos em {METADATA}.")


if __name__ == "__main__":
    main()
