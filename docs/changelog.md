# Changelog

Malet currently uses [**Effort-based Versioning (EffVer)**](https://jacobtomlinson.dev/effver/): minor bumps reflect the scope of changes rather than strict API compatibility guarantees. We plan to migrate to [Semantic Versioning](https://semver.org/) once the API stabilises.

Each release is published on [GitHub Releases](https://github.com/dongyeoplee2/Malet/releases) with downloadable assets and full commit diffs.

---

## Unreleased

#### 2026

**✨ Added**

- four new plot drawers (and `malet-plot` modes) in `plot_utils.plot_drawer`:
  - `ax_draw_scatter_trajectory` / `mode=scatter_trajectory` — 2-metric 2D
    path with `step` as an implicit curve parameter (scaling-law Fig 4 style:
    EMA-smoothed dark-stroked curve + raw-scatter underlay + sparse
    white-fill anchor markers)
  - `ax_draw_scatter_paired` / `mode=scatter_paired` — paired A/B
    comparison (two points + dark-edged colored connector per config);
    binary `pair_field` picked from the first `pmlf`; connector color
    encodes outcome magnitude on a shared colorbar
  - `ax_draw_surface_3d` / `mode=surface_3d` — 3D surface from two
    `x_fields` × one metric; `plot.py` conditionally adds
    `subplot_kw={'projection': '3d'}` and disables `sharex/sharey`
  - `ax_draw_parallel_coords` / `mode=parallel_coords` — wandb-style
    parallel coordinates with cubic-Bezier curves between every pair of
    adjacent axes; numeric + categorical per-axis normalization; color
    driven by the last field (typically the outcome metric)
- GitHub Actions workflow for automatic docs deployment to GitHub Pages
- auto-generated changelog from git tags and commit messages
- plot figures for documentation gallery and guides
- documentation pages for getting started, plotting guides, and advanced topics
- Sphinx docs infrastructure with sphinx-book-theme
- test suite for ExperimentLog, ConfigIter, and plot figure generation
- continuous colormap for numeric multi-line fields and docstrings to plot modules
- Google-style docstrings and refactor core modules

**🚀 Changed**

- slim down README and link to full documentation
- migrate build config to uv and update `pyproject.toml`
- minor refactoring and prior ad hoc patch

**🩹 Fixed**

- deprecated `df.applymap` to `df.map`
- `ExperimentLog.grid_dict` to not sort heterogeneous typed grids
- data_processor speed up by removing repetitive df ops
- get all step function and failed run filtering in `ExperimentLog.from_wandb_sweep`

#### 2025

**✨ Added**

- `ExperimentLog.drop_duplicate` and update df2richtable
- wandb data importing in ExperimentLog and `malet-plot`
- minor codestyle cleanup and docs

**🚀 Changed**

- formatting and suppress pandas warning in `experiment.py`

**🩹 Fixed**

- resolve_merge_conflicts call in `ExperimentLog.merge`

#### 2024

**✨ Added**

- grid_dict(), derive_field, drop_fields
- `__getitem__` = get_metric, use `__future__.annotations`, CNG merge_tsv, merge_folder behavior
- `malet-merge` with new conflict resolver, deprecate auto_update_tsv, improve docstrings, etc.

**🚀 Changed**

- labeling and FIX xscale unif

**🩹 Fixed**

- `Experiment.run` not skipping experiments
- ylabel for multiplot
- experiment resuming
- Experiment name and improve log conflict resolver messages

**🗑️ Removed**

- `__future__.annotations` due to related unknown error

---

## [0.2.1](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.2.1) — 2024-07-17

### ✨ Added

- skipping erroneous configs and timeout in Exepriment
- animation and plot making progress messages
- scatter_heat mode, field_order, marker_size option, colorbar, and etc to `malet-plot`
- control to repeat, skip, and shift color list, CNG -color option to directly set colors
- option to set fields to plot multiple rows and columns of subplots over
- last and best option for step in filter and best_ref_x_fields in `malet-plot`, FIX processing nan values in str2value
- option for finding best over step (step_best) in `malet-plot`
- scatter plot, improvement to legends
- name of log_file in error message when error occured while parsing in `ExperimentLog.parse_tsv`
- option to enable/disable filelock in Experiment, disabled by default
- option to enable/disable filelock in ExperimentLog
- logging in QueuedFileLock and make it a ContextDecorator
- QueuedFileLock for stable grid queueing
- filelock to ExperimentLog and Experiment
- saving tsv message in `malet-plot`
- saving tsv of processed metrics in `malet-plot`
- error when grid fields have different number of groups in ConfigIter

### 🚀 Changed

- malet version name
- `README.md` and -col_row_fields to -multi_plot_fields in `malet-plot`
- df2richtable to set maximum length to show

### 🩹 Fixed

- multi_plot_field in `malet-plot`
- valid field check assertion message in `malet-plot`
- animation when field is not step
- scatter when nan is in dataframe
- best_ref_x_field last for step when there are different total_steps
- plot for no col_row and heatmap
- avg_field when no seed in df in `malet-plot`
- avg_field when no seed in df in `malet-plot`
- field check in `malet-plot`
- best_ref_metric_field
- filtering in `malet-plot`
- linestyle, improve legend
- step best_ref_x_fields and filter
- `malet-plot` for no grid case, filtering total_step, etc
- `df.reset_index`() for no-grid
- no grid process
- no grid processing for log merging
- ExperimentLog for no-grid case, ADD more terminal log in `Experiment.run`
- ConfigIter and ExperimentLog when there are no grid
- tsv saving in `plot.run`
- xscale, yscale for plot_config yaml file, CNG some error messages in `plot.py`

### 🗑️ Removed

- commented lines
- `get_slurm_run_status.py`

---

## [0.1.13](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.13) — 2024-05-12

### ✨ Added

- error message when grid fields have different number of groups in ConfigIter
- error message for overlapping static and grid fields in ConfigIter and filter out feature in `malet-plot`

### 🩹 Fixed

- error when total_splits and curr_splits are passed in as int in Experiment

---

## [0.1.12](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.12) — 2024-05-01

### 🩹 Fixed

- experiment skipping failed cases and executing already running cases

### 🗑️ Removed

- strict dependency versions in `pyproject.toml`

---

## [0.1.11](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.11) — 2024-04-27

### 🩹 Fixed

- update_log to save current duration in Experiment, etc.

---

## [0.1.10](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.10) — 2024-04-18

### 🩹 Fixed

- duration aggregation and NaN checking, ADD static_config matching in Experiment

---

## [0.1.9](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.9) — 2024-04-17

### 🩹 Fixed

- checkpointing, ADD duration and git info in Experiment, etc.

---

## [0.1.8](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.8) — 2024-04-02

### 🚀 Changed

- remove info_field from ExperimentLog and FIX str2value, `ExperimentLog.add_result`, etc

---

## [0.1.7](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.7) — 2024-03-07

### ✨ Added

- processing various length in list field in `plot.py`, new mode (curve_best), additional arguments, etc
- more error messages in select_df, bool to str2value, curve_best mode in `malet-plot`, etc
- annot to heatmap, apply str2value to grid_fields in `ExperimentLog.from_tsv`, etc

### 🚀 Changed

- package version for pypi reasons
- module configuration in plot_util
- method name explode_and_melt_metric to melt_and_explode_metric in ExperimentLog, etc

---

## [0.1.5](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.5) — 2024-01-17

### ✨ Added

- heatmap and style flag and CNG some flag names in `malet-plot`
- remove_metric and remove_index to ExperimentLog
- bar plot mode, multiple field in multi_line_field, etc
- log resplitting, add_derived_index, FIX str2value to process scientific notations and nan, etc
- list2tuple when logging, FIX `ExperimentLog.merge_tsv`

### 🚀 Changed

- cli messages to rich library and ADD fig_size argument in `plot.py`
- `Experiment.resplit_logs` to recieve exp_folders, ADD multi_column_str in `utils.py`

### 🩹 Fixed

- `ExperimentLog.explode_and_melt_metric` to stop raising exceptions when there are no list fields, and handle list fields with NaN entries
- explode_and_melt_metric and merge_tsv, ADD add_computed_result

---

## [0.1.4](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.4) — 2023-12-14

### ✨ Added

- auto-fail-status logging and improve plot feature, bug fixes

### 🚀 Changed

- malet version in `pyproject.toml`

---

## [0.1.3](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.3) — 2023-11-08

### ✨ Added

- various messages and Fix filter and plot_config bugs in plot

---

## [0.1.2](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.2) — 2023-10-25

### 🩹 Fixed

- `malet-plot` entrypoint and install from github instruction in `README.md`

---

## [0.1.1](https://github.com/dongyeoplee2/Malet/releases/tag/malet-v0.1.1) — 2023-10-25

### ✨ Added

- entry point for plot and github action, FIX `Experiment.from_tsv`
- log checkpointing and RMV grid_field when yaml configuring

---

## [0.1.0](https://github.com/dongyeoplee2/Malet/releases/tag/malt-v0.1.0) — 2023-10-12

### ✨ Added

- log checkpointing and RMV grid_field when yaml configuring
