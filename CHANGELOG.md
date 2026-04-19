# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/). This project currently uses **effort-based versioning** (minor bumps reflect scope of changes) and will migrate to [Semantic Versioning](https://semver.org/) once the API stabilizes.

## Unreleased

### Added

- New plot drawers and `malet-plot` modes:
  - `ax_draw_scatter_trajectory` / `mode=scatter_trajectory` — 2-metric
    2D path with step as implicit curve parameter (scaling-law Fig 4
    visual: EMA-smoothed dark-stroked curve + raw-scatter underlay +
    sparse white-fill anchor markers)
  - `ax_draw_scatter_paired` / `mode=scatter_paired` — paired A/B points
    connected by a dark-edged colored line, shared outcome colorbar,
    white-fill markers with thin dark edge; binary `pair_field` picked
    from the first `pmlf`
  - `ax_draw_surface_3d` / `mode=surface_3d` — 3D surface from two
    `x_fields` × one metric (`plot.py` adds `subplot_kw={'projection':'3d'}`
    when this mode is selected)
  - `ax_draw_parallel_coords` / `mode=parallel_coords` — wandb-style
    parallel coordinates joined by cubic Bezier curves; handles numeric
    and categorical axes; colored by the last field

## [0.2.2] - 2026-03-15

### Added

- Sphinx documentation site with Furo theme, hosted on GitHub Pages
- Google-style docstrings for all public and internal functions
- New documentation pages: W&B integration guide, ExperimentLog API reference, Examples & Templates
- `malet-merge` CLI tool documentation
- ruff linter and formatter with Google docstring convention
- uv for dependency management
- GitHub Actions workflow for automatic documentation deployment
- W&B data importing in `ExperimentLog` and `malet-plot` via `from_wandb_sweep()` and `-wandb_sweep_id` flag
- `ExperimentLog.drop_duplicates()` for deduplicating experiment entries
- `ExperimentLog.__getitem__` (`log[config]`) and `get_metric` for easy metric retrieval via indexing syntax
- `ExperimentLog.from_field` for DataFrame initialization by grid/metric field names
- `ExperimentLog.grid_dict()` to get a dictionary of grid fields to values
- `ExperimentLog.derive_field()` (merged from `add_computed_metric` and `add_derived_index`)
- `ExperimentLog.drop_fields()` (merged from `remove_metric` and `remove_index`)
- `ExperimentLog.rename_fields()` for renaming static/grid/metric fields
- `malet-merge` CLI tool with heterogeneous log conflict resolver for NaN error-free merged logs

### Changed

- `ExperimentLog.__init__` arguments changed to `(df, static_configs, logs_file, use_filelock)`
- Deprecated `auto_update_tsv` in favor of `use_filelock`
- `ExperimentLog.merge_tsv` and `merge_folder` now return merged log without saving unless `save_path` is passed
- Relaxed exact dependency pins (`==` to `>=`) for `absl-py` and `ml-collections`
- README slimmed down; advanced topics moved to Sphinx docs
- Repository URL updated to `dongyeoplee2/Malet`

### Fixed

- `Experiment` not skipping already run experiments
- `ExperimentLog.merge_folder` with relative paths
- `resolve_merge_conflicts` call in `ExperimentLog.merge`
- W&B sweep: `get_all_steps` function and failed run filtering
- `ExperimentLog.grid_dict` no longer sorts heterogeneous typed grids
- Deprecated `df.applymap` replaced with `df.map`
- `data_processor` speed improvements by removing repetitive DataFrame operations
- Missing `enumerate` in `ax_draw_bar` annotation loop causing undefined variable `i`
- Removed unused variables `idx_len` and `ilen`
- Replaced `.keys()` with direct dict iteration in plot assertions

### Removed

- `requirements.txt` (replaced by `pyproject.toml` + `uv.lock`)

## [0.2.1] - 2024-07-17

### Added

- `malet.utils.QueuedFileLock` for stable grid parallelism
- `use_filelock=False` attribute option in `ExperimentLog`
- `timeout` keyword argument in `Experiment`
- Error message when reading TSV fails in `ExperimentLog.parse_tsv`
- `dropna` kwarg to `ExperimentLog.melt_and_explode_metric`
- `scatter` and `scatter_heat` plot modes
- Saves TSV of metrics used for plotting
- New CLI arguments: `-multi_plot_fields`, `-animation_field`, `-colors_rep_skip_shift`, `-field_order`, `-zlabel`, `-zscale`, `-marker_size`
- `last` and `best` options for `step` field filtering
- Styles beyond colors (marker, linestyle) for multi-line fields
- Color bar for `heatmap` and `scatter_heat` modes

### Changed

- `Experiment` skips erroneous configs and continues to next
- `plot.draw_metric` returns additional dataframe
- `-colors` now takes matplotlib colormap names

### Fixed

- Error when grid fields have different group numbers in `ConfigIter`
- `ConfigIter` and `ExperimentLog` when no grid in `exp_config.yaml`
- `xscale`, `yscale` setting via `plot_config.yaml`
- `None` value filtering in `select_df`
- `total_step` filtering conflicting with `step` auto-filtering
- `*exclude_fields` argument in `homogenize_df`
- NaN-valued grid annotation in `ax_draw_heatmap`
- NaN processing in `utils.str2value`

## [0.1.13] - 2024-05-12

### Added

- Filter-out syntax using `!` suffix in `malet-plot` (e.g., `-filter 'field! value'`)
- Error message for overlapping fields in static and grid configs

### Fixed

- Error when `total_splits` and `curr_splits` passed as int in `Experiment`

## [0.1.12] - 2024-05-01

### Fixed

- Experiment skipping failed cases and executing already running cases

## [0.1.11] - 2024-04-27

### Added

- Method to set all `R` status to `F` in TSV file (`Experiment.set_log_status_as_failed`)
- Option to set status in `Experiment.update_log`
- `RunInfo` class for time tracking in `Experiment`
- x/y scale options in `malet-plot`
- Standard deviation annotation (mean +/- std) in `malet-plot`

### Changed

- Renamed `get_log_checkpoint` to `get_metric_info` in `Experiment`
- Returns empty dictionaries if matching config log not found

### Fixed

- Run duration tracking not updating when calling `update_log`
- NaN checking in `get_metric_info`
- Filtering `total_step` with `step` auto-filtering in `avgbest_df`

## [0.1.10] - 2024-04-18

### Added

- Error message for non-matching `static_config` between `ConfigIter` and `ExperimentLog`

### Fixed

- Duration aggregation in `Experiment.run`
- NaN checking in `Experiment.get_log_checkpoint`

## [0.1.9] - 2024-04-17

### Added

- Train duration information and git info in `Experiment`

### Changed

- `Experiment.update_log` arguments from `(metric_dict, config)` to `(config, **metric_dict)`
- `Experiment.get_log_checkpoint` arguments and return values

### Fixed

- `Experiment` not recording datetime and status
- `Experiment` not deleting metrics when checkpointing
- `ExperimentLog.add_result` argument change reflected in `Experiment.update_log`

## [0.1.8] - 2024-04-02

### Changed

- Removed `info_field` attribute in `ExperimentLog` (redundant; migrate to `metric_field`)
- Renamed `get_metric_and_info` to `get_metric`
- Removed `infos` kwarg; changed metric kwarg from dict to unpacked keyword arguments

### Fixed

- `str2value` to process `inf` and return string if `literal_eval` throws exception
- `ExperimentLog.add_result` for cases with two grid fields
- `isin` to check only matching config in static configs

## [0.1.7] - 2024-03-07

### Added

- `curve_best` mode for plotting star marker on best performing point
- Heatmap annotations in `malet-plot`
- Epoch range filtering in `malet-plot`
- Processing list fields with various lengths in `malet-plot`
- Automatic `markevery` setting based on x-values in curve modes
- CLI arguments: `-title`, `-xlabel`, `-ylabel`, `-font_size`
- Filters `log.df` prior to `melt_and_expand_metric` for faster processing
- `save` kwarg to `ExperimentLog.merge_folder`
- Better error messages for overlapping and non-existent fields

### Changed

- Renamed `explode_and_melt_metric` to `melt_and_explode_metric`; kwarg `epoch` to `step`
- Compute function no longer mapped onto list fields in `add_computed_metric`
- Changed module structure of `malet.plot_utils`

### Fixed

- Plotting when x-field is `step` (previously `epoch`)
- Plotting all steps instead of only last
- Error when `best_ref_x_fields` not specified
- Annotation placement in curve mode
- Applied `str2value` to indices when loading TSV
- `add_derived_index` to handle tuples

## [0.1.5] - 2024-01-17

### Added

- Bar plot and heatmap modes in `malet-plot`
- Cast list configs to tuple for hashability in `ExperimentLog`
- `parse_str` option in `ExperimentLog.parse_tsv`
- Methods: `add_computed_metric`, `add_derived_index`
- `remove_metric` and `remove_index` in `ExperimentLog`
- Resplitting for `ExperimentLog`
- CLI options: `-annotate_field`, `-fig_size`, `-style`
- `save_path` kwarg to merge methods

### Changed

- `Experiment.resplit_logs` auto-finds paths from experiment folder
- `malet-plot` accepts space-separated lists in `multi_line_fields`, `x_fields`, `best_ref_x_fields`
- `ExperimentLog.merge` changed from `pd.merge` to `pd.concat`
- Improved `malet-plot` messages using `rich` library

### Fixed

- `ExperimentLog.merge_tsv` by not parsing strings to list
- `str2value` for scientific notation and NaN
- `explode_and_melt_metric` with no list fields and NaN entries
- `malet-plot` errors with multiple metric fields using `best_ref` fields

## [0.1.4] - 2023-12-14

### Added

- Automatic fail status logging using try-catch
- Merged `add_configs_only` method with `add_result` in `ExperimentLog`
- Improved shell messages when plotting
- Better plot save names preventing overwrites
- Plot option to select optimal value direction (min or max)

### Fixed

- Proper sorting when plotting over list-valued field
- `str2value` integer and float error
- `ExperimentLog.from_tsv` method call in `Experiment`

## [0.1.3] - 2023-11-08

### Added

- Shell message during `malet-plot` notifying how fields in the dataframe are handled (key, non-key: specified / averaged / optimized)
- Error message when user-specified value does not exist in the field when using `plot_utils.metric_drawer:select_df`

### Fixed

- `str2value` when handling filter in `plot:draw_metric`
- "Cannot concat list with dict" error in `plot_utils.utils:merge_dict`

## [0.1.2] - 2023-10-25

### Fixed

- Correct entry point for `malet-plot`

## [0.1.1] - 2023-10-25

### Added

- Entry point `malet-plot` for `malet.plot:main`
- GitHub Action for automated package publishing to PyPI

### Changed

- Removed `info_fields` from `Experiment.from_tsv`; now inferred from TSV

### Fixed

- `Experiment.from_tsv` input argument error in `plot.py`

## [0.1.0] - 2023-10-12

### Added

- Logging in intermediate epochs

### Changed

- Removed `grid_field` from YAML configuration

### Fixed

- `utils.str2value` logic
