# Plot gallery

A visual overview of what Malet can produce. All figures below were generated from real CIFAR-10 ResNet20 experiment logs. Click any heading to jump to the corresponding guide page.

## {doc}`Curve plots <curve>`

Training and validation curves with error bands, comparing methods or sweeping hyperparameters.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/admm_vs_afdmm.png
:alt: ADMM vs SAFE comparison
```
*ADMM vs SAFE across sparsity levels*
:::

:::{grid-item}
```{image} ../_static/figures/optim-sp_0.9-training_dynamics-max.png
:alt: Training dynamics at sparsity 0.9
```
*Training dynamics: masked val accuracy over epochs*
:::
::::

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/interval_val_acc.png
:alt: Dual-update interval vs val accuracy
```
*Sequential blue colormap for ordered sparsity levels*
:::

:::{grid-item}
```{image} ../_static/figures/lambda_dist.png
:alt: Lambda vs distance to constraint
```
*Log-log curve: penalty vs constraint distance*
:::
::::

## {doc}`Scatter plots <scatter>`

Metric-vs-metric relationships with multi-line encoding (color + marker shape).

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/lmda-lmda_schedule--min.png
:alt: Scatter with dual encoding
```
*Color = lambda, marker = schedule (dual multi-line)*
:::

:::{grid-item}
```{image} ../_static/figures/mlf(lmda)--min.png
:alt: Scatter with continuous colorbar
```
*Marker = lambda, color = proj dev (continuous colorbar)*
:::
::::

## {doc}`Multi-plot grids <multi-plot>`

Subplot grids split by one or two fields.

```{image} ../_static/figures/crf(lmda-sp_schedule)--min.png
:alt: 4x4 faceted scatter grid
:width: 100%
:align: center
```
*4x4 grid by lambda (columns) x sparsity schedule (rows), colored by proj dev*

```{image} ../_static/figures/lmda_schedule_crf(lmda-lmda_schedule)--min.png
:alt: 3x4 faceted scatter grid
:width: 100%
:align: center
```
*3x4 grid by lambda x lambda schedule*

## {doc}`Multi-line <multi-line>`

Multiple curves on the same axes. Ordered numeric fields get sequential colormaps automatically.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/optim-sp_0.9-max.png
:alt: Four methods compared at sparsity 0.9
```
*Tab10 palette: ADMM, SAFE, SAM, SGD at sparsity 0.9*
:::

:::{grid-item}
```{image} ../_static/figures/optim-optim_afdmm_sam_sgd-max.png
:alt: Three methods across sparsities
```
*Method comparison across sparsity levels*
:::
::::

## {doc}`Animation (GIF) <animation>`

Animate any plot type over time. The x-axis shows hyperparameters; the animation field (epoch/step) drives the frames.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/mlf(lmda-lr)-flt(step_50:100)-ani(step)--min.gif
:alt: Animated scatter over training steps
```
*Scatter animated over steps: color = lambda, marker = lr*
:::

:::{grid-item}
```{image} ../_static/figures/cifar-mlf(lmda)-crf(sp-lmda_schedule)-flt(lmda!_0.0001-step_150:200)-ani(step)--min.gif
:alt: Animated multi-plot scatter
```
*Faceted scatter animated over late training*
:::
::::

## Other visualizations

Loss landscapes and custom analysis plots.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/landscape_admm.png
:alt: ADMM loss landscape
```
*ADMM loss landscape (sharpness: 0.2)*
:::

:::{grid-item}
```{image} ../_static/figures/landscape_safe.png
:alt: SAFE loss landscape
```
*SAFE loss landscape (sharpness: 0.09 — flatter minimum)*
:::
::::

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item}
```{image} ../_static/figures/schedule_sp.png
:alt: Lambda schedules
```
*Lambda penalty schedules: constant, cosine, linear*
:::

:::{grid-item}
```{image} ../_static/figures/lambda_val_acc_small.png
:alt: Lambda vs accuracy by sparsity
```
*Dense/sparse/BNT accuracy vs lambda across sparsities*
:::
::::
