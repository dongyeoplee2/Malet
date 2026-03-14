# Scatter Plots

Scatter plots display the relationship between two (or three) metrics at a fixed step, without a traditional x-axis field. This is useful for exploring trade-offs like accuracy vs. compute or loss vs. accuracy.

## 2D scatter (`scatter`)

The mode string has no x-fields — two metrics act as the x and y axes:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode 'scatter--train_loss val_accuracy' \
  -filter 'step last'
```

Each point represents one hyperparameter configuration at the selected step.

```{image} ../_static/figures/lmda-lmda_schedule--min.png
:alt: Scatter with dual multi-line encoding
:width: 80%
:align: center
```

## 3D scatter with color (`scatter_heat`)

Add a third metric for color encoding:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode 'scatter_heat--train_loss val_accuracy param_count' \
  -filter 'step last' \
  -colors viridis
```

The first two metrics are the x and y axes; the third metric determines point color. A colorbar is added automatically. Use `-zscale log` for logarithmic color scaling.

```{image} ../_static/figures/mlf(lmda)--min.png
:alt: Scatter heat with continuous colorbar
:width: 80%
:align: center
```

## Multi-line support

- **`scatter`** supports up to 2 multi-line fields (color + marker)
- **`scatter_heat`** supports up to 1 multi-line field (marker only, since color is used for the third metric)

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode 'scatter--train_loss val_accuracy' \
  -filter 'step last' \
  -multi_line_fields 'optimizer'
```

## Python API

```python
import matplotlib.pyplot as plt
from malet.experiment import ExperimentLog
from malet.plot_utils.plot_drawer import ax_draw_scatter

log = ExperimentLog.from_tsv('log.tsv')
df = log.melt_and_explode_metric(step=-1)

fig, ax = plt.subplots(figsize=(7, 6))
ax_draw_scatter(ax, df, y_fields=['train_loss', 'val_accuracy'],
                color='#d62728', markersize=15)
ax.set_xlabel('Train Loss')
ax.set_ylabel('Val Accuracy')
fig.savefig('scatter.png', dpi=150, bbox_inches='tight')
```

### `ax_draw_scatter` parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `ax` | `Axes` | — | Matplotlib axes |
| `df` | `DataFrame` | — | Melted DataFrame with `metric` index level |
| `y_fields` | `list` | — | Exactly 2 metric names for x and y |
| `color` | `str` | `'orange'` | Marker face color |
| `marker` | `str` | `'D'` | Marker style |
| `markersize` | `float` | `30` | Base marker size (scaled 20x internally) |

### `ax_draw_scatter_heat` parameters

Same as `ax_draw_scatter`, but:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `y_fields` | `list` | — | Exactly 3 metric names (x, y, color) |
| `cmap` | `str` | `'magma'` | Colormap for the third metric |
| `norm` | `Normalize` | `None` | Color normalization |
