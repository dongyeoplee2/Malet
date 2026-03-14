# Weights & Biases Integration

Malet can load experiment data directly from [Weights & Biases](https://wandb.ai/) sweeps, convert them into `ExperimentLog` objects, and plot results using the standard `malet-plot` CLI.

## Loading sweep data

Use `ExperimentLog.from_wandb_sweep()` to create a log from one or more W&B sweeps:

```python
from malet.experiment import ExperimentLog

log = ExperimentLog.from_wandb_sweep(
    entity='my-team',
    project='my-project',
    sweep_ids=['abc123'],
    logs_file='./experiments/wandb_results/log.tsv',
    get_all_steps=True,
)
log.to_tsv()
```

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `entity` | `str` | *(required)* | W&B entity (team or username) |
| `project` | `str` | *(required)* | W&B project name |
| `sweep_ids` | `List[str]` | *(required)* | One or more sweep IDs to load |
| `logs_file` | `str` | *(required)* | Path to save the resulting TSV |
| `get_all_steps` | `bool` | `False` | Fetch full training history (all steps) vs. only final summary |
| `filter_dict` | `dict` | `None` | Filter runs by config values (see below) |
| `get_metrics` | `List[str]` | `None` | Restrict which metrics are loaded (`None` = all) |

### How it works

1. Retrieves all runs from the specified sweeps via the W&B API.
2. Filters out runs not in `"finished"` or `"completed"` state (logs a warning with skipped counts).
3. Applies `filter_dict` if provided.
4. Automatically separates **static** config fields (same across all runs) from **grid** fields (varying).
5. If `get_all_steps=True`, downloads step-by-step history for each metric as lists.
6. Returns an `ExperimentLog` ready for saving or plotting.

### Filtering runs

Use `filter_dict` to load only matching runs:

```python
log = ExperimentLog.from_wandb_sweep(
    entity='my-team',
    project='my-project',
    sweep_ids=['abc123', 'def456'],
    logs_file='./experiments/filtered/log.tsv',
    filter_dict={
        'optimizer': ['adam', 'sgd'],
        'batch_size': 128,
    },
    get_metrics=['val_loss', 'val_accuracy'],
)
```

### Multiple sweeps

Pass multiple sweep IDs to merge results from related sweeps:

```python
log = ExperimentLog.from_wandb_sweep(
    entity='my-team',
    project='my-project',
    sweep_ids=['sweep1', 'sweep2', 'sweep3'],
    logs_file='./experiments/combined/log.tsv',
)
```

## CLI: `-wandb_sweep_id` Flag

Plot W&B sweep results directly from the command line:

```bash
malet-plot -exp_folder ./experiments \
    -wandb_sweep_id 'my-team/my-project/abc123' \
    -mode curve-step-val_loss
```

**Format:** `'{entity}/{project}/{sweep_id}'` (exactly two `/` separators).

**Behavior:**

1. Creates an experiment directory at `<exp_folder>/<project>/<sweep_id>/`.
2. On first run, calls `from_wandb_sweep(get_all_steps=True)` to download and cache the data as TSV.
3. On subsequent runs, uses the cached TSV directly.

```text
<exp_folder>/
  <project>/
    <sweep_id>/
      log.tsv     # cached sweep data
      figs/       # generated plots
```

## Complete workflow

```bash
# 1. Run your W&B sweep as usual
wandb sweep sweep_config.yaml
wandb agent my-team/my-project/abc123

# 2. Plot directly from the sweep
malet-plot -exp_folder ./experiments \
    -wandb_sweep_id 'my-team/my-project/abc123' \
    -mode curve-step-val_loss

# 3. Or load in Python for custom analysis
```

```python
from malet.experiment import ExperimentLog

log = ExperimentLog.from_wandb_sweep(
    entity='my-team',
    project='my-project',
    sweep_ids=['abc123'],
    logs_file='./experiments/my-project/abc123/log.tsv',
    get_all_steps=True,
)
log.to_tsv()

# Now use malet-plot with the cached TSV
# malet-plot -exp_folder ./experiments/my-project/abc123 -mode curve-step-val_loss
```
