# Malet

***Ma**chine **L**earning **E**xperiment **T**ool*

**Malet** is a tool for hyperparameter grid searches, metric logging, advanced analyses and visualizations.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🔎 Easy & powerful grid search
Define hyperparameter grids in a single YAML file. Malet handles the combinatorial expansion, parallel splitting, resuming, and logging automatically.
:::

:::{grid-item-card} 📝 Experiment logging & resuming
Metric logging with automatic TSV persistence and experiment resuming — pick up where you left off when jobs are killed.
:::

:::{grid-item-card} 📊 Flexible visualization
Generate curves, bar charts, heatmaps, scatter plots, and animated GIFs directly from experiment logs with `malet-plot`. No boilerplate scripts needed.
:::

:::{grid-item-card} 🚀 Multi-GPU parallelization
Split experiment grids across GPUs with Slurm, checkpoint long-running jobs, and merge results — all with built-in file locking.
:::
::::

---

## Getting started

Install Malet and run your first experiment in minutes:

```bash
pip install malet
```

```bash
# Run experiments over a grid of hyperparameters
python train.py

# Plot results with a single command
malet-plot -exp_folder ./experiments/my_exp -mode curve-epoch-val_accuracy
```

New to Malet? Start with the {doc}`installation` guide, then work through the {doc}`quickstart/index`.

```{toctree}
:maxdepth: 2
:caption: Getting Started
:hidden:

installation
quickstart/index
```

```{toctree}
:maxdepth: 2
:caption: Plotting
:hidden:

plotting/index
```

```{toctree}
:maxdepth: 2
:caption: Guides
:hidden:

advanced/parallel-splitting
advanced/intermediate-checkpointing
advanced/merging-logs
advanced/wandb-integration
```

```{toctree}
:maxdepth: 2
:caption: Examples & Reference
:hidden:

examples/index
experiment-log-api
api/index
```

```{toctree}
:maxdepth: 2
:caption: Development
:hidden:

changelog
contributing
```
