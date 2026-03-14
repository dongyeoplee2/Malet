# Merging Log Files

After running {doc}`parallel split experiments <parallel-splitting>`, you need to merge the split log files before plotting. Malet provides both a CLI tool and a Python API.

## CLI tool (`malet-merge`)

```bash
# Merge all .tsv files in a folder
malet-merge -folder {log_folder_path}

# Merge specific files only
malet-merge -folder {log_folder_path} -files 'split_0.tsv split_1.tsv'

# Merge with a custom output path
malet-merge -folder {log_folder_path} -save_path {output_path}
```

By default, the merged log is saved as `log_merged.tsv` in the specified folder.

## Python API

### Merge all logs in a folder

```python
from malet.experiment import ExperimentLog

merged_log = ExperimentLog.merge_folder({log_folder_path})
merged_log.to_tsv({save_path})
```

### Merge specific files

```python
from malet.experiment import ExperimentLog

names = ['split_0', 'split_1', 'split_2']
merged_log = ExperimentLog.merge_tsv(names, {log_folder_path})
merged_log.to_tsv({save_path})
```

Both `merge_tsv` and `merge_folder` return the merged `ExperimentLog` without saving. Pass `save_path` to save automatically, or call `to_tsv()` on the result.

### Resplitting

To re-partition logs into a different number of splits (or merge everything into one):

```python
from malet.experiment import Experiment

# Merge all splits into a single log.tsv
Experiment.resplit_logs('./experiments/{exp_folder}', target_split=1)

# Re-split into 4 new partitions
Experiment.resplit_logs('./experiments/{exp_folder}', target_split=4)
```

## Duplicate resolution

If logs have overlapping configs with conflicting metric values, use `drop_duplicates()` for interactive resolution:

```python
log = ExperimentLog.from_tsv('log.tsv')
log.drop_duplicates()
log.to_tsv()
```

See {doc}`../experiment-log-api` for more log manipulation methods.
