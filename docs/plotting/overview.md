# Overview

## Core concept

Every Malet plot starts from an experiment log containing multiple hyperparameter configurations and their metrics. The plotting pipeline reduces this high-dimensional data down to exactly **two fields** — one for the x-axis and one for the y-axis — by handling all other fields in one of three ways:

1. **Specify** — fix a field to a single value (e.g., `model=ResNet20`)
2. **Average** — aggregate across values (e.g., average over `seed`)
3. **Optimize** — select the value that yields the best metric (e.g., best `lr`)

Any field not explicitly assigned to the x-axis, multi-line fields, or `seed` is automatically optimized based on `-best_at_max`.

After running `malet-plot`, a summary panel shows how each field was handled. This is useful for debugging unexpected results.

## The mode string

The `-mode` flag specifies the plot type, x-axis field(s), and metric(s):

```bash
-mode {plot_type}-{x_fields}-{metrics}
```

| Plot type | x-fields | metrics | Description |
| --- | --- | --- | --- |
| `curve` | 1 | 1 | Line plot with error bands |
| `curve_best` | 1 | 1 | Line plot with best point starred |
| `bar` | 1 | 1 | Bar chart |
| `heatmap` | 2 (space-separated) | 1 | 2D heatmap with colorbar |
| `scatter` | 0 | 2 (space-separated) | 2D scatter plot |
| `scatter_heat` | 0 | 3 (space-separated) | Scatter plot with color-mapped 3rd metric |

Examples:

```bash
-mode curve-epoch-val_accuracy
-mode bar-optimizer-val_accuracy
-mode heatmap-lr\ weight_decay-val_accuracy
-mode scatter--train_loss\ val_accuracy
-mode scatter_heat--train_loss\ val_accuracy\ param_count
```

## Filtering data

Use `-filter` to select or exclude specific field values:

```bash
-filter 'field1 val1 val2 / field2 val3'     # include only these values
-filter 'field1! val1'                         # exclude val1
-filter 'step 50:100'                          # range syntax (steps 50-99)
```

Two auto-generated fields can be filtered:

- **`step`** — created by exploding list-type metrics. Special values: `last` (final step), `best` (best-performing step), or range syntax like `50:100`.
- **`metric`** — created by melting multiple metric columns into rows.

The most common filter is `-filter 'step last'`, which selects only the final epoch for bar charts and heatmaps.

## Best-at-max

By default, Malet assumes smaller metric values are better (e.g., loss). For accuracy or other metrics where larger is better, pass `-best_at_max`:

```bash
malet-plot -exp_folder ./exp -mode curve-epoch-val_accuracy -best_at_max
```

## Quick example

```bash
malet-plot \
  -exp_folder ./experiments/resnet_cifar10 \
  -mode curve-epoch-val_accuracy \
  -best_at_max
```

This generates a line plot of `val_accuracy` over epochs, averaging over `seed` and selecting the best `lr` and `weight_decay` automatically.

## Data pipeline

Understanding the internal pipeline helps when results look unexpected:

1. **Load** — read `log.tsv` from the experiment folder
2. **Pre-filter** — apply filters on grid fields (optimizer, lr, etc.)
3. **Melt & explode** — convert wide metric format to long format, expanding list values into separate rows with `step` and `metric` columns
4. **Post-filter** — apply filters on `step`, `metric`, `total_steps`
5. **Classify fields** — split remaining fields into specified, key, averaged, and optimized
6. **avgbest_df** — average over avg fields (seed), select best over optimized fields
7. **Draw** — pass processed DataFrame to the appropriate `ax_draw_*` function
