from typing import Literal

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


def ax_draw_curve(
    ax: Axes,
    df: pd.DataFrame,
    label: str,
    annotate=True,
    annotate_field=[],
    std_plot: Literal["none", "fill", "bar"] = "fill",
    unif_xticks=False,
    color="orange",
    linewidth=4,
    marker="D",
    markersize=10,
    markevery=20,
    linestyle="-",
    **_,
) -> Axes:
    """Draws curve of y_field over arbitrary x_field setted as index of the dataframe.
    If there is column 'y_field_sdv' is in dataframe, draws in errorbar or fill_between depending on ``sdv_bar_plot``
    """
    assert std_plot in {"bar", "fill", "none"}, 'std_plot should be one of {"bar","fill","none"}'
    y_field = list(df)[0]

    x_values, metric_values = map(np.array, zip(*dict(df[y_field]).items()))
    assert not isinstance(metric_values[0], pd.Series), f"y_field should have only {1} values for each index."

    if len(x_values) > 100:
        marker = None
        if unif_xticks:
            ax.locator_params(tight=True, nbins=5)
    elif len(x_values) > 20:
        markevery = 20
        if unif_xticks:
            ax.locator_params(tight=True, nbins=5)
    else:
        markevery = 1

    tick_values = x_values

    artists = []

    if len(tick_values) == 1:
        artists.append(ax.axhline(metric_values, linewidth=linewidth, color=color, label=label))
        if f"{y_field}_std" in df:
            metric_std = float(df[f"{y_field}_std"])
            artists.append(
                ax.axhspan(metric_values[0] + metric_std, metric_values[0] - metric_std, alpha=0.3, color=color)
            )

    else:
        if unif_xticks:
            tick_values = np.arange(len(x_values))
            ax.set_xticks(tick_values, x_values, fontsize=10)  # , rotation=45)

        artists += ax.plot(
            tick_values,
            metric_values,
            label=label,
            color=color,
            linewidth=linewidth,
            marker=marker,
            markersize=markersize,
            markevery=markevery,
            linestyle=linestyle,
        )

        if len(x_values) % markevery != 0:
            artists += ax.plot(tick_values[-1], metric_values[-1], color=color, marker=marker, markersize=markersize)

        if f"{y_field}_std" in df:
            x_values, metric_std = map(np.array, zip(*dict(df[f"{y_field}_std"]).items()))

            if std_plot == "bar":
                artists.append(ax.errorbar(tick_values, metric_values, yerr=metric_std, color=color, elinewidth=3))
            elif std_plot == "fill":
                artists.append(
                    ax.fill_between(
                        tick_values, metric_values + metric_std, metric_values - metric_std, alpha=0.3, color=color
                    )
                )

        if annotate:
            assert not (
                f := set(annotate_field) - (a := set(df) - {"total_steps", "step", y_field, f"{y_field}_std"})
            ), f"Annotation field: {f} are not in dataframe field: {a}"
            annotate_field = set(annotate_field) & a
            abv = lambda s: (
                "".join([i[0] for i in s.split("_")] if "_" in s else [s[0]] + [i for i in s[1:] if i not in "aeiou"])
                if len(s) > 3
                else s
            )
            abv_annot = [*map(abv, annotate_field)]
            for i, (x, y, t) in enumerate(zip(x_values, metric_values, tick_values)):
                if i % markevery and i != len(x_values) - 1:
                    continue
                txt = "\n".join(
                    [
                        f"{y:.5f}"
                        + (
                            rf"$\pm${metric_std[i]:.5f}" if (f"{y_field}_std" in df and pd.notna(metric_std[i])) else ""
                        ),
                        str(x),
                    ]
                    + [f"{i}={df.loc[x][j]}" for i, j in zip(abv_annot, annotate_field)]
                )
                artists.append(ax.annotate(txt, (t, y), textcoords="offset points", xytext=(0, 10), ha="center"))

    ax.tick_params(axis="both", which="major", labelsize=17, direction="in", length=5)

    return artists


def ax_draw_best_stared_curve(
    ax: Axes,
    df: pd.DataFrame,
    label: str,
    annotate=True,
    annotate_field=[],
    std_plot: Literal["none", "fill", "bar"] = "fill",
    best_at_max=True,
    unif_xticks=False,
    color="orange",
    linewidth=4,
    marker="D",
    markersize=10,
    markevery=20,
    linestyle="-",
    **_,
) -> Axes:
    """Draws curve of y_field over arbitrary x_field setted as index of the dataframe.
    If there is column 'y_field_sdv' is in dataframe, draws in errorbar or fill_between depending on ``sdv_bar_plot``
    """
    assert std_plot in {"bar", "fill", "none"}, 'std_plot should be one of {"bar","fill","none"}'
    y_field = list(df)[0]

    x_values, metric_values = map(np.array, zip(*dict(df[y_field]).items()))
    assert not isinstance(metric_values[0], pd.Series), f"y_field should have only {1} values for each index."

    if len(x_values) > 100:
        marker = None
        if unif_xticks:
            ax.locator_params(tight=True, nbins=5)
    elif len(x_values) > 20:
        markevery = 20
        if unif_xticks:
            ax.locator_params(tight=True, nbins=5)
    else:
        markevery = 1

    tick_values = x_values

    artists = []

    if len(tick_values) == 1:
        artists.append(ax.axhline(metric_values, linewidth=linewidth, color=color, label=label))
        if f"{y_field}_std" in df:
            metric_std = float(df[f"{y_field}_std"])
            artists.append(
                ax.axhspan(metric_values[0] + metric_std, metric_values[0] - metric_std, alpha=0.3, color=color)
            )

    else:
        if unif_xticks:
            tick_values = np.arange(len(x_values))
            ax.set_xticks(tick_values, x_values, fontsize=10, rotation=45)

        ax.plot(tick_values, metric_values, color=color, linewidth=linewidth)
        if f"{y_field}_std" in df:
            x_values, metric_std = map(np.array, zip(*dict(df[f"{y_field}_std"]).items()))

            if std_plot == "bar":
                artists.append(ax.errorbar(tick_values, metric_values, yerr=metric_std, color=color, elinewidth=3))
            elif std_plot == "fill":
                artists.append(
                    ax.fill_between(
                        tick_values, metric_values + metric_std, metric_values - metric_std, alpha=0.3, color=color
                    )
                )

        best_idx = list(metric_values).index((max if best_at_max else min)(metric_values))
        for i, (_, _y, _t) in enumerate(zip(x_values, metric_values, tick_values)):
            if i % markevery:
                continue
            if i == best_idx:
                artists += ax.plot(
                    tick_values[i], metric_values[i], color="green", marker="*", markersize=markersize + 10
                )
            else:
                artists += ax.plot(
                    tick_values[i],
                    metric_values[i],
                    color=color,
                    marker=marker,
                    markersize=markersize,
                    markevery=markevery,
                    linestyle=linestyle,
                )

        if annotate:
            assert not (
                f := set(annotate_field) - (a := set(df) - {"total_steps", "step", y_field, f"{y_field}_std"})
            ), f"Annotation field: {f} are not in dataframe field: {a}"
            annotate_field = set(annotate_field) & a
            abv = lambda s: (
                "".join([i[0] for i in s.split("_")] if "_" in s else [s[0]] + [i for i in s[1:] if i not in "aeiou"])
                if len(s) > 3
                else s
            )
            abv_annot = [*map(abv, annotate_field)]
            for i, (x, y, t) in enumerate(zip(x_values, metric_values, tick_values)):
                if i % markevery:
                    continue
                txt = "\n".join(
                    [
                        f"{y:.5f}"
                        + (
                            rf"$\pm${metric_std[i]:.5f}" if (f"{y_field}_std" in df and pd.notna(metric_std[i])) else ""
                        ),
                        str(x),
                    ]
                    + [f"{i}={df.loc[x][j]}" for i, j in zip(abv_annot, annotate_field)]
                )
                artists.append(ax.annotate(txt, (t, y), textcoords="offset points", xytext=(0, 10), ha="center"))

    ax.tick_params(axis="both", which="major", labelsize=17, direction="in", length=5)

    return artists


def ax_draw_bar(
    ax: Axes,
    df: pd.DataFrame,
    label: str,
    annotate=True,
    annotate_field=[],
    std_plot=True,
    unif_xticks=False,
    color="orange",
    **_,
) -> Axes:
    """Draws bar graph of y_field over arbitrary x_field setted as index of the dataframe.
    If there is column 'y_field_sdv' is in dataframe, draws in errorbar or fill_between depending on ``sdv_bar_plot``
    """
    y_field = list(df)[0]

    x_values, metric_values = map(np.array, zip(*dict(df[y_field]).items()))
    assert not isinstance(metric_values[0], pd.Series), f"y_field should have only {1} values for each index."

    tick_values = np.arange(len(x_values))
    ax.set_xticks(tick_values, x_values, fontsize=10, rotation=45)

    artists = []

    if std_plot and f"{y_field}_std" in df:
        x_values, metric_std = map(np.array, zip(*dict(df[f"{y_field}_std"]).items()))
        artists.append(ax.bar(tick_values, metric_values, yerr=metric_std, label=label, color=color))
    else:
        artists.append(ax.bar(tick_values, metric_values, label=label, color=color))

    if annotate:
        assert not (f := set(annotate_field) - (a := set(df) - {"total_steps", "step", y_field, f"{y_field}_std"})), (
            f"Annotation field: {f} are not in dataframe field: {a}"
        )
        annotate_field = set(annotate_field) & a
        abv = lambda s: (
            "".join([i[0] for i in s.split("_")] if "_" in s else [s[0]] + [i for i in s[1:] if i not in "aeiou"])
            if len(s) > 3
            else s
        )
        abv_annot = [*map(abv, annotate_field)]
        for i, (x, y, t) in enumerate(zip(x_values, metric_values, tick_values)):
            txt = "\n".join(
                [
                    f"{y:.5f}"
                    + (rf"$\pm${metric_std[i]:.5f}" if (f"{y_field}_std" in df and pd.notna(metric_std[i])) else "")
                ]
                + ["" if unif_xticks else str(x)]
                + [f"{k}={df.loc[x][j]}" for k, j in zip(abv_annot, annotate_field)]
            )
            artists.append(ax.annotate(txt, (t, y), textcoords="offset points", xytext=(0, 10), ha="center"))

    ax.tick_params(axis="both", which="major", labelsize=17, direction="in", length=5)

    return artists


def ax_draw_heatmap(ax: Axes, df: pd.DataFrame, cmap="magma", annotate=True, annotate_field=[], norm=None, **_) -> Axes:
    """Draws heatmap of y_field over two arbitrary x_fields setted as multi-index of the dataframe."""
    y_field = list(df)[0]
    y_field_df = df.drop(columns=list(df)[1:])

    x_fields = y_field_df.index.names
    grid_df = y_field_df.reset_index().pivot(index=x_fields[1], columns=x_fields[0])

    artists = [ax.pcolor(grid_df, cmap=cmap, edgecolors="w", norm=norm)]

    (*x_values,) = map(lambda l: sorted(set(y_field_df.index.get_level_values(l))), x_fields)
    ax.set_xticks(np.arange(0.5, len(x_values[0]), 1), x_values[0], fontsize=10, rotation=45)
    ax.set_yticks(np.arange(0.5, len(x_values[1]), 1), x_values[1], fontsize=10)

    if annotate:
        assert not (f := set(annotate_field) - (a := set(df) - {"total_steps", "step", y_field, f"{y_field}_std"})), (
            f"Annotation field: {f} are not in dataframe field: {a}"
        )
        annotate_field = set(annotate_field) & a
        abv = lambda s: (
            "".join([i[0] for i in s.split("_")] if "_" in s else [s[0]] + [i for i in s[1:] if i not in "aeiou"])
            if len(s) > 3
            else s
        )
        abv_annot = [*map(abv, annotate_field)]

        if f"{y_field}_std" in df:
            y_std_df = df.drop(columns=list(set(df) - {f"{y_field}_std"}))
            std_grid_df = y_std_df.reset_index().pivot(index=x_fields[1], columns=x_fields[0])

        for i, (mtc, x) in enumerate([*grid_df]):
            for j, y in enumerate([*grid_df.index.get_level_values(0)]):
                txt = "\n".join(
                    [
                        f"{grid_df.loc[y, (mtc, x)]:.5f}"
                        + (
                            f"\n$\\pm${std_grid_df.loc[y, (f'{mtc}_std', x)]:.5f}"
                            if (f"{y_field}_std" in df and pd.notna(std_grid_df.loc[y, (f"{mtc}_std", x)]))
                            else ""
                        )
                    ]
                    + [
                        f"{i}={df.loc[(x, y), j]}"
                        for i, j in zip(abv_annot, annotate_field)
                        if df.index.isin([(x, y)]).any()
                    ]
                )
                artists.append(ax.text(i + 0.5, j + 0.5, txt, c="dimgrey", ha="center", va="center", weight="bold"))

    # ax.tick_params(axis='both', which='major', labelsize=17, direction='in', length=5)
    return artists


def ax_draw_scatter(ax: Axes, df: pd.DataFrame, y_fields: list, color="orange", marker="D", markersize=30, **_) -> Axes:
    """Draws a 2D scatter plot of two metrics from a melted dataframe.

    Args:
        ax: Matplotlib axes to draw on.
        df: DataFrame with a 'metric' level in the index and 'metric_value' column.
        y_fields: List of exactly two metric names to plot as x and y axes.
        color: Marker face color.
        marker: Marker style.
        markersize: Base marker size (scaled by 20x internally).

    Returns:
        list: List of matplotlib artist objects created.
    """
    assert len(set(df.index.get_level_values("metric"))) == 2, (
        f"There should be {2} metrics in the dataframe, got {set(df.index.get_level_values('metric'))}."
    )
    assert set(df.index.get_level_values("metric")) == set(y_fields), (
        "y_fields should be the same as metrics in the dataframe."
    )

    df = df.reset_index(["total_steps", "step"], drop=True)

    # revert back melted metrics into original column form
    prcs = lambda y: (
        df.loc[df.index.get_level_values("metric") == y]
        .reset_index("metric", drop=True)
        .rename(columns={"metric_value": y})
    )

    df = pd.concat([*map(prcs, y_fields)], axis=1)

    y1, y2 = map(lambda y: list(df[y]), y_fields)

    artists = [ax.scatter(y1, y2, color=color, marker=marker, s=markersize * 20, edgecolors="black")]

    return artists


def ax_draw_scatter_heat(
    ax: Axes, df: pd.DataFrame, y_fields: list, cmap="magma", marker="D", markersize=30, norm=None, **_
) -> Axes:
    """Draws a scatter plot with heatmap coloring from three metrics.

    The first two metrics are used as x and y coordinates, and the third
    metric determines the color of each point.

    Args:
        ax: Matplotlib axes to draw on.
        df: DataFrame with a 'metric' level in the index and 'metric_value' column.
        y_fields: List of exactly three metric names (x, y, color).
        cmap: Colormap name for the heatmap coloring.
        marker: Marker style.
        markersize: Base marker size (scaled by 20x internally).
        norm: Matplotlib normalization instance for color mapping.

    Returns:
        list: List of matplotlib artist objects created.
    """
    assert len(set(df.index.get_level_values("metric"))) == 3, (
        f"There should be {3} metrics in the dataframe, got {set(df.index.get_level_values('metric'))}."
    )
    assert set(df.index.get_level_values("metric")) == set(y_fields), (
        "y_fields should be the same as metrics in the dataframe."
    )

    df = df.reset_index(["total_steps", "step"], drop=True)

    # revert back melted metrics into original column form
    prcs = lambda y: (
        df.loc[df.index.get_level_values("metric") == y]
        .reset_index("metric", drop=True)
        .rename(columns={"metric_value": y})
    )

    df = pd.concat([*map(prcs, y_fields)], axis=1)

    y1, y2, y3 = map(lambda y: list(df[y]), y_fields)

    artists = [ax.scatter(y1, y2, c=y3, marker=marker, s=markersize * 20, norm=norm, cmap=cmap)]

    return artists


def ax_draw_surface_3d(
    ax: Axes,
    df: pd.DataFrame,
    label: str = "",
    cmap="Blues",
    alpha=0.85,
    rstride=1,
    cstride=1,
    linewidth=0.2,
    edgecolor="0.7",
    antialiased=True,
    elev: float = 25,
    azim: float = -60,
    **_,
) -> Axes:
    """3D surface: (x_field_1 × x_field_2) → metric. Same df input as
    ``ax_draw_heatmap`` (2 index levels, y_field as first column), rendered
    as a matplotlib ``plot_surface``.

    Usage note: the incoming ``ax`` MUST be a ``mpl_toolkits.mplot3d.Axes3D``.
    Malet's ``plot.py`` handles this when mode=='surface_3d' (creates the
    figure with ``subplot_kw={'projection': '3d'}``). If calling directly,
    create your axes as ``fig.add_subplot(..., projection='3d')``.
    """
    from mpl_toolkits.mplot3d import Axes3D  # noqa

    assert isinstance(ax, Axes3D), (
        "ax_draw_surface_3d requires a 3D axes. Create with projection='3d'."
    )

    y_field = list(df)[0]
    y_field_df = df.drop(columns=list(df)[1:])

    x_fields = y_field_df.index.names
    assert len(x_fields) == 2, f"surface_3d expects 2 index levels, got {x_fields}."

    # Pivot to a regular 2D grid (x_fields[0] along cols, x_fields[1] along rows)
    grid = y_field_df.reset_index().pivot(index=x_fields[1], columns=x_fields[0], values=y_field)
    grid = grid.sort_index().sort_index(axis=1)

    x_vals = np.array(grid.columns.tolist(), dtype=float)
    y_vals = np.array(grid.index.tolist(), dtype=float)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = grid.values.astype(float)

    artists = []
    surf = ax.plot_surface(
        X, Y, Z,
        cmap=cmap, alpha=alpha,
        rstride=rstride, cstride=cstride,
        linewidth=linewidth, edgecolor=edgecolor,
        antialiased=antialiased,
        label=label if label else None,
    )
    artists.append(surf)

    ax.set_xlabel(str(x_fields[0]))
    ax.set_ylabel(str(x_fields[1]))
    ax.set_zlabel(y_field)
    ax.view_init(elev=elev, azim=azim)

    return artists


def ax_draw_scatter_trajectory(
    ax: Axes,
    df: pd.DataFrame,
    label: str,
    y_fields: list,
    color_field: str | None = None,
    color="orange",
    cmap="viridis",
    smooth_alpha: float = 0.08,
    anchor_every: int = 10,
    raw_alpha: float = 0.12,
    stroke_width=4.4,
    curve_width=2.6,
    vmin=None,
    vmax=None,
    **_,
) -> Axes:
    """Scaling-law-style trajectory: x and y are BOTH metrics (not step).
    Each call draws ONE curve — the current HP combination's path through
    (y_fields[0], y_fields[1]) space as step advances. Step is the implicit
    parameter along the curve, not on any axis.

    Visual: dark-stroked colored curve (EMA-smoothed) + raw-scatter alpha
    underlay + sparse white-fill anchor markers at ``anchor_every`` checkpoints.

    Input dataframe: 2-metric melted form like ``ax_draw_scatter`` but with
    ``step`` kept in the index (NOT reset) so we can order the trajectory.
    Call once per line — Malet's outer ``pmlf`` loop feeds one df per line.

    color_field: if provided and present as an index level (e.g. from pmlf),
    its value on this sub-df sets the trajectory color via ``cmap`` (numeric)
    or overrides ``color``. Otherwise ``color`` is used directly.
    """
    import matplotlib.colors as mcolors
    import matplotlib.patheffects as pe

    assert len(set(df.index.get_level_values("metric"))) == 2, (
        f"There should be {2} metrics, got {set(df.index.get_level_values('metric'))}."
    )
    assert set(df.index.get_level_values("metric")) == set(y_fields), (
        "y_fields should be the same as metrics in the dataframe."
    )
    assert "step" in df.index.names, (
        "ax_draw_scatter_trajectory requires 'step' in the index to order the trajectory."
    )

    # Reshape: long→wide on metric, keep step (and other HP levels) as index
    prcs = lambda y: (
        df.loc[df.index.get_level_values("metric") == y]
        .reset_index("metric", drop=True)
        .rename(columns={"metric_value": y})
    )
    wide = pd.concat([*map(prcs, y_fields)], axis=1)
    # Sort by step so the curve order is correct
    wide = wide.sort_index(level="step")
    # Drop duplicate steps across other HP levels by aggregating if needed
    if "step" in wide.index.names and len(wide.index.names) > 1:
        wide = wide.groupby(level="step", sort=True).mean(numeric_only=True)
    # Drop rows with any NaN
    wide = wide.dropna(subset=y_fields)
    if wide.empty:
        return []

    x_vals = wide[y_fields[0]].to_numpy(dtype=float)
    y_vals = wide[y_fields[1]].to_numpy(dtype=float)

    # Resolve color
    this_color = color
    if color_field is not None and color_field in df.index.names:
        cv_series = df.index.get_level_values(color_field)
        try:
            cv = float(next(iter(set(cv_series))))
            if vmin is None or vmax is None:
                this_color = plt.get_cmap(cmap)(0.5)
            else:
                norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
                this_color = plt.get_cmap(cmap)(norm(cv))
        except (ValueError, TypeError, StopIteration):
            pass

    # EMA smooth y_vals (x_vals independently smoothed preserves curve shape)
    def _ema(arr):
        if len(arr) == 0:
            return arr
        out = [float(arr[0])]
        for v in arr[1:]:
            out.append(smooth_alpha * float(v) + (1 - smooth_alpha) * out[-1])
        return np.asarray(out)

    xs_s = _ema(x_vals)
    ys_s = _ema(y_vals)

    artists = []
    # Raw-scatter underlay
    artists.append(
        ax.scatter(x_vals, y_vals, s=4, color=this_color, alpha=raw_alpha,
                   edgecolor="none", zorder=1)
    )
    # Dark-stroked smoothed trajectory
    artists += ax.plot(
        xs_s, ys_s,
        label=label,
        color=this_color,
        linewidth=curve_width,
        alpha=0.95,
        solid_capstyle="round",
        path_effects=[pe.withStroke(linewidth=stroke_width, foreground="black")],
        zorder=2,
    )
    # Sparse white-fill anchor circles
    n = len(xs_s)
    if n > 0 and anchor_every > 0:
        idx = np.linspace(0, n - 1, num=min(anchor_every, n)).astype(int)
        artists.append(
            ax.scatter(
                xs_s[idx], ys_s[idx],
                s=22, marker="o",
                facecolor="white", edgecolor="black",
                linewidths=0.6, zorder=3,
            )
        )

    ax.tick_params(axis="both", which="major", labelsize=17, direction="in", length=5)
    return artists


def ax_draw_parallel_coords(
    ax: Axes,
    df: pd.DataFrame,
    label: str = "",
    fields: list = (),
    color_field: str | None = None,
    cmap="plasma",
    line_alpha: float = 0.35,
    line_width: float = 1.0,
    axis_line_color="0.6",
    axis_line_width: float = 0.8,
    tick_fontsize: int = 9,
    label_fontsize: int = 10,
    vmin=None,
    vmax=None,
    **_,
) -> Axes:
    del label  # kept for Malet drawer-API compliance; not drawn on-plot here
    """Wandb-style parallel coordinates plot with smooth cubic-Bezier curves.

    One vertical axis per field (in order), each normalized to [0, 1]. One
    polyline per row of ``df`` connects the row's value on every axis; the
    line is colored by ``color_field`` (typically the last — the outcome
    metric). Between every adjacent pair of axes, points are joined by a
    cubic Bezier with horizontal tangents (``P0, P0+dx/3, P1-dx/3, P1``)
    giving the wandb S-curve look.

    Input: wide dataframe with one row per run and one column per field in
    ``fields``. Categorical columns are mapped to integer indices preserving
    sort order; numeric columns use min/max normalization. NaNs in any
    field cause that row to be skipped.

    Designed to match the visual vocabulary of wandb's Hyperparameter
    Importance / Parallel Coordinates panel.
    """
    import matplotlib.colors as mcolors
    import matplotlib.path as mpath
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch

    fields = list(fields)
    assert len(fields) >= 2, f"parallel_coords needs >= 2 fields, got {fields}."
    assert all(f in df.columns for f in fields), (
        f"All fields must be columns in df. Missing: {[f for f in fields if f not in df.columns]}"
    )
    color_field = color_field or fields[-1]
    assert color_field in df.columns, f"color_field '{color_field}' not in df columns."

    # Build per-axis normalization + tick info
    def _axis_info(col: "pd.Series"):
        """Returns (normalize_fn, tick_positions, tick_labels)."""
        s = col.dropna()
        try:
            vals = s.astype(float)
            vmin_c, vmax_c = float(vals.min()), float(vals.max())
            if vmin_c == vmax_c:
                vmin_c, vmax_c = vmin_c - 0.5, vmax_c + 0.5
            rng = vmax_c - vmin_c
            # 6 evenly-spaced ticks
            ticks = np.linspace(vmin_c, vmax_c, 6)
            tick_pos = (ticks - vmin_c) / rng
            tick_lbl = [f"{t:g}" for t in ticks]
            return (lambda v, vmin_c=vmin_c, rng=rng: (float(v) - vmin_c) / rng), tick_pos, tick_lbl
        except (ValueError, TypeError):
            # Categorical
            uniq = sorted({v for v in s if v is not None and (isinstance(v, str) or not np.isnan(v) if isinstance(v, float) else True)},
                          key=lambda x: (isinstance(x, str), x))
            idx_map = {v: i for i, v in enumerate(uniq)}
            n = max(len(uniq), 1)
            denom = max(n - 1, 1)
            tick_pos = np.array([i / denom for i in range(n)]) if n > 1 else np.array([0.5])
            return (lambda v: (idx_map.get(v, 0) / denom) if n > 1 else 0.5), tick_pos, [str(u) for u in uniq]

    axis_infos = [_axis_info(df[f]) for f in fields]

    # Draw vertical axes
    n_axes = len(fields)
    for i, (f, (_, tp, tl)) in enumerate(zip(fields, axis_infos)):
        ax.axvline(i, color=axis_line_color, lw=axis_line_width, zorder=1)
        ax.text(i, 1.03, f, ha="center", va="bottom",
                fontsize=label_fontsize, zorder=5)
        for p, t in zip(tp, tl):
            ax.text(i - 0.02, p, t, ha="right", va="center",
                    fontsize=tick_fontsize, zorder=4)

    # Color map for polylines
    cvals = df[color_field].dropna()
    try:
        cvals_f = cvals.astype(float)
        _vmin = float(cvals_f.min()) if vmin is None else vmin
        _vmax = float(cvals_f.max()) if vmax is None else vmax
        if _vmin == _vmax:
            _vmin, _vmax = _vmin - 1.0, _vmax + 1.0
        norm = mcolors.Normalize(vmin=_vmin, vmax=_vmax)
        is_numeric_color = True
    except (ValueError, TypeError):
        norm = None
        is_numeric_color = False
    cmap_obj = plt.get_cmap(cmap)

    # Draw each row as a polyline of cubic Bezier segments
    artists = []
    bezier_codes = [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4]
    for idx, row in df[fields].iterrows():
        # Skip rows with any NaN in the selected fields
        if row.isna().any():
            continue
        # Normalize per-axis
        ys = []
        for f, (norm_fn, _, _) in zip(fields, axis_infos):
            try:
                ys.append(norm_fn(row[f]))
            except (TypeError, ValueError, KeyError):
                ys.append(np.nan)
        if any(np.isnan(y) for y in ys):
            continue

        # Color
        cv_raw = row[color_field]
        if is_numeric_color:
            try:
                color = cmap_obj(norm(float(cv_raw)))
            except (ValueError, TypeError):
                color = "0.5"
        else:
            color = cmap_obj(0.5)

        # Build composite path: cubic Bezier between each pair of axes
        verts = [(0, ys[0])]
        codes = [mpath.Path.MOVETO]
        for i in range(n_axes - 1):
            x0, x1 = i, i + 1
            y0, y1 = ys[i], ys[i + 1]
            c0 = (x0 + 1.0 / 3.0, y0)
            c1 = (x1 - 1.0 / 3.0, y1)
            verts.extend([c0, c1, (x1, y1)])
            codes.extend(bezier_codes[1:])
        path = mpath.Path(verts, codes)
        patch = PathPatch(path, facecolor="none", edgecolor=color,
                          lw=line_width, alpha=line_alpha, zorder=2)
        ax.add_patch(patch)
        artists.append(patch)

    # Axes limits + cosmetics
    ax.set_xlim(-0.2, n_axes - 0.8)
    ax.set_ylim(-0.05, 1.12)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    return artists


def ax_draw_iso_step_bezier(
    ax: Axes,
    curves: list,
    at_steps=None,
    n_connect: int = 6,
    linestyle: str = ":",
    line_width: float = 0.7,
    color="0.3",
    alpha: float = 0.55,
    sort_by: Literal["x", "y", "given"] = "x",
    **_,
) -> list:
    """Thin dotted cubic-Bezier curves connecting SAME-step anchor points
    across multiple trajectories. Post-hoc overlay for scatter_trajectory
    plots — call AFTER all per-run ``ax_draw_scatter_trajectory`` calls.

    Args:
        curves: list of ``(steps_array, x_array, y_array)`` tuples, one per
            trajectory. Each array must be sorted by ``step``.
        at_steps: explicit shared step values at which to draw connectors.
            If ``None``, picks ``n_connect`` values evenly in the common
            step range (excluding endpoints).
        n_connect: used only when ``at_steps`` is None.
        sort_by: how to order points before building the Bezier path. "x"
            (default) makes the connector monotone along x; "y" along y;
            "given" preserves the caller's order in ``curves``.

    Each shared step gets one path: cubic Bezier with horizontal tangents
    between adjacent points (same pattern as ax_draw_parallel_coords).
    """
    import matplotlib.path as mpath
    from matplotlib.patches import PathPatch

    if len(curves) < 2:
        return []

    # Normalize input arrays + filter empty
    valid = []
    for c in curves:
        s, x, y = c
        s = np.asarray(s); x = np.asarray(x); y = np.asarray(y)
        if len(s) >= 2 and len(s) == len(x) == len(y):
            valid.append((s, x, y))
    if len(valid) < 2:
        return []

    if at_steps is None:
        lo = max(s.min() for s, _, _ in valid)
        hi = min(s.max() for s, _, _ in valid)
        if hi <= lo:
            return []
        at_steps = np.linspace(lo, hi, n_connect + 2)[1:-1]
    else:
        at_steps = np.asarray(at_steps, dtype=float)

    artists = []
    for st in at_steps:
        pts = []
        for s, x, y in valid:
            if st < s.min() or st > s.max():
                continue
            xi = float(np.interp(st, s, x))
            yi = float(np.interp(st, s, y))
            pts.append((xi, yi))
        if len(pts) < 2:
            continue

        if sort_by == "x":
            pts.sort(key=lambda p: p[0])
        elif sort_by == "y":
            pts.sort(key=lambda p: p[1])

        verts = [pts[0]]
        codes = [mpath.Path.MOVETO]
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            dx = x1 - x0
            c0 = (x0 + dx / 3.0, y0)
            c1 = (x1 - dx / 3.0, y1)
            verts.extend([c0, c1, (x1, y1)])
            codes.extend([mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4])
        path = mpath.Path(verts, codes)
        patch = PathPatch(path, facecolor="none", edgecolor=color,
                          lw=line_width, linestyle=linestyle, alpha=alpha,
                          zorder=4)
        ax.add_patch(patch)
        artists.append(patch)

    return artists


def ax_draw_scatter_paired(
    ax: Axes,
    df: pd.DataFrame,
    y_fields: list,
    pair_field: str,
    pair_values: tuple = (),
    color_by: Literal["delta_y", "abs_delta_y", "y_a"] = "delta_y",
    cmap="RdBu_r",
    markers_pair: tuple = ("s", "o"),
    markersize=30,
    stroke_width=5.0,
    curve_width=3.2,
    vmin=None,
    vmax=None,
    **_,
) -> Axes:
    """Paired scatter: each config appears as two points (pair_field takes two
    values) connected by a dark-edged colored line whose color encodes the
    outcome magnitude (default |Δy|). Endpoint markers are white-filled with
    a thin dark edge, shape per pair member (markers_pair).

    Input: 2-metric melted dataframe like ``ax_draw_scatter``, additionally
    requires ``pair_field`` to be present as an index level with exactly 2
    distinct values. ``pair_values`` optionally fixes the order; otherwise
    the sorted unique values are used.

    Fits Malet's "paired ablation" case (e.g. LRC on vs off) where you want
    to see BOTH the joint (y1, y2) coordinate of each config AND the direction
    of improvement when a single HP is toggled.
    """
    import matplotlib.colors as mcolors
    import matplotlib.patheffects as pe

    assert len(set(df.index.get_level_values("metric"))) == 2, (
        f"There should be {2} metrics in the dataframe, got {set(df.index.get_level_values('metric'))}."
    )
    assert set(df.index.get_level_values("metric")) == set(y_fields), (
        "y_fields should be the same as metrics in the dataframe."
    )
    assert pair_field in df.index.names, f"pair_field '{pair_field}' must be an index level."

    df = df.reset_index(["total_steps", "step"], drop=True)

    prcs = lambda y: (
        df.loc[df.index.get_level_values("metric") == y]
        .reset_index("metric", drop=True)
        .rename(columns={"metric_value": y})
    )
    wide = pd.concat([*map(prcs, y_fields)], axis=1)

    pvs = tuple(pair_values) if pair_values else tuple(sorted(set(wide.index.get_level_values(pair_field))))
    assert len(pvs) == 2, f"pair_field '{pair_field}' must have exactly 2 values, got {pvs}."
    a_val, b_val = pvs

    other_levels = [n for n in wide.index.names if n != pair_field]
    a_df = wide.xs(a_val, level=pair_field)
    b_df = wide.xs(b_val, level=pair_field)
    keys = a_df.index.intersection(b_df.index)

    def _cv(a_row, b_row):
        ya2, yb2 = a_row[y_fields[1]], b_row[y_fields[1]]
        if color_by == "delta_y":
            return yb2 - ya2
        if color_by == "abs_delta_y":
            return abs(yb2 - ya2)
        return a_row[y_fields[1]]

    cvals = [_cv(a_df.loc[k], b_df.loc[k]) for k in keys]
    if not cvals:
        return []

    _vmin = float(min(cvals)) if vmin is None else vmin
    _vmax = float(max(cvals)) if vmax is None else vmax
    if _vmin == _vmax:
        _vmin, _vmax = _vmin - 1.0, _vmax + 1.0
    norm = mcolors.Normalize(vmin=_vmin, vmax=_vmax)
    cmap_obj = cm.get_cmap(cmap) if hasattr(cm, "get_cmap") else plt.get_cmap(cmap)

    artists = []
    for k, cv in zip(keys, cvals):
        a_row = a_df.loc[k]; b_row = b_df.loc[k]
        xa, ya = a_row[y_fields[0]], a_row[y_fields[1]]
        xb, yb = b_row[y_fields[0]], b_row[y_fields[1]]
        color = cmap_obj(norm(cv))
        artists += ax.plot(
            [xa, xb],
            [ya, yb],
            color=color,
            linewidth=curve_width,
            alpha=0.95,
            solid_capstyle="round",
            path_effects=[pe.withStroke(linewidth=stroke_width, foreground="black")],
            zorder=2,
        )
        artists.append(
            ax.scatter(
                xa, ya, marker=markers_pair[0], s=markersize * 14,
                facecolor="white", edgecolor="black", linewidths=0.7, zorder=3,
            )
        )
        artists.append(
            ax.scatter(
                xb, yb, marker=markers_pair[1], s=markersize * 14,
                facecolor="white", edgecolor="black", linewidths=0.7, zorder=3,
            )
        )

    ax.tick_params(axis="both", which="major", labelsize=17, direction="in", length=5)
    return artists
