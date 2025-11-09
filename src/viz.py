import matplotlib.pyplot as plt

def plot_slice(df):
    if df is None or df.empty:
        return None
    fig, ax = plt.subplots()
    if "balls_rem" in df.columns and "y_runs_to_end_no_extras" in df.columns:
        ax.scatter(df["balls_rem"], df["y_runs_to_end_no_extras"], s=10)
        ax.set_xlabel("balls_rem")
        ax.set_ylabel("runs_to_end")
        ax.set_title("Nearby training states")
    else:
        ax.text(0.5, 0.5, "no slice columns", ha="center")
    return fig
