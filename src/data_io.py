import pandas as pd
from .config import load_config

def load_dls_table():
    cfg = load_config()
    return pd.read_parquet(cfg["dls_table_path"])

def load_cricml_resource():
    cfg = load_config()
    return pd.read_parquet(cfg["cricml_resource_path"])

def load_balls_features(sample=None):
    cfg = load_config()
    df = pd.read_parquet(cfg["balls_features_path"])
    if sample is not None:
        df = df.sample(n=sample, random_state=42)
    return df
