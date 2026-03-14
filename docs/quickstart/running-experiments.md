# Running Experiments

This page shows how to define an experiment configuration, execute it, and inspect the resulting logs.

## Experiment config YAML

Define your experiment in a YAML file. The `grid` keyword tells Malet which hyperparameters to sweep over — all combinations are run automatically:

```yaml
# Static configs (same across all runs)
model: LeNet5
dataset: mnist
num_epochs: 100
batch_size: 128
optimizer: adam

# Grid fields (all combinations are run)
grid:
    seed: [1, 2, 3]
    lr: [0.0001, 0.001, 0.01, 0.1]
    weight_decay: [0.0, 0.00005, 0.0001]
```

This produces 3 x 4 x 3 = **36 configurations**. Fields change least frequently in declaration order — `seed` changes slowest and `weight_decay` changes fastest.

For list comprehensions, grid sequences, and field grouping, see {doc}`gridding`.

## Running the experiment

Wrap your training function with `Experiment` and call `run()`:

```python
from functools import partial
from malet.experiment import Experiment

train_fn = partial(train, ...{other arguments besides config}..)
exp_metrics = ['train_accuracies', 'val_accuracies', 'train_losses', 'val_losses']
experiment = Experiment({exp_folder_path}, train_fn, exp_metrics)
experiment.run()
```

The training function must accept only `config` as its argument. Use `functools.partial` to bind any other arguments beforehand.

## Experiment logs

Results are saved automatically as `log.tsv` in the experiment folder. The file stores static configs as a YAML header and per-run metrics as TSV rows. You can load the log programmatically:

```python
from malet.experiment import ExperimentLog

log = ExperimentLog.from_tsv({tsv_file})

log.static_configs   # dict of static config values
log.df               # pandas DataFrame with grid fields as MultiIndex
```

### Automatic resuming

If a job is interrupted, Malet automatically resumes from the last completed configuration on the next `experiment.run()` call — already-completed configs are skipped. This resumes at the *config* level. For resuming from intermediate checkpoints *within* a training run, see {doc}`../advanced/intermediate-checkpointing`.
