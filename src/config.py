from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CFG = {
    "dls_table_path": str(ROOT / "data" / "dls_table.parquet"),
    "cricml_resource_path": str(ROOT / "data" / "cricml_resource.parquet"),
    "balls_features_path": str(ROOT / "data" / "balls_features.parquet"),
}

def load_config():
    cfg_path = ROOT / "data" / "config.json"
    if cfg_path.exists():
        with open(cfg_path, "r") as f:
            user = json.load(f)
        return {**DEFAULT_CFG, **user}
    return DEFAULT_CFG
