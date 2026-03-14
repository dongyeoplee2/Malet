# Intermediate Checkpointing

Malet can checkpoint experiment logs at intermediate epochs, so metrics are preserved even if a job crashes mid-training. This complements your own model/optimizer checkpointing.

## Training function setup

Add the `experiment` argument to your training function and use it to save and restore metrics:

```python
import os

def train(config, experiment, ...):
    metric_dict = {
        'train_accuracies': [],
        'val_accuracies': [],
        'train_losses': [],
        'val_losses': [],
    }
    start_epoch = 0

    # Restore metric checkpoint if resuming a failed run
    if config in experiment.log:
        metric_dict = experiment.get_metric_info(config)[0]
        start_epoch = len(metric_dict['train_accuracies'])

    # Restore model checkpoint if available
    ckpt_dir = get_ckpt_dir(config)
    if os.path.exists(ckpt_dir):
        ckpt = load_ckpt(ckpt_dir)
        start_epoch = ckpt.epoch

    for epoch in range(start_epoch, config.num_epochs):
        # ... train and evaluate ...
        # ... append to metric_dict ...

        # Checkpoint every N epochs
        if (epoch + 1) % config.ckpt_every == 0:
            save_ckpt(model, ckpt_dir)
            experiment.update_log(config, **metric_dict)

    return metric_dict
```

## Running with checkpointing

Enable checkpointing when creating the `Experiment`:

```python
from functools import partial
from malet.experiment import Experiment

train_fn = partial(train, ...{other arguments besides config and experiment}..)
experiment = Experiment(
    {exp_folder_path}, train_fn,
    ['train_accuracies', 'val_accuracies', 'train_losses', 'val_losses'],
    checkpoint=True,
    filelock=True,
)
experiment.run()
```

Setting `checkpoint=True` passes the `experiment` object to your training function. The `filelock=True` enables file locking for safe concurrent TSV access during checkpointing.

## Run status

Each config in the log has a `status` field that determines how it is handled on resume:

| Status | Meaning | On resume |
| --- | --- | --- |
| `R` | Currently running | Skipped |
| `C` | Completed | Skipped |
| `F` | Failed | Rerun with restored `metric_dict` |

### Handling unexpected termination

If a job is killed externally (e.g., Slurm timeout, machine shutdown), Malet cannot update the status to `F`. You have two options:

1. **Manually** edit `log.tsv` and change the status from `R` to `F` for the affected row.
2. **Programmatically** mark all running configs as failed:

   ```python
   from malet.experiment import Experiment
   Experiment.set_log_status_as_failed('./experiments/{exp_folder}')
   ```
