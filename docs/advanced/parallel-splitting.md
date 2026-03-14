# Parallel Grid Splitting

When using GPU resource managers like Slurm, you can split the configuration grid across multiple parallel jobs. Malet provides two strategies — **partitioning** and **queueing** — which can also be combined.

## Setup

Pass `total_splits` and `curr_split` as command-line flags to your training script:

```python
from absl import app, flags
from malet.experiment import Experiment

FLAGS = flags.FLAGS

def main(argv):
    experiment = Experiment(
        {exp_folder_path}, train_fn, exp_metrics,
        total_splits=FLAGS.total_splits,
        curr_split=FLAGS.curr_split,
        filelock=FLAGS.filelock,
        configs_save=FLAGS.configs_save,
    )
    experiment.run()

if __name__ == '__main__':
    flags.DEFINE_string('total_splits', '1')
    flags.DEFINE_string('curr_split', '0')
    flags.DEFINE_bool('filelock', False)
    flags.DEFINE_bool('configs_save', False)
    app.run(main)
```

## Partitioning

Splits the config grid into fixed, non-overlapping partitions.

### Uniform partitioning (by number)

Divide configs evenly by specifying the total number of partitions and the current partition index (0-based):

```bash
splits=4
for ((i=0; i<splits; i++)); do
    python train.py ./experiments/{exp_folder} \
        --total_splits=$splits \
        --curr_split=$i
done
```

### Field partitioning (by field name)

Split by values of a specific field. Each job handles a subset of field values:

```bash
# Job 1: only SGD
python train.py ./experiments/{exp_folder} \
    --total_splits='optimizer' \
    --curr_split='sgd'

# Job 2: RMSprop and Adam
python train.py ./experiments/{exp_folder} \
    --total_splits='optimizer' \
    --curr_split='rmsprop adam'
```

Both methods save results to separate files at `{exp_folder}/log_splits/split_{i}.tsv`.

While `filelock` can be used with partitioning, it adds unnecessary read/write overhead — especially as `log.tsv` grows larger. Leave it off for pure partitioning.

## Queueing

With queueing, each job picks up the next unrun config from a shared queue. A job skips any config that is already completed or currently running by another job.

```bash
python train.py ./experiments/{exp_folder} \
    --filelock \
    --configs_save
```

- `configs_save=True` writes each config to the log **before** training starts, so other jobs can see it's in progress.
- `filelock=True` enables file locking for safe concurrent read/write to the TSV.

The main advantage of queueing is flexibility — you can add or remove GPU jobs while the experiment is running.

## Combining both

For large experiments, combine partitioning (to keep individual TSV files small) with queueing (to allow flexible GPU allocation within each partition):

```bash
splits=4
for ((i=0; i<splits; i++)); do
    python train.py ./experiments/{exp_folder} \
        --total_splits=$splits \
        --curr_split=$i \
        --filelock \
        --configs_save
done
```

This avoids the TSV file contention that arises when many jobs queue on a single large file.

## Merging split logs

After parallel runs complete, merge the split logs for plotting. See {doc}`merging-logs` for details.

```python
from malet.experiment import Experiment

Experiment.resplit_logs('./experiments/{exp_folder}', target_split=1)
```
