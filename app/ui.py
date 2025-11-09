import gradio as gr
from src.inference import load_artifacts, infer_targets
from src.viz import plot_slice

_art = load_artifacts()

def run_app(fi_score, fi_overs_done, fi_wickets, si_mode, si_balls_remaining, si_wickets_in_hand):
    out = infer_targets(_art, int(fi_score), float(fi_overs_done), int(fi_wickets),
                        si_mode, int(si_balls_remaining), int(si_wickets_in_hand))
    fig = plot_slice(out["slice_df"])
    table_html = out["slice_df"].head(50).to_html(index=False) if not out["slice_df"].empty else ""
    return out["target_dls"], out["target_cricml"], table_html, fig, out["explanation"]

def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# CricML target viewer")
        with gr.Row():
            fi_score = gr.Number(label="First innings score", value=275)
            fi_overs_done = gr.Number(label="First innings overs done", value=50)
            fi_wickets = gr.Number(label="First innings wickets lost", value=6)
        with gr.Row():
            si_mode = gr.Radio(["not_started", "continuing"], value="continuing", label="Second innings mode")
            si_balls_remaining = gr.Number(label="2nd inns balls remaining", value=300)
            si_wickets_in_hand = gr.Number(label="2nd inns wickets in hand", value=10)

        btn = gr.Button("Compute targets")
        target_dls = gr.Number(label="Target by DLS")
        target_cricml = gr.Number(label="Target by your method")
        table = gr.HTML(label="Relevant training rows")
        plot = gr.Plot(label="Local training distribution")
        expl = gr.Textbox(label="Explanation", lines=3)

        btn.click(run_app,
                  inputs=[fi_score, fi_overs_done, fi_wickets, si_mode, si_balls_remaining, si_wickets_in_hand],
                  outputs=[target_dls, target_cricml, table, plot, expl])
    return demo
