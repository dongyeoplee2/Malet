"""Generate example figures from real CIFAR-10 ResNet20 experiment logs.

Run with: pytest tests/test_resnet20_figures.py -m figures
Generated figures are saved to docs/_static/figures/

All figures use the malet default style:
- figsize 7×7, frame_width 2.5, dashed grid
- diamond markers (D), linewidth 4, markersize 10
- fill_between error bands alpha 0.3
- fontsize 22 for labels/titles, tick labelsize 25, legend fontsize 20
"""

import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib import colors as mcolors
from matplotlib.animation import ArtistAnimation, PillowWriter

from malet.plot_utils.data_processor import avgbest_df, select_df
from malet.plot_utils.plot_drawer import (
    ax_draw_bar,
    ax_draw_best_stared_curve,
    ax_draw_curve,
    ax_draw_heatmap,
    ax_draw_scatter,
    ax_draw_scatter_heat,
)

matplotlib.use("Agg")

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "_static", "figures")

# ── Malet default style constants ─────────────────────────────────────
FONT_SIZE = 22
TICK_SIZE = 25
LEGEND_SIZE = 20
FRAME_WIDTH = 2.5
LINEWIDTH = 4
MARKER = "D"
MARKERSIZE = 10
MARKEVERY = 1
SCATTER_MARKERSIZE = 30
FILL_ALPHA = 0.3
FIG_SIZE = 7
MARKERS = ["D", "o", ">", "X", "s", "v", "^", "<", "p", "P", "*", "+", "x"]


def _style_ax(ax):
    """Apply malet default axis styling."""
    for spine in ["top", "bottom", "left", "right"]:
        ax.spines[spine].set_linewidth(FRAME_WIDTH)
    ax.tick_params(axis="both", which="major", labelsize=TICK_SIZE,
                   direction="in", length=5)
    ax.grid(True, linestyle="--")


def save_fig(fig, name, fmt="png"):
    """Save figure and close."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIGURES_DIR, f"{name}.{fmt}"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def _to_single_index(df, keep_level):
    """Drop all index levels except keep_level."""
    drop_levels = [n for n in df.index.names if n != keep_level]
    return df.reset_index(drop_levels, drop=True).sort_index()


def _keep_index_levels(df, keep_levels):
    """Drop all index levels except the given ones."""
    drop_levels = [n for n in df.index.names if n not in keep_levels]
    return df.reset_index(drop_levels, drop=True).sort_index()


# ── Curve Plots ─────────────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20CurvePlots:
    """Training curve figures from real ResNet20 experiments."""

    def test_baseline_vs_sam_val_accuracy(self, resnet20_log):
        """Compare baseline (ADMM) vs SAM+SAFE with shaded std error."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric()
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5, "sp": 0.9})

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))

        base_df = select_df(df, {"grad_type": "grad", "optim": "admm", "rho": 0.0})
        base_df = avgbest_df(base_df, "metric_value", avg_over={"seed"}, best_at_max=True)
        base_df = _to_single_index(base_df, "step")
        ax_draw_curve(ax, base_df, label="Baseline (ADMM)", color="tab:blue",
                      annotate=False, std_plot="fill")

        sam_df = select_df(df, {"grad_type": "sam_grad", "optim": "safe"})
        sam_df = avgbest_df(sam_df, "metric_value", avg_over={"seed"}, best_over={"rho"}, best_at_max=True)
        sam_df = _to_single_index(sam_df, "step")
        ax_draw_curve(ax, sam_df, label="SAM+SAFE (best ρ)", color="tab:red",
                      annotate=False, std_plot="fill")

        ax.set_xlabel("Epoch", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        ax.set_title("ADMM vs SAFE", fontsize=FONT_SIZE)
        ax.legend(fontsize=LEGEND_SIZE)
        _style_ax(ax)
        save_fig(fig, "resnet20_baseline_vs_sam")

    def test_train_val_gap(self, resnet20_log):
        """Train vs val accuracy on the same axes — generalization gap."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric()
        df = select_df(df, {"noise": 0.5, "sp": 0.9, "optim": "safe", "grad_type": "sam_grad"})

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        for metric_name, sty in {
            "train_accuracy": {"color": "tab:blue", "linestyle": "--", "label": "Train Accuracy"},
            "val_accuracy": {"color": "tab:red", "linestyle": "-", "label": "Val Accuracy"},
        }.items():
            p_df = select_df(df, {"metric": metric_name})
            p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_over={"rho"}, best_at_max=True)
            p_df = _to_single_index(p_df, "step")
            ax_draw_curve(ax, p_df, annotate=False, std_plot="fill", **sty)

        ax.set_xlabel("Epoch", fontsize=FONT_SIZE)
        ax.set_ylabel("Accuracy", fontsize=FONT_SIZE)
        ax.set_title("Train vs Val Accuracy", fontsize=FONT_SIZE)
        ax.legend(fontsize=LEGEND_SIZE)
        _style_ax(ax)
        save_fig(fig, "resnet20_train_val_gap")


# ── Best-Starred Curves (HP x-axis) ───────────────────────────────────


@pytest.mark.figures
class TestResNet20StarPlots:
    """Best-starred curve with hyperparameter on x-axis."""

    def test_star_rho_multi_sparsity(self, resnet20_log):
        """Val_accuracy vs rho with best starred, one line per sparsity."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5,
                            "optim": "safe", "grad_type": "sam_grad"})

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        # Sequential blue palette for ordered sparsity values
        blues = plt.cm.Blues
        sp_vals = [0.8, 0.9, 0.95]
        for i, sp in enumerate(sp_vals):
            p_df = select_df(df, {"sp": sp})
            p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)
            p_df = _to_single_index(p_df, "rho")
            color = blues(0.4 + 0.2 * i)
            ax_draw_best_stared_curve(
                ax, p_df, label=f"sp={sp}", best_at_max=True,
                color=color, annotate=False,
            )

        ax.set_xlabel("ρ", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        ax.set_title("Best ρ per Sparsity", fontsize=FONT_SIZE)
        ax.legend(fontsize=LEGEND_SIZE)
        _style_ax(ax)
        save_fig(fig, "resnet20_star_rho_sparsity")


# ── Bar Plots ───────────────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20BarPlots:
    """Bar chart figures."""

    def test_rho_bar(self, resnet20_log):
        """Bar chart comparing rho values."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5, "sp": 0.9,
                            "optim": "safe", "grad_type": "sam_grad"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)
        df = _to_single_index(df, "rho")

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax_draw_bar(ax, df, label="Val Accuracy", color="tab:blue", annotate=True)
        ax.set_xlabel("ρ", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        ax.set_title("Val Accuracy by ρ", fontsize=FONT_SIZE)
        _style_ax(ax)
        ax.grid(True, linestyle="--", axis="y")
        save_fig(fig, "resnet20_bar_rho")


# ── Heatmap Plots ───────────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20HeatmapPlots:
    """Heatmap figures."""

    def test_rho_vs_sparsity_heatmap(self, resnet20_log):
        """Heatmap of val_accuracy over rho × sparsity."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5,
                            "optim": "safe", "grad_type": "sam_grad"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)
        df = _keep_index_levels(df, ["rho", "sp"])

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax_draw_heatmap(ax, df, cmap="YlOrRd", annotate=True)
        ax.set_xlabel("ρ", fontsize=FONT_SIZE)
        ax.set_ylabel("Sparsity", fontsize=FONT_SIZE)
        ax.set_title("Val Accuracy: ρ vs Sparsity", fontsize=FONT_SIZE)
        _style_ax(ax)
        save_fig(fig, "resnet20_heatmap_rho_sp")


# ── Scatter Plots ───────────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20ScatterPlots:
    """Scatter plot figures."""

    def test_scatter_loss_vs_accuracy(self, resnet20_log):
        """2D scatter: train_loss vs val_accuracy at final epoch."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": ["train_loss", "val_accuracy"],
                            "noise": 0.5, "optim": "safe", "grad_type": "sam_grad"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax_draw_scatter(ax, df, y_fields=["train_loss", "val_accuracy"],
                        color="tab:red", markersize=SCATTER_MARKERSIZE)
        ax.set_xlabel("Train Loss", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        _style_ax(ax)
        save_fig(fig, "resnet20_scatter_loss_acc")

    def test_scatter_heat_three_metrics(self, resnet20_log):
        """3D scatter: train_loss vs val_accuracy, colored by train_accuracy."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": ["train_loss", "val_accuracy", "train_accuracy"],
                            "noise": 0.5, "optim": "safe", "grad_type": "sam_grad"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)

        norm = mcolors.Normalize(
            df[df.index.get_level_values("metric") == "train_accuracy"]["metric_value"].min(),
            df[df.index.get_level_values("metric") == "train_accuracy"]["metric_value"].max(),
        )

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax_draw_scatter_heat(ax, df, y_fields=["train_loss", "val_accuracy", "train_accuracy"],
                             cmap="magma", markersize=SCATTER_MARKERSIZE, norm=norm)
        ax.set_xlabel("Train Loss", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap="magma"), ax=ax,
                     label="Train Accuracy")
        _style_ax(ax)
        save_fig(fig, "resnet20_scatter_heat")

    def test_multiplot_scatter_by_sparsity(self, resnet20_log):
        """1×3 multi-plot scatter: one per sparsity level."""
        log, _ = resnet20_log
        sparsities = [0.8, 0.9, 0.95]
        fig, axes = plt.subplots(1, 3, figsize=(3 * FIG_SIZE, FIG_SIZE),
                                 sharex=True, sharey=True)

        for ax, sp in zip(axes, sparsities):
            df = log.melt_and_explode_metric(step=-1)
            df = select_df(df, {"metric": ["train_loss", "val_accuracy"],
                                "noise": 0.5, "sp": sp,
                                "optim": "safe", "grad_type": "sam_grad"})
            df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)
            ax_draw_scatter(ax, df, y_fields=["train_loss", "val_accuracy"],
                            color="tab:blue", markersize=SCATTER_MARKERSIZE)
            ax.set_title(f"sp={sp}", fontsize=FONT_SIZE)
            ax.set_xlabel("Train Loss", fontsize=FONT_SIZE)
            _style_ax(ax)

        axes[0].set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        fig.tight_layout()
        save_fig(fig, "resnet20_multiplot_scatter")


# ── Multi-Line Plots ───────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20MultiLine:
    """Multi-line figures with continuous colormap."""

    def test_multiline_rho(self, resnet20_log):
        """Multiple rho values with continuous colormap (sequential blues)."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric()
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5, "sp": 0.9,
                            "optim": "safe", "grad_type": "sam_grad"})

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        cmap = plt.cm.Blues
        rho_values = sorted(set(df.index.get_level_values("rho")))

        for i, rho in enumerate(rho_values):
            try:
                p_df = select_df(df, {"rho": rho})
                p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)
                p_df = _to_single_index(p_df, "step")
                color = cmap(0.3 + 0.7 * i / max(1, len(rho_values) - 1))
                ax_draw_curve(ax, p_df, label=f"ρ={rho}", color=color,
                              annotate=False, std_plot="none")
            except Exception:
                continue

        ax.set_xlabel("Epoch", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        ax.legend(fontsize=LEGEND_SIZE, ncol=2)
        _style_ax(ax)
        save_fig(fig, "resnet20_multiline_rho")


# ── Multi-Plot Subplots ────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20MultiPlot:
    """Multi-subplot figures — analogous to crf() mode."""

    def test_multiplot_sparsity(self, resnet20_log):
        """1×3 subplot grid: curves by sparsity with multi-line rho."""
        log, _ = resnet20_log
        df = log.melt_and_explode_metric()
        df = select_df(df, {"metric": "val_accuracy", "noise": 0.5,
                            "optim": "safe", "grad_type": "sam_grad"})

        sparsities = [0.8, 0.9, 0.95]
        fig, axes = plt.subplots(1, 3, figsize=(3 * FIG_SIZE, FIG_SIZE), sharey=True)
        cmap = plt.cm.Blues
        rho_values = sorted(set(df.index.get_level_values("rho")))

        for ax, sp in zip(axes, sparsities):
            sp_df = select_df(df, {"sp": sp})
            for j, rho in enumerate(rho_values):
                try:
                    p_df = select_df(sp_df, {"rho": rho})
                    p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)
                    p_df = _to_single_index(p_df, "step")
                    color = cmap(0.3 + 0.7 * j / max(1, len(rho_values) - 1))
                    ax_draw_curve(ax, p_df, label=f"ρ={rho}", color=color,
                                  annotate=False, std_plot="none")
                except Exception:
                    continue
            ax.set_xlabel("Epoch", fontsize=FONT_SIZE)
            ax.set_title(f"sp={sp}", fontsize=FONT_SIZE)
            _style_ax(ax)
            ax.legend(fontsize=12, ncol=2)

        axes[0].set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        fig.tight_layout()
        save_fig(fig, "resnet20_multiplot_sparsity")


# ── Animation ──────────────────────────────────────────────────────────


@pytest.mark.figures
class TestResNet20Animation:
    """Animated GIF figures — x-axis is a hyperparameter, animation over time.

    Style matches malet GIF output:
    - Animation label "step=N" at (0.0, 1.01) in axes coords
    - fontsize 22, ha="left", va="bottom"
    """

    def test_animation_curve_over_epochs(self, resnet20_log):
        """Animate val_accuracy vs rho (HP x-axis) over epochs (ani=step).

        Analogous to: curve-rho-val_accuracy -mlf sp -ani step
        Multi-line by sparsity (sequential blues), animated over training steps.
        """
        log, _ = resnet20_log
        df_full = log.melt_and_explode_metric()
        df_full = select_df(df_full, {"metric": "val_accuracy", "noise": 0.5,
                                      "optim": "safe", "grad_type": "sam_grad"})

        all_steps = sorted(set(df_full.index.get_level_values("step")))
        ani_steps = [s for s in all_steps if s >= 50 and s % 20 == 0]

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax.set_xlabel("ρ", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        _style_ax(ax)

        sp_vals = [0.8, 0.9, 0.95]
        blues = plt.cm.Blues

        frames = []
        for step in ani_steps:
            frame_artists = []
            step_df = select_df(df_full, {"step": step})
            for i, sp in enumerate(sp_vals):
                try:
                    p_df = select_df(step_df, {"sp": sp})
                    p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)
                    p_df = _to_single_index(p_df, "rho")
                    y_field = list(p_df)[0]
                    x_vals, y_vals = map(np.array, zip(*dict(p_df[y_field]).items()))
                    color = blues(0.4 + 0.2 * i)
                    line = ax.plot(x_vals, y_vals, color=color,
                                  linewidth=LINEWIDTH, marker=MARKER, markersize=MARKERSIZE)
                    frame_artists += line
                except Exception:
                    continue
            # Animation label in malet style
            txt = ax.text(0.0, 1.01, f"step={step}", fontsize=FONT_SIZE,
                          ha="left", va="bottom", transform=ax.transAxes)
            frame_artists.append(txt)
            frames.append(frame_artists)

        if frames:
            anim = ArtistAnimation(fig, frames, interval=400, repeat=True)
            os.makedirs(FIGURES_DIR, exist_ok=True)
            gif_path = os.path.join(FIGURES_DIR, "resnet20_animation_curve.gif")
            anim.save(gif_path, writer=PillowWriter(fps=3))
            plt.close(fig)
            assert os.path.isfile(gif_path)
        else:
            plt.close(fig)

    def test_animation_scatter_over_epochs(self, resnet20_log):
        """Animate scatter plot (train_loss vs val_accuracy) over epochs.

        Analogous to: scatter--train_loss val_accuracy -mlf sp -ani step
        x,y = metrics (not time), animation = step, multi-line by sparsity.
        """
        log, _ = resnet20_log
        df_full = log.melt_and_explode_metric()
        df_full = select_df(df_full, {"metric": ["train_loss", "val_accuracy"],
                                      "noise": 0.5, "optim": "safe", "grad_type": "sam_grad"})

        all_steps = sorted(set(df_full.index.get_level_values("step")))
        ani_steps = [s for s in all_steps if s >= 10 and s % 20 == 0]

        fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        ax.set_xlabel("Train Loss", fontsize=FONT_SIZE)
        ax.set_ylabel("Val Accuracy", fontsize=FONT_SIZE)
        _style_ax(ax)

        sp_vals = [0.8, 0.9, 0.95]
        blues = plt.cm.Blues

        frames = []
        for step in ani_steps:
            frame_artists = []
            step_df = select_df(df_full, {"step": step})
            for i, sp in enumerate(sp_vals):
                try:
                    p_df = select_df(step_df, {"sp": sp})
                    p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)

                    loss_df = p_df[p_df.index.get_level_values("metric") == "train_loss"]
                    acc_df = p_df[p_df.index.get_level_values("metric") == "val_accuracy"]
                    losses = loss_df["metric_value"].values
                    accs = acc_df["metric_value"].values
                    color = blues(0.4 + 0.2 * i)
                    sc = ax.scatter(losses, accs, color=color, marker=MARKER,
                                   s=SCATTER_MARKERSIZE * 20, edgecolors="black", linewidths=0.5)
                    frame_artists.append(sc)
                except Exception:
                    continue
            txt = ax.text(0.0, 1.01, f"step={step}", fontsize=FONT_SIZE,
                          ha="left", va="bottom", transform=ax.transAxes)
            frame_artists.append(txt)
            frames.append(frame_artists)

        if frames:
            anim = ArtistAnimation(fig, frames, interval=400, repeat=True)
            os.makedirs(FIGURES_DIR, exist_ok=True)
            gif_path = os.path.join(FIGURES_DIR, "resnet20_animation_scatter.gif")
            anim.save(gif_path, writer=PillowWriter(fps=3))
            plt.close(fig)
            assert os.path.isfile(gif_path)
        else:
            plt.close(fig)

    def test_animation_multiplot_scatter(self, resnet20_log):
        """Animate multi-plot scatter (1×3 by sparsity) over epochs.

        Analogous to: scatter--train_loss val_accuracy -crf sp -ani step
        Each subplot is a scatter of train_loss vs val_accuracy for one sparsity,
        with points colored by rho (viridis continuous cmap), animated over steps.
        """
        log, _ = resnet20_log
        df_full = log.melt_and_explode_metric()
        df_full = select_df(df_full, {"metric": ["train_loss", "val_accuracy"],
                                      "noise": 0.5, "optim": "safe", "grad_type": "sam_grad"})

        all_steps = sorted(set(df_full.index.get_level_values("step")))
        ani_steps = [s for s in all_steps if s >= 10 and s % 25 == 0]

        sp_vals = [0.8, 0.9, 0.95]
        cmap = plt.cm.viridis

        fig, axes = plt.subplots(1, 3, figsize=(3 * FIG_SIZE, FIG_SIZE),
                                 sharex=True, sharey=True)
        for ax, sp in zip(axes, sp_vals):
            ax.set_title(f"sp={sp}", fontsize=FONT_SIZE)
            ax.set_xlabel("Train Loss", fontsize=FONT_SIZE)
            _style_ax(ax)
        axes[0].set_ylabel("Val Accuracy", fontsize=FONT_SIZE)

        frames = []
        for step in ani_steps:
            frame_artists = []
            step_df = select_df(df_full, {"step": step})
            for ax, sp in zip(axes, sp_vals):
                try:
                    p_df = select_df(step_df, {"sp": sp})
                    p_df = avgbest_df(p_df, "metric_value", avg_over={"seed"}, best_at_max=True)
                    rho_vals = sorted(set(p_df.index.get_level_values("rho")))

                    for j, rho in enumerate(rho_vals):
                        r_df = p_df[p_df.index.get_level_values("rho") == rho]
                        loss_df = r_df[r_df.index.get_level_values("metric") == "train_loss"]
                        acc_df = r_df[r_df.index.get_level_values("metric") == "val_accuracy"]
                        if len(loss_df) and len(acc_df):
                            color = cmap(j / max(1, len(rho_vals) - 1))
                            sc = ax.scatter(
                                loss_df["metric_value"].values,
                                acc_df["metric_value"].values,
                                color=color, marker=MARKER,
                                s=SCATTER_MARKERSIZE * 20, edgecolors="black", linewidths=0.5,
                            )
                            frame_artists.append(sc)
                except Exception:
                    continue
            # Animation label on first subplot only
            txt = axes[0].text(0.0, 1.01, f"step={step}", fontsize=FONT_SIZE,
                               ha="left", va="bottom", transform=axes[0].transAxes)
            frame_artists.append(txt)
            frames.append(frame_artists)

        if frames:
            anim = ArtistAnimation(fig, frames, interval=400, repeat=True)
            os.makedirs(FIGURES_DIR, exist_ok=True)
            gif_path = os.path.join(FIGURES_DIR, "resnet20_animation_multiplot_scatter.gif")
            anim.save(gif_path, writer=PillowWriter(fps=3))
            plt.close(fig)
            assert os.path.isfile(gif_path)
        else:
            plt.close(fig)
