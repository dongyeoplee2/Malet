# ExperimentLog API Reference

This page documents public methods of `ExperimentLog`, `Experiment`, and `ConfigIter` beyond what is covered in the {doc}`quickstart/running-experiments`.

## ExperimentLog

### Field manipulation

#### `derive_field(new_field_name, fn, *fn_arg_fields, is_index=False)`

Adds a new computed field by applying `fn` to existing fields.

```python
# Categorical field from a numeric one
log.derive_field('lr_group', lambda lr: 'high' if lr > 0.01 else 'low', 'lr', is_index=True)

# Derived from multiple fields
log.derive_field('effective_lr', lambda lr, bs: lr * bs / 256, 'lr', 'batch_size')
```

**Parameters:**

`new_field_name` (`str`)
: Name for the new column.

`fn` (`callable`)
: Function receiving the values of `fn_arg_fields` as positional arguments.

`*fn_arg_fields` (`str`)
: Names of existing fields to pass into `fn`.

`is_index` (`bool`)
: If `True`, the new field becomes a grid (index) field. Default: `False`.

#### `drop_fields(field_names)`

Removes fields from the log. Works on static, grid (index), and metric (column) fields.

```python
log.drop_fields(['train_loss', 'unused_metric'])
log.drop_fields(['seed'])  # remove a grid field
```

#### `rename_fields(name_map)`

Renames fields across static, grid, and metric fields.

```python
log.rename_fields({'val_accuracy': 'val_acc', 'learning_rate': 'lr'})
```

---

### Querying

#### `isin(config)` / `config in log`

Checks whether a configuration exists in the log. Both forms are equivalent:

```python
config = {'seed': 1, 'lr': 0.01, 'optimizer': 'adam'}
log.isin(config)
config in log
```

#### `get_metric(config)` / `log[config]`

Retrieves metric values for a specific configuration:

```python
config = {'seed': 1, 'lr': 0.01, 'optimizer': 'adam'}
metrics = log[config]
# {'train_loss': [...], 'val_accuracy': [...]}
```

#### `is_same_exp(other)`

Checks whether two logs have the same configuration fields (both static and grid), regardless of values. Useful before merging.

```python
if log_a.is_same_exp(log_b):
    log_a.merge(log_b)
```

#### `grid_dict()`

Returns a dictionary mapping each grid field to its unique values:

```python
log.grid_dict()
# {'seed': [1, 2, 3], 'lr': [0.001, 0.01, 0.1]}
```

---

### Data transformation

#### `melt_and_explode_metric(df=None, step=None, dropna=True)`

Converts from wide format (one column per metric, list values per step) to long format (one row per metric per step). This is the standard preprocessing step before plotting.

```python
df_long = log.melt_and_explode_metric()       # all steps
df_last = log.melt_and_explode_metric(step=-1) # last step only
```

Returns a DataFrame with new columns: `metric` (name), `metric_value` (scalar), `step` (1-indexed), and `total_steps`.

#### `drop_duplicates()`

Removes duplicate entries. Identical duplicates are auto-removed; conflicting duplicates trigger an interactive CLI prompt.

```python
log.drop_duplicates()
```

---

## Experiment

### `Experiment.resplit_logs(exp_folder_path, target_split=1, save_backup=True)`

Re-partitions split log files into a new number of splits.

```python
from malet.experiment import Experiment

Experiment.resplit_logs('./experiments/my_exp', target_split=1)   # merge into one
Experiment.resplit_logs('./experiments/my_exp', target_split=4)   # re-split into 4
```

`exp_folder_path` (`str`)
: Path to the experiment folder.

`target_split` (`int`)
: Number of output splits. `1` merges into a single `log.tsv`.

`save_backup` (`bool`)
: Save a backup as `logs_backup.tsv` before resplitting. Default: `True`.

### `Experiment.set_log_status_as_failed(exp_folder_path)`

Marks all `R` (running) configs as `F` (failed). Useful for recovering from crashed jobs. See {doc}`advanced/intermediate-checkpointing` for details on run status values.

```python
Experiment.set_log_status_as_failed('./experiments/my_exp')
```

---

## ConfigIter

### `ConfigIter.filter_iter(filt_fn)`

Filters the configuration iterator in-place using a predicate function.

```python
from malet.experiment import ConfigIter

configs = ConfigIter('exp_config.yaml')
configs.filter_iter(lambda i, d: d['lr'] > 0.001)   # keep configs where lr > 0.001
configs.filter_iter(lambda i, d: i % 2 == 0)         # keep even-indexed configs
```

`filt_fn` (`callable`)
: Function taking `(index, config_dict)`, returns `True` to keep.

### `ConfigIter.grid_dict` (property)

Returns a dictionary mapping each grid field to its unique values:

```python
configs = ConfigIter('exp_config.yaml')
configs.grid_dict
# {'seed': [1, 2, 3], 'lr': [0.001, 0.01, 0.1], 'optimizer': ['sgd', 'adam']}
```

### Indexing and slicing

`ConfigIter` supports `len()`, integer indexing, and slicing:

```python
configs = ConfigIter('exp_config.yaml')

len(configs)       # total number of configs
configs[0]         # first config
configs[-1]        # last config
configs[10:20]     # slice of configs
```
