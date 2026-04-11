Malet Enhancement Plans

## Issues

(Dormant)

- [ ] **change pyproject.toml dependencies version specifications as range (e.g., 'pkg==1.2.3' → 'pkg >=1.1.1, <2.2.2') according to dependent api changes**
  - numpy api:
    - np.array, np.arange, np.nan, np.isscalar
  - pandas
    - pd.concat,
    - df.drop, .apply, .applymap, .set_index, .reset_index, .to_csv, .loc, .
- [ ] PLOT: **Add empty dataframe error each step of manipulation for better** **debug****ging**

## Features

(sug: 26.01.20)

- [ ] uv

(sug: 25.05.26)

- [ ] EXPLOG: Experiment meta-data manager
  - [ ] commit number
  - [ ] slurm run id number / slurm log
- [ ] EXPMANAGER
  - [ ] generate exp structure
  - [ ] folder management
  - [ ] Grand experiment log repository
    - [ ] reusability
    - [ ] extendability
      - [ ] allocate value for new field in old log and exp_config
    - [ ] maintainability
    - [ ] diff management (commit id)
    - [ ] reproducibility
    - [ ] metalog
      - [ ] log change in log (gitting logs?)
  - [ ] what was run

(sug: 25.05.26)

- [ ] EXP: git commit num and reverting back to it

(sug: 25.05.01)

- [ ] EXPLOG: REGEX for making y field to x field
- [ ] PLOT(convenience): Extract python file for compiled plots
- [ ] PLOT(convenience): GUI for plot, log manipulation
- [ ] PLOT(efficiency): used already processed tables after first plotting → restyling
- [ ] PLOT(convenience): Jupyter interface?
- [ ] EXP: Add examples folder for using malet
  - [ ] malet-create
  - [ ] read exp.py and extract config from argparser

(sug: <25.05.01)

- [ ] EXPLOG: Seperate Log and Logger?
- [ ] EXPLOG: malet logs/checkpoint dependent on versions of experiment repo
- [ ] CFG: Config version manager
- [ ] EXP: Checkpoint manager, version control
- [ ] PLOT: Multi-file-field

## Quality-of-life features

- Add error catching
  - delete current run in tsv
  - undo file lock (if filelock is added to code)
- make [read the docs](https://about.readthedocs.com/?ref=readthedocs.org)
  - utilize sphinx style doc features (deprecated, added in …)
  - mkdocs
    - <https://squidfunk.github.io/mkdocs-material/>
    - <https://mkdocstrings.github.io/>

## PLOT: more plotting features

- new plot types
  - diff (axis:+0)
  - scatter ~~plot with heat color (axis: +1)~~
    - with bubble plot (axis: +1)
    - connected scatter plot (axis +1)
  - jitter/strip plot (scatter plot with grid_fields, jitterd on x-axis for visibility)
  - beeswarm plot
  - violin plot
- maybe gui / interactive
- Better error messages
- Better CLI functionalities
  - groups in filter
  - options to choose annotations

## Add testing

- unit / integration testing
  - CFG.yaml
    - grid
    - group
    - expressions
  - Experiment
    - No split

    - Split
      - Log data race condition test
  - Plot
    - plot_configs

## EXPLOG: **Better reusability features**

- reuse results for already-run configs from other experiments
  - Make global log
    - with splits for fast accessing
    - and splits annotation csv for fast log search when accessing
- global log annotation for config lookup

## EXPLOG: Adaptivity

- Git commit ID in log (fetch at the beginning of run)
- log under change of code

## EXPLOG: Scalability

- Slower log_tsv reading speeds (with large experiments and added list-metrics)
  - causes numerous errors and bottlenecks
  1. long writing time creates empty-tsv for long time → reading during this causes errors

> ## <b><i><u>pandas → polars</u></i></b>
>
> ## <b><i><u>change ExperimentLog internals (use lazydataframe)</u></i></b>
>
> ## <b><i><u>how to differentiate grid and metric fields?</u></i></b>
>
> ## <b><i><u>change plot internals (avgbest, select_df, …)</u></i></b>
>
> ## <b><i><u>change dependencies in pyproject.toml, requirements, and readme</u></i></b>
>
> ## <b><i><u>tsv → parquet</u></i></b>
>
> ## <b><i><u>tracker from reading parquet</u></i></b>

## EXPLOG: **Better Log interfacing**

- Python script for log accessing (based on pandas operation?)
- Integrate plotting

## EXP, EXPLOG: **Inter-process communication (between different jobs)**

- tsv file-based communication

## **Prior Issues (archive)**

- [x] Log disappearing during runs (seems to happen when rewriting)
- [x] adding row with .loc\[(...,)\] indexing error for two-level multiindex dataframe in ExperimentLog.add_result
- [x] Infinite backslash problem (the string problem)

 1. the problem arises when \[float, …, str, …, float\]
 1. pandas saves \[float, …, str, …, float\] -> “\[float, 'str′, …, float\]”
 1. ExperimentLog reads “\[float, 'str′, …, float\]”
 1. str2value “\[float, 'str′, …, float\]” -> \[float, “\’str\′”, …, float\]
 1. repeat

# essential
