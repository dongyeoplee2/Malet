# Animated Plots (GIF)

Malet can animate any plot type over a field, creating a GIF that shows how the plot changes across values of that field. This is particularly effective for visualizing training dynamics over epochs or sweeping through a hyperparameter.

## Basic usage

Use `-animation_field` to specify which field to animate over:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-lr-val_accuracy \
  -animation_field 'step' \
  -filter 'step 50:200' \
  -best_at_max
```

This creates a GIF where each frame shows the curve at a different training step. The output is saved as a `.gif` file instead of PDF.

```{image} ../_static/figures/mlf(lmda-lr)-flt(step_50:100)-ani(step)--min.gif
:alt: Animated scatter over training steps
:width: 80%
:align: center
```

## How it works

For each unique value of the animation field, Malet generates a complete frame of the plot. A text label in the corner shows the current animation field value (e.g., `step=100`). Frames are assembled into a GIF at 10 fps using Pillow.

## Common use cases

### Training dynamics over epochs

Animate a heatmap to see how the hyperparameter landscape evolves during training:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode 'heatmap-lr weight_decay-val_accuracy' \
  -animation_field 'step' \
  -best_at_max
```

### Sweeping a hyperparameter

Animate over a hyperparameter to see its effect on the training curve:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-epoch-val_accuracy \
  -multi_line_fields 'optimizer' \
  -animation_field 'lr' \
  -best_at_max
```

Each frame shows the training curves for a different learning rate value.

```{image} ../_static/figures/cifar-mlf(lmda)-crf(sp-lmda_schedule)-flt(lmda!_0.0001-step_150:200)-ani(step)--min.gif
:alt: Animated multi-plot scatter over training
:width: 100%
:align: center
```

## Combining with multi-line and multi-plot

Animation works with both multi-line and multi-plot fields. For example, animate a multi-line plot over steps:

```bash
malet-plot -exp_folder ./experiments/my_exp \
  -mode curve-lr-val_accuracy \
  -multi_line_fields 'optimizer' \
  -multi_plot_fields 'sp' \
  -animation_field 'step' \
  -filter 'step 50:200' \
  -best_at_max
```

This creates a GIF where each frame contains a grid of subplots, each with multiple lines, at a specific training step.

## Output

- Output format: GIF (`.gif`)
- Frame rate: 10 fps
- Frame interval: 400ms
- Writer: Pillow (`PillowWriter`)
- Filename encodes the animation field: `...-ani(step)--max.gif`
