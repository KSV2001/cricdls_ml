from dataclasses import dataclass
from .data_io import load_dls_table, load_cricml_resource, load_balls_features
from .models import ResourceTable

@dataclass
class InferenceArtifacts:
    dls: ResourceTable
    cricml: ResourceTable
    balls_df: object

def load_artifacts() -> InferenceArtifacts:
    dls_tab = load_dls_table()
    cric_tab = load_cricml_resource()
    balls_df = load_balls_features()
    return InferenceArtifacts(
        dls=ResourceTable(dls_tab),
        cricml=ResourceTable(cric_tab),
        balls_df=balls_df,
    )

def infer_targets(art: InferenceArtifacts, first_innings_score: int, first_innings_overs_done: float,
                  first_innings_wickets: int, si_mode: str, si_balls_remaining: int, si_wickets_in_hand: int):
    if si_mode == "not_started":
        base_target = first_innings_score + 1
        return {
            "target_dls": base_target,
            "target_cricml": base_target,
            "slice_df": art.balls_df.head(0),
            "explanation": "Second innings not started. Target = 1 more than first innings.",
        }
    tgt_dls = art.dls.target_from_first_innings(first_innings_score, si_balls_remaining, si_wickets_in_hand)
    tgt_cric = art.cricml.target_from_first_innings(first_innings_score, si_balls_remaining, si_wickets_in_hand)

    df = art.balls_df
    if {"balls_rem", "wickets_rem"}.issubset(df.columns):
        lo = si_balls_remaining - 18
        hi = si_balls_remaining + 18
        mask = (df["balls_rem"].between(lo, hi)) & (df["wickets_rem"] == si_wickets_in_hand)
        slice_df = df.loc[mask].head(400)
    else:
        slice_df = df.head(0)

    expl = (f"DLS target uses resource at balls={si_balls_remaining}, wickets_in_hand={si_wickets_in_hand}. "
            f"Your method uses its own resource table exported from training.")

    return {
        "target_dls": int(tgt_dls),
        "target_cricml": int(tgt_cric),
        "slice_df": slice_df,
        "explanation": expl,
    }
