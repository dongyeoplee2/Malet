"""Tests that generate example figures for documentation.

Run with: pytest tests/test_plot_figures.py -m figures
Generated figures are saved to docs/_static/figures/
"""

import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from malet.experiment import ExperimentLog
from malet.plot_utils.data_processor import avgbest_df, select_df
from malet.plot_utils.plot_drawer import (
    ax_draw_bar,
    ax_draw_best_stared_curve,
    ax_draw_curve,
    ax_draw_heatmap,
    ax_draw_scatter,
)
from malet.plot_utils.utils import ax_styler

matplotlib.use("Agg")

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "_static", "figures")


def save_fig(fig, name, fmt="png"):
    """Save figure and close."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIGURES_DIR, f"{name}.{fmt}"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def _prepare_curve_df(log, optimizer, metric="val_accuracy"):
    """Prepare a single-index df ready for ax_draw_curve."""
    df = log.melt_and_explode_metric()
    df = select_df(df, {"metric": metric, "optimizer": optimizer})
    df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_over={"lr"}, best_at_max=True)
    # Drop everything except step as index
    drop_levels = [n for n in df.index.names if n != "step"]
    df = df.reset_index(drop_levels, drop=True).sort_index()
    return df


# ── Figure tests ─────────────────────────────────────────────────────────


@pytest.mark.figures
class TestCurvePlots:
    """Generate curve plot figures."""

    def test_basic_curve(self, sample_log):
        """Basic line plot of val_accuracy over steps for each optimizer."""
        log, _ = sample_log

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ["#1f77b4", "#ff7f0e"]

        for i, opt in enumerate(["sgd", "adam"]):
            p_df = _prepare_curve_df(log, opt)
            ax_draw_curve(ax, p_df, label=opt.upper(), color=colors[i], annotate=False, markersize=6)

        ax.set_xlabel("Step", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Validation Accuracy over Training Steps", fontsize=18)
        ax.legend(fontsize=14)
        ax.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig, "curve_basic")

    def test_curve_with_std(self, sample_log):
        """Curve with fill-between showing standard error across seeds."""
        log, _ = sample_log
        p_df = _prepare_curve_df(log, "adam")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax_draw_curve(ax, p_df, label="Adam (fill)", std_plot="fill", color="#1f77b4", annotate=False, markersize=6)

        ax.set_xlabel("Step", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Curve with Standard Error (fill)", fontsize=18)
        ax.legend(fontsize=14)
        ax.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig, "curve_std_fill")

    def test_curve_std_bar(self, sample_log):
        """Curve with error bars."""
        log, _ = sample_log
        p_df = _prepare_curve_df(log, "adam")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax_draw_curve(ax, p_df, label="Adam (error bars)", std_plot="bar", color="#ff7f0e", annotate=False, markersize=6)

        ax.set_xlabel("Step", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Curve with Error Bars", fontsize=18)
        ax.legend(fontsize=14)
        ax.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig, "curve_std_bar")

    def test_curve_best_starred(self, sample_log):
        """Curve with star marker on the best point."""
        log, _ = sample_log
        p_df = _prepare_curve_df(log, "adam")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax_draw_best_stared_curve(
            ax, p_df, label="Adam", best_at_max=True, color="#2ca02c", annotate=False, markersize=8
        )

        ax.set_xlabel("Step", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Curve with Best Point Starred", fontsize=18)
        ax.legend(fontsize=14)
        ax.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig, "curve_best_starred")


@pytest.mark.figures
class TestBarPlots:
    """Generate bar plot figures."""

    def test_bar_chart(self, sample_log):
        """Bar chart comparing optimizers at last step."""
        log, _ = sample_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": "val_accuracy"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_over={"lr"}, best_at_max=True)
        drop_levels = [n for n in df.index.names if n != "optimizer"]
        df = df.reset_index(drop_levels, drop=True).sort_index()

        fig, ax = plt.subplots(figsize=(7, 5))
        ax_draw_bar(ax, df, label="Val Accuracy", color="#1f77b4", annotate=True)

        ax.set_xlabel("Optimizer", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Optimizer Comparison (Last Epoch)", fontsize=18)
        ax.grid(True, linestyle="--", alpha=0.3, axis="y")
        save_fig(fig, "bar_optimizer")


@pytest.mark.figures
class TestHeatmapPlots:
    """Generate heatmap figures."""

    def test_heatmap(self, sample_log):
        """Heatmap of lr vs optimizer."""
        log, _ = sample_log
        df = log.melt_and_explode_metric(step=-1)
        df = select_df(df, {"metric": "val_accuracy"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)
        drop_levels = [n for n in df.index.names if n not in ("optimizer", "lr")]
        df = df.reset_index(drop_levels, drop=True).sort_index()

        fig, ax = plt.subplots(figsize=(7, 5))
        ax_draw_heatmap(ax, df, cmap="viridis", annotate=True)

        ax.set_title("Val Accuracy: LR vs Optimizer", fontsize=18)
        save_fig(fig, "heatmap_lr_optimizer")


@pytest.mark.figures
class TestScatterPlots:
    """Generate scatter plot of train_loss vs val_accuracy."""

    def test_scatter(self, sample_log):
        log, _ = sample_log
        df = log.melt_and_explode_metric(step=-1)
        # scatter expects 'step' and 'total_steps' in index
        # step=-1 gives step as value in index, keep total_steps too

        fig, ax = plt.subplots(figsize=(7, 6))
        ax_draw_scatter(ax, df, y_fields=["train_loss", "val_accuracy"], color="#d62728", markersize=15)

        ax.set_xlabel("Train Loss", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Train Loss vs Val Accuracy", fontsize=18)
        ax.grid(True, linestyle="--", alpha=0.3)
        save_fig(fig, "scatter_loss_acc")


@pytest.mark.figures
class TestMultiLinePlot:
    """Generate multi-line comparison figure."""

    def test_multi_optimizer_lr(self, sample_log):
        """Multiple curves comparing optimizers with different line styles."""
        log, _ = sample_log
        df = log.melt_and_explode_metric()
        df = select_df(df, {"metric": "val_accuracy"})
        df = avgbest_df(df, "metric_value", avg_over={"seed"}, best_at_max=True)

        fig, ax = plt.subplots(figsize=(9, 6))
        colors = {"sgd": "#1f77b4", "adam": "#ff7f0e"}
        linestyles = {0.001: "-", 0.01: "--", 0.1: "-."}

        for opt in ["sgd", "adam"]:
            for lr in [0.001, 0.01, 0.1]:
                try:
                    p_df = select_df(df, {"optimizer": opt, "lr": lr}, "step")
                    drop_levels = [n for n in p_df.index.names if n != "step"]
                    p_df = p_df.reset_index(drop_levels, drop=True).sort_index()
                    ax_draw_curve(
                        ax,
                        p_df,
                        label=f"{opt}, lr={lr}",
                        color=colors[opt],
                        linestyle=linestyles[lr],
                        annotate=False,
                        markersize=0,
                        linewidth=2,
                    )
                except Exception:
                    continue

        ax.set_xlabel("Step", fontsize=16)
        ax.set_ylabel("Val Accuracy", fontsize=16)
        ax.set_title("Val Accuracy by Optimizer and LR", fontsize=18)
        ax.legend(fontsize=10, ncol=2)
        ax.grid(True, linestyle="--", alpha=0.3)
        save_fig(fig, "multi_line_optimizer_lr")
