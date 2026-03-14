# Curve Plots

Curve plots show how a metric evolves over a continuous x-axis field (typically `epoch` or `step`). This is the most common plot type for visualizing training dynamics.

## Basic usage

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-epoch-val_accuracy \
  -best_at_max
```

This plots `val_accuracy` on the y-axis over `epoch` on the x-axis. Seeds are averaged automatically, and all other hyperparameters are optimized (best value selected).

```{image} ../_static/figures/admm_vs_afdmm.png
:alt: ADMM vs SAFE curve plot
:width: 80%
:align: center
```

## Error bands and error bars

When averaging over seeds, Malet computes standard error and displays it as shaded bands by default. You can switch between display modes:

- `std_plot: fill` — shaded band (default)
- `std_plot: bar` — error bars
- `std_plot: none` — no error display

```{image} ../_static/figures/optim-sp_0.9-training_dynamics-max.png
:alt: Training curves with shaded error bands
:width: 80%
:align: center
```

## Curve with best point starred

Use `curve_best` mode to highlight the best-performing point with a star marker:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve_best-epoch-val_accuracy \
  -best_at_max
```

```{image} ../_static/figures/resnet20_star_rho_sparsity.png
:alt: Best-starred curve with HP x-axis
:width: 80%
:align: center
```

This is useful for identifying the epoch where a model peaks before overfitting begins.

You can also use `curve_best` with a hyperparameter on the x-axis to find the optimal hyperparameter value:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve_best-rho-val_accuracy \
  -filter 'step last' \
  -best_at_max
```

```{image} ../_static/figures/resnet20_star_rho_sparsity.png
:alt: Best-starred curve with hyperparameter x-axis
:width: 80%
:align: center
```

## Python API

For fine-grained control, use `ax_draw_curve` and `ax_draw_best_stared_curve` directly:

```python
import matplotlib.pyplot as plt
from malet.experiment import ExperimentLog
from malet.plot_utils.data_processor import avgbest_df, select_df
from malet.plot_utils.plot_drawer import ax_draw_curve

log = ExperimentLog.from_tsv('log.tsv')
df = log.melt_and_explode_metric()
df = select_df(df, {'metric': 'val_accuracy'})
df = avgbest_df(df, 'metric_value', avg_over={'seed'},
                best_over={'lr'}, best_at_max=True)

# Reduce to single index (step)
drop = [n for n in df.index.names if n != 'step']
df = df.reset_index(drop, drop=True).sort_index()

fig, ax = plt.subplots(figsize=(9, 6))
ax_draw_curve(ax, df, label='ResNet20', color='#1f77b4',
              annotate=False, std_plot='fill')
ax.set_xlabel('Epoch')
ax.set_ylabel('Val Accuracy')
ax.legend()
fig.savefig('curve.png', dpi=150, bbox_inches='tight')
```

### `ax_draw_curve` parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `ax` | `Axes` | — | Matplotlib axes to draw on |
| `df` | `DataFrame` | — | Single-index DataFrame with one value column |
| `label` | `str` | — | Legend label |
| `std_plot` | `str` | `'fill'` | Error display: `'fill'`, `'bar'`, or `'none'` |
| `color` | `str` | `'orange'` | Line color |
| `linewidth` | `float` | `4` | Line width |
| `marker` | `str` | `'D'` | Marker style |
| `markersize` | `float` | `10` | Marker size |
| `markevery` | `int` | `20` | Show marker every N points |
| `linestyle` | `str` | `'-'` | Line style |
| `annotate` | `bool` | `True` | Add value annotations |
| `unif_xticks` | `bool` | `False` | Uniform x-tick spacing |

When the number of data points exceeds 100, markers are disabled automatically.
