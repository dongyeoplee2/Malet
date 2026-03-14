# Multi-Plot Grids

Multi-plot creates a grid of subplots, each showing the same plot type for a different value of one or two fields. This is useful for comparing across dimensions that are hard to overlay on a single axes (e.g., different datasets, models, or sparsity levels).

## Basic usage

Use `-multi_plot_fields` to split the plot into subplots:

```bash
# One row of subplots, one per sparsity level
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-epoch-val_accuracy \
  -multi_plot_fields 'sp' \
  -best_at_max
```

Each subplot shares the same x and y axes for easy comparison.

```{image} ../_static/figures/crf(lmda-sp_schedule)--min.png
:alt: 4x4 faceted scatter grid
:width: 100%
:align: center
```

## Two-dimensional grid

Specify two fields to create a row-column grid:

```bash
# Columns for sparsity, rows for noise level
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-epoch-val_accuracy \
  -multi_plot_fields 'sp noise' \
  -best_at_max
```

The first field controls columns, the second controls rows. The figure size scales automatically: `[width * num_cols, height * num_rows]`.

```{image} ../_static/figures/lmda_schedule_crf(lmda-lmda_schedule)--min.png
:alt: 3x4 multi-plot grid lambda x lambda schedule
:width: 100%
:align: center
```

## Combining with multi-line

Multi-plot and multi-line can be used together. For example, show a grid of subplots (one per sparsity level) where each subplot contains multiple lines (one per optimizer):

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-epoch-val_accuracy \
  -multi_plot_fields 'sp' \
  -multi_line_fields 'optimizer' \
  -best_at_max
```

## Supported plot types

All plot types support multi-plot with up to 2 fields, including heatmaps. This makes it possible to create a grid of heatmaps — one per model or dataset:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode 'heatmap-lr weight_decay-val_accuracy' \
  -multi_plot_fields 'model' \
  -filter 'step last' \
  -best_at_max
```
