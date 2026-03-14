# Styling and Configuration

Malet provides three levels of styling control: CLI flags for quick adjustments, YAML config files for reusable presets, and the Python API for full matplotlib access.

## CLI styling flags

| Flag | Default | Description |
| --- | --- | --- |
| `-colors` | `'default'` | Colormap or palette name(s) |
| `-annotate` / `-noannotate` | `True` | Toggle data point annotations |
| `-annotate_field` | — | Additional fields to show in annotations |
| `-fig_size` | — | Figure size: one number (square) or two (width height) |
| `-style` | `'default'` | Matplotlib style (e.g., `'ggplot'`, `'seaborn'`) |
| `-xscale` | — | X-axis scale: `linear`, `log`, or `unif` |
| `-yscale` | — | Y-axis scale: `linear` or `log` |
| `-zscale` | — | Colorbar scale: `linear` or `log` |
| `-title` | — | Custom plot title |
| `-xlabel`, `-ylabel`, `-zlabel` | — | Custom axis labels |
| `-font_size` | `22` | Font size for title and labels |
| `-marker_size` | `10` | Marker size |

The special x-scale value `unif` (uniform) converts the x-axis to evenly spaced ticks regardless of actual numeric values. This is useful when x-axis values are irregularly spaced (e.g., `[0.001, 0.01, 0.1, 1.0]`).

## Colors

The `-colors` flag accepts palette names, colormap names, or specific hex codes:

```bash
-colors default              # seaborn default palette
-colors Blues                 # matplotlib colormap
-colors 'light:#9467bd'      # named palette with specific hue
-colors 'default Blues'       # multiple palettes (cycled)
```

Fine-tune color sampling with `-colors_rep_skip_shift [repeat skip shift]`:

- `repeat` — number of times to repeat each color
- `skip` — skip every Nth color from the palette
- `shift` — offset into the palette

## YAML plot config

For reusable styling, create a YAML file and pass it via `-plot_config`:

```bash
malet-plot -exp_folder ./exp -plot_config style.yaml -mode curve-epoch-val_accuracy
```

### Config structure

```yaml
# Default style applied to all plots
default_style:
  annotate: false
  std_plot: fill
  line_style:
    linewidth: 4
    marker: 'D'
    markersize: 10
  ax_style:
    frame_width: 2.5
    fig_size: 7
    legend: [{fontsize: 20}]
    grid: [true, {linestyle: '--'}]
    tick_params:
      - axis: both
        which: major
        labelsize: 25
        direction: in
        length: 5

# Per-mode overrides
'curve-epoch-val_accuracy':
  annotate: true
  ax_style:
    title: ['Validation Accuracy', {size: 27}]
```

### `line_style`

Controls matplotlib line properties:

| Key | Type | Description |
| --- | --- | --- |
| `linewidth` | float | Line width |
| `marker` | str | Marker style |
| `markersize` | float | Marker size |
| `markevery` | int | Show marker every N points |
| `color` | str | Line color |
| `linestyle` | str | Line style (`-`, `--`, `-.`, `:`) |

### `ax_style`

Controls figure and axes properties. Most keys map directly to `matplotlib.axes.Axes` setter methods. The value format is `[*positional_args, {**keyword_args}]`:

```yaml
ax_style:
  title: ['My Title', {size: 27}]
  xlabel: ['Epoch', {fontsize: 20}]
  yscale: ['log']
  ylim: [0, 1]
```

Two special keys are provided for convenience:

| Key | Description |
| --- | --- |
| `fig_size` | Figure width (and height if square) |
| `frame_width` | Width of the axes border spines |

### Mode aliases

Define reusable plot configurations with custom names:

```yaml
'sam_comparison':
  mode: curve-rho-val_accuracy
  multi_line_fields: optimizer
  filter: 'optimizer sgd sam'
  annotate: true
  colors: ''
  std_plot: bar
  ax_style:
    title: ['SGD vs SAM', {size: 27}]
    xlabel: ['$\rho$', {size: 30}]
    ylabel: ['Val Accuracy (%)', {size: 30}]
```

Invoke with:

```bash
malet-plot -exp_folder ./exp -plot_config style.yaml -mode sam_comparison
```

When using a mode alias, any conflicting CLI arguments are overridden by the alias configuration.

### Style hierarchy

When styles conflict, higher-priority sources take precedence:

```
default_style  <  CLI flags  <  per-mode config  <  mode alias
```

## Field ordering

Control the order of categorical values in plots with `-field_orders`:

```bash
-field_orders 'optimizer sgd adam / lr 0.1 0.01 0.001'
```

Values appear in the specified order. Malet validates that all specified values exist in the data.

## Best-reference arguments

By default, each x-axis value gets its own optimal hyperparameter set. These arguments let you fix the reference point for optimization:

`-best_ref_x_fields {value}`
: Choose the best hyperparameters at a specific x value, then apply them to all x values. For step-based x-axes, defaults to `last`.

`-best_ref_ml_fields {value}`
: Use the same hyperparameters across all multi-line field values, chosen based on a specific value.

`-best_ref_metric_field {metric}`
: Optimize hyperparameters based on one metric, then plot a different metric with those hyperparameters.

## Custom preprocessing

For advanced use cases, pass a custom preprocessing function via the `preprcs_df` argument in the Python API:

```python
def preprcs_df(p_df, legend, mlvs):
    # Modify the DataFrame, legend string, or multi-line values
    return p_df, legend, mlvs
```

This runs after `avgbest_df` and before drawing. Useful for custom legend formatting or additional row filtering.
