import math
import pandas as pd

BALLS_PER_OVER = 6
FULL_RESOURCE = 100.0

class ResourceTable:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_resource(self, balls_remaining: int, wickets_in_hand: int) -> float:
        overs_left = max(int(balls_remaining // BALLS_PER_OVER), 0)
        overs_left = min(overs_left, int(self.df.index.max()))
        wickets_lost = 10 - int(wickets_in_hand)
        wickets_lost = max(0, min(wickets_lost, 9))
        return float(self.df.loc[overs_left, str(wickets_lost)])

    def target_from_first_innings(self, first_innings_score: int,
                                  balls_remaining: int,
                                  wickets_in_hand: int) -> int:
        r2 = self.get_resource(balls_remaining, wickets_in_hand)
        return math.floor(first_innings_score * (r2 / FULL_RESOURCE)) + 1
