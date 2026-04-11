<!-- markdownlint-disable MD033 MD031 MD032 MD040 -->

## Master Enhancement Summary

All proposals unified, graded, and sorted. Details in each category section below.

**Grading:** T1 = strong (no caveats), T2 = promising (resolvable caveat), T3 = speculative (critical pitfall)

### T1 — Implement with confidence

| ID | Enhancement | Category |  Effort |
| -- | ----------- | -------- |  ------ |
| 1.1 | Content-addressable experiment identity (schema + config + commit hash) | [Identity & Schema](#identity--schema-evolution) | ~1d |
| 1.2 | `--parallel N` local parallelism via `multiprocessing.Queue` | [Execution](#execution--parallelism) | ~2d |
| 1.3 | FastAPI/HTTP coordinator protocol (not gRPC — faster in Python) | [Execution](#execution--parallelism) | ~2d |
| 1.4 | Function signature inspection for config validation (Fiddle-inspired) | [Validation](#error-messages--validation) | ~4h |
| 1.5 | Storage backend interface (`StorageBackend` protocol) | [Storage](#storage--data-model) | ~1d |
| 1.6 | Textual TUI for coordinator live status | [UX](#ux--output-control) | ~1d |
| 1.7 | Mode format validation with actionable error hints | [Validation](#error-messages--validation) | ~1h |
| 1.8 | Filter special-value detection (`'last'` → suggest `--best_ref_x_fields`) | [Validation](#error-messages--validation) | ~1h |
| 1.9 | wandb field rename hints (`_step` → `step`) | [Validation](#error-messages--validation) | ~1h |
| 1.10 | Centralized validation module (`plot_utils/validation.py`) | [Validation](#error-messages--validation) | ~4h |
| 1.11 | Output format control (`--output_format`, `--output_dir`, `--dpi`) | [UX](#ux--output-control) | ~1h |
| 1.12 | Replace bare `except:` with specific types + traceback chaining | [Code Quality](#code-quality) | ~2h |
| 1.13 | Remove `pd.DataFrame.set_index` monkey-patch | [Code Quality](#code-quality) | ~30m |
| 1.14 | Config schema extraction from argparse / absl FLAGS | [Validation](#error-messages--validation) | ~4h |
| 1.15 | Dependency version ranges in pyproject.toml (`==` → `>=,<`) | [Code Quality](#code-quality) | ~2h |
| 1.16 | Explicit schema definition with `PrjSchema` handler (Python dataclass) | [Identity & Schema](#identity--schema-evolution) | ~2d |

### T2 — Promising (caveat to resolve first)

| ID | Enhancement | Category | Caveat | Effort |
| -- | ----------- | -------- | ------ | ------ |
| 2.1 | Sparse metric + `best_ref` diagnostic message | [Validation](#error-messages--validation) | Shares code with 2.6; test coverage needed | ~2h |
| 2.2 | Filter `'last'`/`'first'` resolution to actual values | [UX](#ux--output-control) | Depends on 1.8 as fallback | ~1h |
| 2.3 | Sparse metric cross-optimization (non-NaN subset alignment) | [Data Processing](#bug-fixes--data-processing) | Panel-data alignment logic needs careful testing | ~2h |
| 2.4 | `homogenize_df` fix: exclude metric-dependent fields | [Data Processing](#bug-fixes--data-processing) | Validate doesn't break non-metric-dep workflows | ~2h |
| 2.5 | Summary cache (materialized view for `avgbest_df`) | [Data Processing](#bug-fixes--data-processing) | Cache invalidation on write | ~4h |
| 2.6 | Append-only checkpoint writes (WAL pattern) | [Storage](#storage--data-model) | WAL file management + crash recovery logic | ~2d |
| 2.7 | QueuedFileLock hardening (atomic ops, stale detection) | [Execution](#execution--parallelism) | Subtle race conditions; thorough testing needed | ~2d |
| 2.8 | Non-interactive merge conflict resolution | [Data Processing](#bug-fixes--data-processing) | Must not silently discard data; default = "raise" | ~4h |
| 2.9 | Typed config fields with semantic roles (`role: replicate`) | [Identity & Schema](#identity--schema-evolution) | Schema complexity; must be fully optional | ~2d |
| 2.10 | Config aliases for schema evolution | [Identity & Schema](#identity--schema-evolution) | Alias chains; one-level-only rule mitigates | ~4h |
| 2.11 | Aim v3 integration for web dashboard | [Dashboard](#dashboard--visualization) | SDK-only ingestion; data duplication; ~50MB dep | ~1w |
| 2.12 | Marimo as interactive analysis environment | [Dashboard](#dashboard--visualization) | Young project; matplotlib→Altair friction | ~3d |
| 2.13 | Documentation (wandb mapping, best_ref docs, troubleshooting) | [Documentation](#documentation) | Must wait for validation fixes to finalize | ~4h |
| 2.14 | New plot types (jitter/strip, beeswarm, violin, connected scatter, bubble) | [UX](#ux--output-control) | Each type needs design decisions for field mapping | ~1d ea |
| 2.15 | Experiment metadata in log (slurm job ID, slurm log path) | [Identity & Schema](#identity--schema-evolution) | Which metadata fields to include; avoid bloat | ~4h |
| 2.16 | Global experiment log repository (reuse results across experiments) | [Data Processing](#bug-fixes--data-processing) | Schema matching across experiments; stale results | ~1w |
| 2.17 | Allocate default values for new fields in existing logs | [Identity & Schema](#identity--schema-evolution) | Must distinguish "was default" from "was not measured" | ~4h |
| 2.18 | Testing infrastructure (unit + integration for ConfigIter, Experiment, Plot) | [Code Quality](#code-quality) | Large surface area; prioritize by bug frequency | ~1w |
| 2.19 | REGEX field derivation (derive x-field from metric field name pattern) | [UX](#ux--output-control) | Regex can be confusing; needs good error messages | ~4h |
| 2.20 | Export compiled plot as standalone Python script | [UX](#ux--output-control) | Need to capture all state (data + config + style) | ~1d |
| 2.21 | Nested Dremel-style columns for per-layer metrics | [Storage](#storage--data-model) | Complex schema; power-user feature; flat→nested parser needed | ~1w |

### T3 — Speculative (critical pitfall)

| ID | Enhancement | Category | Critical pitfall |
| -- | ----------- | -------- | ---------------- |
| 3.1 | Altair for interactive plots | [Dashboard](#dashboard--visualization) | 5K row limit breaks large-data use case |
| 3.2 | Aim v4 (AimOS) custom dashboards | [Dashboard](#dashboard--visualization) | Maintenance stalled since Oct 2023 |
| 3.3 | Polars as primary DataFrame backend | [Storage](#storage--data-model) | Full API rewrite; overkill for <50MB |
| 3.4 | DuckDB query engine | [Storage](#storage--data-model) | ~80MB dep; scope confusion |
| 3.5 | Star schema (`ExperimentStore`) | [Storage](#storage--data-model) | Only useful at >50MB; adds class + 2 deps |

### Implementation Phases

```
Phase 1 — Quick wins (no new deps, high impact):
  1.7, 1.8, 1.9, 1.10     validation & error messages
  1.11                      output format/path control
  1.12, 1.13               code quality
  1.4                       function signature inspection

Phase 2 — Core architecture:
  1.16                      PrjSchema handler class
  1.1                       content-addressable identity (uses 1.16 schema hash)
  1.5                       storage backend interface
  1.2                       --parallel N
  2.4                       homogenize_df fix
  2.6                       append-only writes

Phase 3 — Coordinator + UI:
  1.3                       FastAPI coordinator (multi-machine)
  1.6                       Textual TUI
  2.7                       filelock hardening (fallback path)
  2.8                       non-interactive merge

Phase 4 — Optimization + polish:
  2.1 + 2.3                sparse metric handling
  2.2                       filter 'last' resolution
  2.5                       summary cache
  2.9, 2.10                typed configs + aliases
  2.13                      documentation

Phase 5 — Dashboard (optional deps):
  2.11                      Aim bridge (malet[dashboard])
  2.12                      Marimo notebook (malet[analyze])
```

### Critical Files

| File | Items |
| ---- | ----- |
| `src/malet/plot.py` | 1.7, 1.9, 1.11, 2.1, 2.2, 2.3 |
| `src/malet/plot_utils/data_processor.py` | 1.8, 2.4, 2.5 |
| `src/malet/plot_utils/validation.py` | 1.10 (new file — consolidates 1.7, 1.8, 1.9) |
| `src/malet/schema.py` | 1.16 (new file — `PrjSchema` class) |
| `src/malet/experiment.py` | 1.1, 1.4, 1.5, 1.12, 1.13, 1.16, 2.6, 2.8, 2.9, 2.10 |
| `src/malet/utils.py` | 1.12, 2.7 |
| `src/malet/coordinator.py` | 1.2, 1.3, 1.6 (new file) |
| `docs/` | 2.13 |

---
---

## Error Messages & Validation

### [T1] 1.7 — Mode format validation

**Problem:** `mode.split("-")` → `ValueError: not enough values to unpack` with no guidance.
**Location:** `src/malet/plot.py:112`

| Current error | Situation | Suggested message |
| ------------- | --------- | ----------------- |
| `ValueError: not enough values to unpack (expected 3, got 2)` | `scatter-loss` instead of `scatter--loss` | `"Mode 'scatter-loss' has wrong format. Expected '{type}-{x_fields}-{metrics}' (exactly 2 dashes). For scatter, x_fields is empty: 'scatter--m1 m2'."` |

```python
parts = pcfg["mode"].split("-")
if len(parts) != 3:
    mode_type = parts[0] if parts else "unknown"
    hints = {
        "scatter": "scatter--metric1 metric2",
        "scatter_heat": "scatter_heat--m1 m2 m3",
        "heatmap": "heatmap-x1 x2-metric",
        "curve": "curve-x_field-metric",
        "curve_best": "curve_best-x_field-metric",
        "bar": "bar-x_field-metric",
    }
    hint = hints.get(mode_type, "type-x_fields-metrics")
    raise ValueError(
        f"Mode '{pcfg['mode']}' has wrong format. "
        f"Expected '{{type}}-{{x_fields}}-{{metrics}}' (exactly 2 dashes). "
        f"Example: '{hint}'. For scatter, x_fields is empty: 'scatter--m1 m2'."
    )
mode, x_fields, metrics = parts
```

**Test:** `scatter-loss`, `curve_loss`, `heatmap-lr-wd-loss` → assert `ValueError` with hint.

### [T1] 1.8 — Filter special-value detection

**Problem:** `--filter 'step last'` → `AssertionError: Values {'last'} are not in field 'step'`.
**Location:** `src/malet/plot_utils/data_processor.py:85-88`

| Current error | Suggested message |
| ------------- | ----------------- |
| `AssertionError: Values {'last'} are not in field 'step': [1, 2, ..., 40]` | `"'last' is not a valid filter value for 'step'. Use --best_ref_x_fields 'last' or --filter 'step 40'."` |

```python
if validate:
    vs = pd.Index(idx.get_level_values(k).unique())
    bad = set(values) - set(vs.tolist())
    if bad:
        special = bad & {'last', 'first', 'best'}
        if special:
            raise ValueError(
                f"Special value(s) {special} cannot be used in --filter for field '{k}'. "
                f"To select the last/first/best value, use --best_ref_x_fields instead. "
                f"Or use the actual value: --filter '{k} {vs.max()}'"
            )
        assert not bad, f"Values {bad} are not in field '{k}': {sorted(vs.tolist())}"
```

### [T1] 1.9 — wandb field rename hints

**Problem:** `_step` (wandb name) → `X-field ['_step'] not in log` with no hint about the rename.
**Location:** `src/malet/plot.py:186-200`

| Current error | Suggested message |
| ------------- | ----------------- |
| `X-field ['_step'] not in log. Choose between {'lr', 'step', ...}` | `"X-field '_step' not found. After wandb import, '_step' is renamed to 'step'."` |

```python
_WANDB_RENAMES = {"_step": "step", "_runtime": "runtime", "_timestamp": "timestamp"}

missing_x = [x for x in x_fields if x not in log.df.index.names and x not in post_melt_k]
if missing_x:
    hints = [f"'{x}' → use '{_WANDB_RENAMES[x]}' (renamed after wandb import)"
             for x in missing_x if x in _WANDB_RENAMES]
    hint_str = (" Hint: " + "; ".join(hints)) if hints else ""
    raise KeyError(
        f"X-field {missing_x} not in log. "
        f"Choose between {set(log.df.index.names) | post_melt_k}.{hint_str}"
    )
```

Apply same pattern to filter keys, column-row fields, multi-line fields, and metrics.

### [T1] 1.10 — Centralized validation module

Consolidates 1.7, 1.8, 1.9 into a single testable module:

```python
# src/malet/plot_utils/validation.py
def _validate_mode(mode_str: str) -> tuple[str, str, str]: ...
def _validate_fields(log, x_fields, metrics, filter_keys, ml_fields):
    WANDB_RENAMES = {"_step": "step", "_runtime": "runtime", "_timestamp": "timestamp"}
    SPECIAL_VALUES = {"last", "first", "best"}
    ...
```

### [T2] 2.1 — Sparse metric + best_ref diagnostic

**Problem:** `best_ref_metric_field` with sparse metric → opaque `assert not df.empty`.
**Location:** `src/malet/plot.py:229-237`

| Current error | Suggested message |
| ------------- | ----------------- |
| `AssertionError: Values {'act_pres_mean'} are not in field 'metric': ['loss']` | `"Metric 'act_pres_mean' is not available after optimization. Try removing --best_ref_metric_field, or ensure both metrics are logged at the same steps."` |

```python
if df.empty:
    ref_metric = pcfg.get('best_ref_metric_field', '')
    if ref_metric:
        test_df = log.melt_and_explode_metric(dropna=False)
        has_main = any(
            not test_df[test_df.index.get_level_values("metric") == m]["metric_value"].dropna().empty
            for m in metrics
        )
        has_ref = not test_df[test_df.index.get_level_values("metric") == ref_metric]["metric_value"].dropna().empty
        if has_main and not has_ref:
            raise ValueError(
                f"best_ref_metric_field '{ref_metric}' has no non-NaN values. "
                f"This metric may be sparse (not logged at every step). "
                f"Fix: remove --best_ref_metric_field to optimize on the plotted metric directly."
            )
    raise AssertionError(
        f"Metrics {metrics}"
        + (f" and best_ref_metric_field '{ref_metric}' are" if ref_metric else " is")
        + f" NaN in given dataframe:\n{log.df}"
    )
```

### [T1] 1.4 — Function signature inspection (Fiddle-inspired)

Use `inspect.signature` to validate configs against the user's train function (no Fiddle dependency):

```python
def train(lr: float, optimizer: str, seed: int = 1) -> dict:
    ...

experiment = malet.Experiment("my_exp/", train)
# Malet inspects signature:
#   - Validates exp_config.yaml fields match parameter names
#   - Type-checks values (lr="high" → error: expected float)
#   - Identifies defaults (seed=1 → candidate for static config)
#   - If config has "learning_rate", suggests: "did you mean 'lr'?"
```

**Why T1:** Zero deps, zero workflow change. Works when hints exist, silently skips when they don't.

### [T1] 1.14 — Config schema extraction from argparse / absl FLAGS

Richer alternative to 1.4: extract config schema from the user's existing argument parser. These give type, default, choices, and help text — strictly more information than function type hints.

```python
# User's existing code (no Malet-specific changes):
parser = argparse.ArgumentParser()
parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--optimizer', choices=['adam', 'sgd'], default='adam')
parser.add_argument('--seed', type=int, default=1)

# Or with absl (which Malet already uses):
flags.DEFINE_float('lr', 0.01, 'learning rate')
flags.DEFINE_enum('optimizer', 'adam', ['adam', 'sgd'], 'optimizer type')
flags.DEFINE_integer('seed', 1, 'random seed')
```

Malet extracts from the parser object:

```python
experiment = malet.Experiment("my_exp/", train_fn, parser=parser)
# → validates exp_config.yaml fields match parser args
# → type-checks grid values against declared types
# → validates grid values against choices (['adam', 'sgd'])
# → if config has 'learning_rate', suggests: "did you mean 'lr'? (from --lr)"
```

Extraction is straightforward — both expose structured metadata:

```python
# argparse: parser._actions
for action in parser._actions:
    name = action.dest           # 'lr'
    type_ = action.type          # float
    default = action.default     # 0.01
    choices = action.choices     # None or ['adam', 'sgd']

# absl: FLAGS[name]
for name in FLAGS:
    flag = FLAGS[name]
    type_ = type(flag.value)     # float
    default = flag.default       # 0.01
```

**Why T1:** Zero new deps (argparse is stdlib, absl is already a Malet dep). User passes their existing parser — no code changes to the training script. Choices validation catches invalid grid values at experiment setup, not mid-run. 1.4 and 1.14 are complementary: use whichever the user's code provides (signature, parser, or FLAGS).

---

## UX & Output Control

### [T1] 1.11 — Output format and path control

**Problem:** Output hardcoded to PDF. No `--output_dir`.
**Location:** `src/malet/plot.py` lines 752, 755, ~827

```python
flags.DEFINE_enum("output_format", "pdf", ["pdf", "png", "svg", "jpg"],
                  "Output file format for plots.")
flags.DEFINE_string("output_dir", None, "Override default output directory.")
flags.DEFINE_integer("dpi", 150, "DPI for raster formats (png, jpg).")

# In save logic:
fmt = plot_config.get("output_format", "pdf")
dpi = plot_config.get("dpi", 150) if fmt in ("png", "jpg") else None
save_dir = plot_config.get("output_dir") or os.path.join(exp_folder, "figure", mode_str)
fig.savefig(os.path.join(save_dir, f"{save_name}.{fmt}"), format=fmt, dpi=dpi)
```

### [T2] 2.2 — Filter 'last'/'first' resolution

**Problem:** `--filter 'step last'` should resolve `last` to max step value.
**Depends on:** 1.8 (becomes fallback for unrecognized special values)

```python
def _resolve_special_filter_values(df, field_key, values):
    level = df.index.get_level_values(field_key)
    resolved = []
    for v in values:
        if v == 'last':
            resolved.append(level.max())
        elif v == 'first':
            resolved.append(level.min())
        else:
            resolved.append(v)
    return resolved

# Apply before each select_df call:
for fk in list(pflt):
    clean_k = fk.rstrip("!")
    if clean_k in log.df.index.names:
        pflt[fk] = _resolve_special_filter_values(log.df, clean_k, pflt[fk])
```

### [T1] 1.6 — Textual TUI for coordinator status

When `--host` or `--parallel` is active, show live terminal dashboard:

```
┌─ my_sweep ──────────────────────────────┐
│ Progress: ██████████░░░░░░░░ 24/42      │
│                                          │
│ Agent    Config  Status    Duration       │
│ gpu-01   #25     running   00:12:34       │
│ gpu-02   #26     running   00:08:21       │
│ gpu-03   —       idle      —              │
│                                          │
│ Last completed: #24 (loss: 0.0234)       │
│ Best so far:    #11 (loss: 0.0189)       │
└──────────────────────────────────────────┘
```

Works over SSH, no browser needed. Textual is pure Python and lightweight.

### Ungraded convenience ideas (from usage notes)

- **Better `--help`**: group flags by category (data, filtering, styling, optimization, I/O)
- **`--dry_run`**: show field handling and config selection without drawing
- **Default font size**: 22 is too large; consider 14 or per-project config
- **Color assignment persistence**: variant-to-color mapping should be deterministic and configurable via plot_config YAML
- **Per-run progress on wandb fetch**: `from_wandb_sweep` progress bar doesn't show per-run history fetch
- **Multi-metric overlay**: `curve-step-loss drift_from_init` with dual y-axes
- **Shaded min/max bands**: auto-detect `{name}_mean`, `{name}_min`, `{name}_max` pattern
- **Filter groups**: group syntax in `--filter` for complex queries
- **Annotation options**: choose which values to annotate
- **Plot individual seed points**: show per-seed data points in addition to mean curves (from `old_notes.md`)
- **Save data table alongside plot**: `malet-plot` should also save the filtered/processed DataFrame as TSV (from `old_notes.md`)

### [T2] 2.14 — New plot types (from `malep.md`)

- **Jitter/strip plot**: scatter with grid_fields, jittered on x-axis for visibility
- **Beeswarm plot**: non-overlapping point distribution
- **Violin plot**: distribution shape per group
- **Connected scatter plot**: scatter with line connecting sequential points
- **Bubble plot**: scatter with size as third dimension
- **Diff plot**: difference between two metrics/runs

Each needs design decisions for how fields map to axes/aesthetics.

### [T2] 2.19 — REGEX field derivation (from `malep.md`)

Use regex patterns to derive x-fields from metric field names. Example: extract layer index from `grad_rank/module0.blocks.2.sa.c_k.weight` → x-axis = block index.

### [T2] 2.20 — Export compiled plot as standalone Python script (from `malep.md`)

After `malet-plot` generates a figure, export a self-contained `.py` file that reproduces the plot with hardcoded data + matplotlib calls. Useful for fine-tuning figures for papers without re-running the full pipeline.

---

## Code Quality

### [T1] 1.12 — Bare exception cleanup

At least 5 locations use bare `except:` (lines ~387, 572, 627, 1397):

```python
# Current (line ~387):
except:
    return l  # Swallows TypeError, ValueError, AND KeyboardInterrupt

# Current (line ~627):
except:
    raise Exception("Error while reading log file")  # Loses traceback
```

Replace with narrowest applicable type:

- `str2value` conversions: `except (ValueError, SyntaxError)`
- TSV parsing: `except (ValueError, KeyError, pd.errors.ParserError)`
- WandB API calls: `except (wandb.errors.Error, KeyError, ValueError)`
- Generic fallbacks: `except Exception` (not `KeyboardInterrupt`)
- Chain: `raise MaletError("...") from e`

### [T1] 1.13 — DataFrame monkey-patch removal

`experiment.py:305-314` monkey-patches `pd.DataFrame.set_index` globally:

```python
pd.DataFrame.set_index = lambda self, idx, *__, **_: self if not idx else self.old_set_index(idx, *__, **_)
```

Replace with explicit checks at the 2-3 call sites:

```python
if grid_fields:
    df = df.set_index(grid_fields)
```

### [T1] 1.15 — Dependency version ranges

**Problem (from `malep.md`):** pyproject.toml uses exact pins for some deps. Should use ranges based on which API surface Malet actually uses.

Audit needed for: `numpy` (np.array, np.arange, np.nan, np.isscalar), `pandas` (pd.concat, df.drop, .apply, .set_index, .reset_index, .to_csv, .loc).

Change `==` → `>=x.y, <z.0` based on when APIs were introduced and when breaking changes occurred.

### [T2] 2.18 — Testing infrastructure

**Problem (from `malep.md`):** No structured test suite. Key areas from `malep.md`:

- **ConfigIter:** grid expansion, group handling, bracket expressions
- **Experiment:** no-split execution, split mode, filelock race condition tests
- **ExperimentLog:** add_result, merge, parse_tsv edge cases
- **Plot:** plot_configs parsing, mode validation, each plot type

Prioritize by bug frequency. The `src/tests/` directory exists (per git status) but needs structured coverage.

---

## Identity & Schema Evolution

### [T1] 1.1 — Content-addressable experiment identity (git-style hashing)

Three levels of identity:

```python
experiment_id = sha256(
    commit_hash +
    hash(canonical_json(sorted(grid_fields + static_field_names))) +
    hash(canonical_json(config_values))
)
```

- **Schema hash** = `hash(field_names + field_types)` — "same experiment design?"
- **Config hash** = `hash(schema_hash + config_values)` — "same hyperparameter point?"
- **Run hash** = `hash(config_hash + commit_hash)` — "same code + same config?"

`Experiment.run()` compares `run_hash` before skipping. Code changed + same config → warn. Schema changed + alias exists → still matches.

**Why T1:** Solves the identity problem with zero workflow change. Git validated this model for 20 years.

### [T2] 2.9 — Typed config fields with semantic roles

```yaml
grid:
  - lr: [0.001, 0.01, 0.1]
    seed: [1, 2, 3]

schema:
  lr: { type: float, range: [1e-6, 10] }
  seed: { type: int, role: replicate }    # always averaged, never optimized
```

Roles: `hyperparameter` (optimize), `condition` (keep), `replicate` (average).

**Caveat:** Must be fully optional — everything works without it, roles just provide smart defaults.

### [T2] 2.10 — Config aliases for schema evolution

```yaml
schema:
  aliases:
    learning_rate: lr
    n_epochs: num_epochs
```

`merge()` uses aliases to match fields across renamed configs. `Experiment.run()` detects old results under `learning_rate` match current `lr`.

**Caveat:** One-level-only rule (no chains). Current name in `exp_config.yaml` is always canonical.

### [T1] 1.16 — Explicit schema definition with `PrjSchema` handler class

**Problem:** Malet currently infers grid vs static vs metric from the data — if a field has one value it's static, if it varies it's grid. This is fragile: a single-value `lr` is semantically grid but gets classified as static. Config schemas are implicit and undiscoverable.

**Proposal:** Users explicitly declare a schema as a Python dataclass. `PrjSchema` is the handler class that wraps it, validates configs, and generates CLI arguments.

**Schema definition** (Python dataclass — zero parsing, full type safety, IDE autocomplete):

```python
from typing import Annotated
from dataclasses import field
import malet

@malet.schema
class MySchema:
    # Grid fields — swept over in experiments
    optimizer: Annotated[str, malet.Grid(choices=["adam", "sgd", "muon"])] = "adam"
    lr: Annotated[float, malet.Grid()] = 0.01
    weight_decay: Annotated[float, malet.Grid()] = 0.0

    # Replicate fields — averaged over, never optimized
    seed: Annotated[int, malet.Replicate()] = 1

    # Static fields — fixed across all runs
    model: Annotated[str, malet.Static()] = "ResNet32"

    # Metric fields — logged outputs (no default, not set by user)
    loss: Annotated[float, malet.Metric()] = field(init=False)
    accuracy: Annotated[float, malet.Metric()] = field(init=False)
```

**Why Python, not YAML/TOML:**
- Zero parsing — it's just a class
- Full type safety from type hints — IDE catches `lr="high"` immediately
- Autocomplete and refactoring for free
- Users already write Python for experiments — adding a dataclass is natural
- `Annotated[]` metadata is standard Python (PEP 593), not a custom DSL

**`PrjSchema` class API:**

```python
# Load from any format
schema = PrjSchema.from_dataclass(MySchema)
schema = PrjSchema.from_toml("malet_schema.toml")
schema = PrjSchema.from_yaml("malet_schema.yaml")  # backward compat

# Generate CLI arguments (the key feature)
parser = schema.to_argparse()
# → adds --optimizer (choices=['adam','sgd'], help='Optimizer algorithm')
# → adds --lr (type=float, help='Learning rate')
# etc.

schema.define_absl_flags()
# → DEFINE_enum('optimizer', 'adam', ['adam','sgd'], 'Optimizer algorithm')
# → DEFINE_float('lr', 0.01, 'Learning rate')

# Extract schema from EXISTING user code (1.14 integration)
schema = PrjSchema.from_argparse(parser)     # reads parser._actions
schema = PrjSchema.from_absl_flags(FLAGS)    # reads flag definitions
schema = PrjSchema.from_signature(train_fn)  # reads type hints

# Validate configs
schema.validate({"optimizer": "adam", "lr": 0.01})    # OK
schema.validate({"optimizer": "rmsprop"})              # Error: not in choices
schema.validate({"learning_rate": 0.01})               # Error: did you mean 'lr'?

# Generate exp_config.yaml template
schema.to_exp_config(grid_values={"lr": [0.01, 0.1], "seed": [1, 2, 3]})

# Schema hash (for experiment identity — feeds into 1.1)
schema.hash()  # SHA256 of canonical (sorted fields + types + roles)

# Diff two schemas
PrjSchema.diff(old_schema, new_schema)
# → Added: weight_decay (float, grid)
# → Renamed: learning_rate → lr (alias detected)
# → Removed: warmup_steps
```

**Roles and their semantics:**

| Role | Meaning in Malet | Grid? | Averaged? | Optimized? |
| ---- | ---------------- | ----- | --------- | ---------- |
| `grid` | Hyperparameter to sweep over | Yes | No | Yes (via best_ref) |
| `static` | Fixed across all runs | No | — | — |
| `replicate` | Averaged across (e.g., seed) | Yes | Yes (always) | Never |
| `metric` | Logged output value | — | — | — |
| `condition` | Independent variable (not optimized) | Yes | No | No |

**Why ml_collections doesn't solve this:** ml_collections provides `ConfigDict` (attribute access, locking, field references) and `config_flags` (absl FLAGS integration). But it has no YAML support, no field roles, no schema versioning, no argparse generation, and no hashing. It solves runtime config management, not schema declaration. The concepts are complementary but the overlap is minimal.

**Why tyro/jsonargparse don't solve this either:** tyro generates argparse from dataclasses (good), but has no concept of `grid`/`replicate`/`metric` roles. jsonargparse loads YAML into argparse (good), but same — no experiment-management semantics. `PrjSchema` is the bridge between config libraries and experiment design.

**Why T1:** Pure Python, no new dependencies, no new file formats. Standard `dataclasses` + `typing.Annotated` (both stdlib). The `from_argparse()` and `from_absl_flags()` extractors (1.14) mean users don't even need to write a schema if they already have a CLI — Malet infers it. The key novelty is the `role` annotation (`Grid`, `Replicate`, `Static`, `Metric`), which no existing library provides.

### Format versioning

Add version to YAML header:

```yaml
[Static Configs]
__format_version__: 2
model: ResNet32
---------------------------------------------
```

`parse_tsv()` dispatches to appropriate parser. Old files default to version 1.

### [T2] 2.15 — Experiment metadata in log (from `malep.md`)

Store beyond just git commit: slurm job ID, slurm log path, run duration, datetime. `RunInfo` already captures some of this — extend it and make it queryable.

### [T2] 2.17 — Allocate default values for new fields in existing logs (from `malep.md`)

When a new grid field is added to `exp_config.yaml`, old logs lack that field. Malet should allocate a sentinel value (e.g., `None` or a user-specified default) for the new field in old log entries, enabling merge/comparison across schema versions. Must clearly distinguish "used default" from "was not measured."

---

## Execution & Parallelism

### [T1] 1.2 — `--parallel N` for local parallelism

```bash
# One command, everything happens
malet run experiments/my_sweep/ --parallel 4
```

Internally: coordinator forks 4 child processes pulling from `multiprocessing.Queue`. No TCP, no ports, no filelock.

Multi-machine (rarer):

```bash
malet run experiments/my_sweep/ --host              # coordinator
malet run experiments/my_sweep/ --connect host:8471  # agent
```

**Why T1:** `multiprocessing.Queue` is stdlib, race-free by construction. `--parallel 4` covers 90% of use cases.

### [T1] 1.3 — FastAPI/HTTP coordinator protocol (not gRPC)

At 20-1000 agents (~17-33 QPS), FastAPI uses 0.3% of its capacity. **gRPC-Python is actually slower** due to GIL.

| Factor | FastAPI | gRPC-Python |
| ------ | ------- | ----------- |
| Throughput (small payloads) | 10,000-20,000 req/s | 2,500-8,700 req/s |
| Debugging | curl, browser, Swagger | need grpcurl |
| Schema | Pydantic models (Python-native) | .proto + compilation |
| Client code | `httpx.post()` — 1 line | generated stubs |

gRPC wins at >50,000 QPS, >10KB payloads, or polyglot services. None apply here.

**Why T1:** Simpler, faster in Python, curl-debuggable. Also naturally serves the web dashboard on the same port.

### [T2] 2.7 — QueuedFileLock hardening

Current issues at 100-agent scale (per `old_notes.md`):

- `__read_queue()` / `__write_queue()` not atomic → concurrent corruption
- Silent failures: retries 10 times then returns empty list
- Hardcoded 3-hour timeout, fixed 0.05s poll interval
- No stale lock detection (crashed process leaves ID in queue)

Fixes:

1. **Atomic ops**: `os.replace()` via temp file
2. **Stale detection**: Record `(id, pid, timestamp)`, expire old entries
3. **Configurable timeout**: `lock_timeout` param on `ExperimentLog.__init__`
4. **Adaptive polling**: exponential backoff (0.05s → 1s) with jitter
5. **Crash recovery**: check PIDs alive via `os.kill(pid, 0)`

### Architecture rethink: remove splitting, separate status file (from `old_notes.md`)

An earlier design note proposes a fundamental change to parallel execution:

1. **Remove the splitting mechanism** entirely (predetermined `total_splits` / `curr_split`)
2. **Separate ExperimentLog into two files**: TSV for metric data, YAML for run status (running/completed/failed)
3. **Each worker gets its own log** file, merged at the end

This aligns with the coordinator model (1.2/1.3): the coordinator owns run status, workers write to individual log files, and merge happens centrally. The splitting mechanism becomes unnecessary because the coordinator assigns configs dynamically.

Note: this is largely superseded by the `--parallel N` / `--host` / `--connect` design (1.2, 1.3), but the "separate status file" idea has independent value — it would make run status queryable without parsing the full TSV.

---

## Storage & Data Model

### [T1] 1.5 — Storage backend interface

Hide format behind protocol (Parnas's decomposition principle):

```python
class StorageBackend(Protocol):
    def read(self, path: str) -> tuple[pd.DataFrame, dict]: ...
    def write(self, path: str, df: pd.DataFrame, static_configs: dict): ...
    def append(self, path: str, row: dict): ...

class TSVBackend(StorageBackend): ...      # current behavior, default
class ParquetBackend(StorageBackend): ...  # new, opt-in
```

Every future storage improvement becomes a new backend, not a rewrite of ExperimentLog.

### Parquet migration (via StorageBackend)

```
ExperimentLog.to_parquet(path)       # write long-format, partitioned by stat_type, zstd
ExperimentLog.from_parquet(path)     # lazy read, reconstruct MultiIndex
ExperimentLog.convert_tsv_to_parquet(tsv_path, parquet_dir)
```

Design: internal DataFrame stays as pandas. Static configs stored as Parquet metadata. Target: 10-50× size reduction, 5-20× faster single-metric reads. Optional dep: `pyarrow`.

### [T2] 2.21 — Nested Dremel-style columns for per-layer metrics

**Problem:** Per-layer metric columns encode model structure as flat strings: `grad_rank/module0.blocks.0.sa.c_k.weight`. This is the "5 attributes encoded as a string" problem from the database theory ref. Querying by layer structure (e.g., "all metrics for block 0", "compare across sublayers") requires string parsing.

**Observation:** The column namespace mirrors the model's `nn.Module` tree — `model.named_parameters()` returns the same paths. When logging per-layer stats (weight norms, gradient ranks, activation stats), you're projecting the module tree into column names.

**Proposal:** Use Parquet's nested schema (Dremel encoding) to preserve the tree structure:

```python
# Parquet schema with nested columns:
schema = pa.schema([
    ("run_id", pa.string()),
    ("step", pa.int32()),
    ("measurements", pa.struct({
        "grad_rank": pa.struct({
            "module0": pa.struct({
                "blocks": pa.list_(pa.struct({
                    "sa": pa.struct({
                        "c_k_weight": pa.float64(),
                        "c_v_weight": pa.float64(),
                    }),
                    "ffwd": pa.struct({...}),
                })),
            }),
        }),
        "act_frob_norm": pa.struct({...}),
    })),
])
```

This enables:
- **Column pruning by stat_type**: read `measurements.grad_rank` without touching `act_frob_norm`
- **Column pruning by layer depth**: read `.blocks[0]` without reading other blocks
- **Structural queries**: "all params in `sa` sublayers" without string parsing
- **Natural alignment with model architecture**: schema mirrors `nn.Module` tree

**Auto-generation from model:**

```python
# Build schema from PyTorch model
def schema_from_model(model, stat_types=["grad_rank", "act_frob_norm"]):
    """Generate nested Parquet schema mirroring model.named_parameters()."""
    layer_tree = {}
    for name, _ in model.named_parameters():
        parts = name.split(".")
        node = layer_tree
        for part in parts:
            node = node.setdefault(part, {})
    # Convert tree → pa.struct recursively
    ...
```

**Access patterns this enables:**

```python
# Current: string manipulation
block_0_cols = [c for c in df.columns if "blocks.0." in c and c.startswith("grad_rank/")]

# With nested schema: structured access
pq.read_table("measurements.parquet",
    columns=["measurements.grad_rank.module0.blocks.element[0]"])

# Or via DuckDB:
SELECT measurements.grad_rank.module0.blocks[1].sa.*
FROM read_parquet('measurements.parquet')
WHERE run_id = 'run_a'
```

**Relationship to other items:**
- Extends 1.5 (storage backend) with a nested-aware `ParquetBackend`
- Replaces the `layers` dimension table from 3.5 (star schema) — the layer structure is encoded in the schema itself, not in a separate table
- Connects to `treescope` (from `New tools to try out.md`) for visualizing the nested structure

**Caveat:** Deeply nested Parquet schemas add complexity to read/write code. PyArrow's nested struct support is good but requires careful schema construction. Most Malet users log scalar metrics (loss, accuracy), not per-layer stats — this is a power-user feature for model analysis workflows. Must be opt-in and invisible to users who don't need it.

**Caveat severity: Medium.** The schema generation from `nn.Module` is clean, but transforming existing flat column names into nested structs requires a reliable parser for the `stat_type/layer.path` convention. Edge cases in layer naming (dots in parameter names, numeric indices) need handling.

### [T2] 2.6 — Append-only checkpoint writes

**Theory (update anomaly):** `Experiment.update_log()` rewrites entire TSV to update one row. For 500 rows, every checkpoint rewrites 499 unchanged rows.

**Fix:** Append delta row. Deduplicate on read (last row per key wins). Compact periodically.

```python
def append_result(self, config, **metrics):
    row = {**{k: config[k] for k in self.grid_fields}, **metrics}
    with open(self.logs_file, 'a') as f:
        f.write('\t'.join(str(row[c]) for c in self._tsv_column_order) + '\n')
```

**Caveat:** YAML header makes pure append tricky. Need either `.tsv.wal` sidecar file or JSONL format. Crash recovery logic required.

### [T3] 3.5 — Star schema for large-scale logs

```
experiment_store/
├── runs.parquet
├── layers.parquet
├── summaries.parquet
└── measurements/
    ├── stat_type=grad_rank/data.parquet
    └── stat_type=train_loss/data.parquet
```

**Critical pitfall:** Only useful at >50MB. Adds new class + 2 deps for niche use case.

### [T3] 3.3 — Polars as primary DataFrame backend

5-20× speedup, but full API rewrite of every internal. Overkill for <50MB logs. Revisit if user base regularly exceeds 100MB.

### [T3] 3.4 — DuckDB query engine

~80MB dep. Most users don't need SQL. If storage backend supports Parquet, users can query with DuckDB directly — Malet doesn't need to wrap it.

---

## Bug Fixes & Data Processing

### [T2] 2.4 — `homogenize_df` and the `total_steps` problem

**Theory (2NF violation):** `total_steps` depends on `(config, metric)`, not `config` alone. `homogenize_df` treats it as config-dependent, filtering out metrics with different step counts.

**Example from `old_notes.md`:** `best_ref_metric_field='final_val_acc'` has `total_step=1`, plotted metric `emp_lip` has `total_step=100` → `emp_lip` gets filtered out.

```python
METRIC_DEPENDENT_FIELDS = {"step", "total_steps"}
def homogenize_df(df, ref_df, filt_dict, *exclude_fields):
    exclude_fields = set(exclude_fields) | METRIC_DEPENDENT_FIELDS
    ...
```

### [T2] 2.3 — Sparse metric cross-optimization

**Theory (panel data / missing data):** The sparse metric problem is a missing-data alignment problem.

```python
if pcfg["best_ref_metric_field"]:
    ref_metric = pcfg["best_ref_metric_field"]
    ref_df = df[df.index.get_level_values("metric") == ref_metric].dropna(subset=["metric_value"])
    if ref_df.empty:
        raise ValueError(
            f"best_ref_metric_field '{ref_metric}' has no non-NaN values. "
            f"Remove --best_ref_metric_field or use a different reference metric."
        )
    ref_best = avgbest_df(ref_df, "metric_value",
                          avg_over=avg_field, best_over=optimized_field,
                          best_of=best_of, best_at_max=pcfg["best_at_max"])
    main_df = avgbest_df(df, "metric_value", avg_over=avg_field)
    best_df = homogenize_df(main_df, ref_best, {}, "total_steps")
```

Alternative (from econometrics): LOCF (forward-fill sparse metric to all steps), or evaluate at intersection of observed steps only.

### [T2] 2.8 — Non-interactive merge conflict resolution

**Theory (lossless join):** `pd.concat` produces duplicates when logs overlap with different metrics for same config.

```python
ExperimentLog.merge(
    logs,
    on_conflict="interactive"  # default, current behavior
    # | "keep_first" | "keep_last" | "keep_best" | "raise"
)
```

### [T2] 2.5 — Summary cache (materialized view)

**Theory (OLAP):** `avgbest_df()` = GROUP BY + argmax/argmin. Runs from scratch on every `malet-plot` call.

```python
log.compute_summary(
    avg_over={"seed"},
    best_over={"lr", "weight_decay"},
    best_metric="val_loss",
    best_at_max=False,
)
# Saves to {exp_folder}/summary.parquet
# malet-plot reads summary when available, skips avgbest_df
```

Invalidate when new results are added.

### Lazy melt cache

**Theory (1NF):** `melt_and_explode_metric()` runs O(n×m×s) on every plot.

```python
@property
def melted_df(self) -> pd.DataFrame:
    if self._melted_cache is None or self._melted_dirty:
        self._melted_cache = self.melt_and_explode_metric()
        self._melted_dirty = False
    return self._melted_cache
```

Invalidate on write. Deeper fix: store long form on disk as `.parquet` alongside wide TSV.

### [T2] 2.16 — Global experiment log repository (from `malep.md`)

Reuse results from already-run configs across different experiments. A global log indexes all experiment logs with splits for fast lookup and an annotation CSV for config search.

**Caveat:** Schema matching across experiments is hard — same field name may mean different things. Stale results (code changed) must be detectable (addressed by 1.1 identity hashing). Needs careful design to avoid silently reusing invalid data.

### Prior issues (resolved, from `malep.md` archive)

- [x] Log disappearing during runs (rewrite race condition)
- [x] `.loc[(...,)]` indexing error for two-level multiindex in `add_result`
- [x] Infinite backslash problem: `[float, str, float]` → pandas saves with quotes → `str2value` re-escapes → grows on each read/write cycle

---

## Dashboard & Visualization

### [T2] 2.11 — Aim v3 integration

**Aim provides:** Interactive web UI, metric comparison, parallel coordinates, run grouping/tagging.
**Malet provides (and Aim doesn't):** Config-aware grid analysis (`avgbest_df`, `homogenize_df`), mode-string plotting with optimization, YAML config iteration, structured grid parallelism, merge/conflict resolution.

**Integration:** Malet exports → Aim displays.

```python
from aim import Run as AimRun

def export_to_aim(log: ExperimentLog, aim_repo: str = ".aim"):
    for config, metrics in log:
        run = AimRun(repo=aim_repo, experiment=log.name)
        run["config"] = config
        for metric_name, values in metrics.items():
            if isinstance(values, list):
                for step, val in enumerate(values):
                    run.track(val, name=metric_name, step=step)
            else:
                run.track(values, name=metric_name)
```

**Caveat:** Aim requires SDK ingestion (RocksDB backend, no file drops). Data duplication. ~50MB dep. NFS issues. v3 has no custom UI extensibility.

Recommended: hybrid approach — Textual TUI for live terminal monitoring, Aim for post-hoc web analysis.

### [T2] 2.12 — Marimo interactive analysis

```bash
malet analyze experiments/my_sweep/
# → opens pre-built marimo notebook at localhost:2718, reactive charts
```

**Caveat:** Young project (2023). matplotlib→Altair friction. Ship as optional `malet[analyze]` extra.

### [T3] 3.1 — Altair for interactive plots

**Critical pitfall:** 5,000 row default limit; browser struggles beyond ~100K. Malet's core value is handling large-scale data where matplotlib has no limit. **Cannot replace matplotlib.** Only viable as optional backend for dashboard views of pre-filtered data.

### [T3] 3.2 — Aim v4 (AimOS) custom dashboards

**Critical pitfall:** Development stalled since Oct 2023. Split from main repo because "Aim 4.0 and 3.0 are two different products." Use Aim v3 for now; if custom web UI needed, marimo or FastAPI+Plotly is safer.

---

## Documentation

### [T2] 2.13 — Documentation improvements

Must wait until validation fixes (1.7-1.10) are implemented so docs reflect final behavior.

#### Missing from current docs

- **wandb field name mapping:** `_step` → `step`, `_runtime` → `runtime`, `_timestamp` → `timestamp`
- **`best_ref_x_fields` accepted values:** `'last'` and `'best'` are special keywords, not field names
- **`from_wandb_sweep` `get_metrics`:** omitting it downloads ALL metrics (slow for large sweeps)
- **Sparse metric handling:** `best_ref_metric_field` requires reference metric at every step; workaround: omit it

#### Restructuring suggestions

- **End-to-end wandb example:** import → plot → interpret output
- **CLI flag reference table:** flag, type, default, description, example — easier to scan than `--help`
- **Common patterns page:** 5-10 most common `malet-plot` invocations as copy-pasteable templates
- **Troubleshooting page:** error → fix table

#### File changes

- `docs/advanced/wandb-integration.md` — field mapping table, `get_metrics` tip
- `docs/plotting/styling.md` — `best_ref_x_fields` special values table
- `docs/troubleshooting.md` — new page, add to `docs/index.md` nav

---
---

## Appendix A: Theory & Analysis

Background from `tmp/ref/` that motivates the proposals above. Not actionable items — theoretical grounding.

### Reference architectures (from `Public google tools.md`)

- **Vizier** (Google) — blackbox/hyperparameter optimization service. Relevant as reference for how a coordinator distributes search points to workers. Malet's coordinator (1.2/1.3) is simpler (grid enumeration, not Bayesian optimization), but Vizier's fault-tolerance patterns (retry failed trials, checkpointing search state) are worth studying.
- **Xmanager** (DeepMind) — experiment management platform. Manages job submission, resource allocation, and experiment tracking at Google scale. Reference for how `malet run --host` could eventually integrate with cluster schedulers (Slurm, Kubernetes).
- **PyGlove** (Google) — Python object manipulation via decorators. Its approach to making any Python object "searchable" (mutating hyperparameters via symbolic manipulation) is an alternative to Malet's YAML-based `ConfigIter`. Not directly usable but conceptually interesting.

### Malet's data model through a relational lens

```
Functional dependencies:
  (grid_fields)  →  (metric_fields)        # the composite key
  static_configs →  constant per log file   # denormalized into YAML header
```

ExperimentLog is a **denormalized relation**: candidate key = composite `grid_fields` (MultiIndex), non-key attributes = `metric_fields` (columns), static_configs = separate dimension (YAML header). Sound 2NF for small logs, breaks down at scale.

### Decision framework mapping (from "Database Structural Decisions" ref)

| Decision | Current Malet | What Theory Says | Enhancement |
| -------- | ------------- | ---------------- | ----------- |
| **1. Granularity** | One row per config (wide, lists in cells) | "ONE metric across ALL runs → long format" | Long-form cache (2.5); plot reads only needed metric |
| **2. Normalization** | Single table + YAML header | "Normalize to eliminate anomalies" | YAML header is good. Optional star schema (3.5) for large logs |
| **3. Partitioning** | None (single file) | "Partition by first filter" → `stat_type` | Parquet partitioned by metric name |
| **4. Write path** | Full rewrite on every update | "Append-only, convert later" | Append-only checkpoints (2.6) |
| **5. Summary** | Recomputed every plot (`avgbest_df`) | "Pre-aggregate: last, best per run" | Summary cache (2.5) |
| **6. Read path** | Load entire df, filter in memory | "Push filter to storage layer" | Parquet predicate pushdown |
| **7. Schema evolution** | No versioning | "Schema history" | Format version in header |

---

## Appendix B: Usage Reference (AI Agent Guide)

Reference for AI agents and new users working with Malet v0.2.x.

### Core workflow

1. **Import data** — `ExperimentLog.from_wandb_sweep()` → TSV log file
2. **Plot** — `malet-plot` CLI (or `python -m malet.plot`) with experiment folder and mode string
3. **Outputs** — `{exp_folder}/figure/{mode}/{save_name}.pdf` automatically

### Mode string format

`{plot_type}-{x_fields}-{metrics}` — always exactly 2 dashes:

- `curve-step-loss` — line plot of loss over step
- `heatmap-lr weight_decay-loss` — heatmap (space-separated x_fields)
- `scatter--train_loss val_accuracy` — scatter (empty x_field, two metrics)

### Field types after `from_wandb_sweep(get_all_steps=True)`

- **Grid fields** → DataFrame MultiIndex (e.g., `variant`, `lr`)
- **Metric fields** → stored as lists (one value per step)
- After `melt_and_explode_metric()`: `_step` → `step`, `_runtime` → `runtime`
- Synthetic `total_steps` field added (max step per run)

### Key CLI flags

- `--multi_line_fields variant` — one line per variant
- `--filter 'step 40 / lr 0.01 0.1'` — filter rows; `!` suffix excludes; ranges with `0:100`
- `--best_ref_x_fields 'last'` — optimize at last step (`'last'`, `'best'`, or specific value)
- `--best_ref_metric_field 'loss'` — optimize using different metric
- `--noannotate` — disable annotation labels

### Known limitations

- `--best_ref_metric_field` requires reference metric at every step. Sparse metrics → assertion error. Workaround: omit it.
- `filter 'step last'` does not work. Use actual step number.
- Output always PDF to `{exp_folder}/figure/{mode}/`.
- No `--save` / `--output` flag.

### Typical command template

```bash
.venv/bin/python3 -m malet.plot \
  --exp_folder ./experiments/{sweep_name} \
  --mode 'curve-step-{metric}' \
  --multi_line_fields {grouping_field} \
  --best_ref_x_fields 'last' \
  --best_ref_metric_field '{optimization_metric}' \
  --noannotate \
  --font_size 14
```

---

## Appendix B: "Native Python for Everything" — Viability Review

A review of the Fiddle/XManager approach (configuration-as-code, no config files) and whether Malet should adopt it wholesale.

### What Fiddle does

`fdl.Config` wraps a callable and stores its arguments as mutable attributes:

```python
cfg = fdl.Config(MyModel, hidden_size=256, num_layers=4)
cfg.optimizer = fdl.Config(Adam, lr=0.001)  # nested configs
model = fdl.build(cfg)                       # recursively constructs

# auto_config: rewrites function AST to produce Config trees instead of objects
@auto_config
def build_model():
    return Sequential([Dense(128, relu), Dense(1, None)])
cfg = build_model.as_buildable()  # Config tree, nothing instantiated
```

Key features: `fdl.build()` (recursive construction), `fdl.Partial` (deferred construction), `fiddle.diffing` (config diff/patch), serialization to JSON (via fully-qualified Python paths).

### What XManager does

Pure-Python experiment launch — sweeps are Python loops:

```python
with xm_local.create_experiment('cifar10') as experiment:
    for lr, bs in itertools.product([0.1, 0.01], [32, 64]):
        experiment.add(xm.Job(executable=exe, args={'lr': lr, 'bs': bs}))
```

Deduplication via `identity='unique_string'`. Async execution with `asyncio`. Backends: local, Vertex AI, Kubernetes.

### Benefits of native Python configs

| Benefit | How it works | Malet relevance |
| ------- | ------------ | --------------- |
| IDE autocomplete | Configs are typed Python objects | High — config typos are a common Malet pain point |
| Type errors caught before runtime | mypy/pyright check config types | High — catches `lr="high"` at edit time |
| Refactoring works | Rename a param → all configs update | Medium — Malet configs are small enough to grep |
| Full expressiveness | Conditionals, loops, imports, inheritance | Medium — most Malet configs are flat grids |
| Debuggable | Set breakpoints in config code | Low — configs rarely need debugging |
| No parsing layer | No YAML/TOML parser, no schema validation | High — removes an entire class of bugs |

### Downsides of native Python configs

| Downside | Severity for Malet | Details |
| -------- | ------------------ | ------- |
| **Serialization is fragile** | **High** | Fiddle serializes class references as `"module.ClassName"`. Renaming or moving a class breaks saved configs. Malet needs to store configs in logs persistently — YAML/TSV are self-contained, Python class paths are not. |
| **No declarative overview** | **Medium** | You must run the code to see what the config actually is. A YAML file is readable by anyone (including non-Python tools, CI scripts, dashboards). |
| **Reproducibility harder** | **High** | A YAML config is self-contained. A Python config depends on the codebase state — same config file + different code version = different config. This is the exact identity problem Malet is trying to solve. |
| **Config diffing requires custom tooling** | **Medium** | Fiddle provides `fiddle.diffing`, but it's complex (alignment heuristics, DAG structure comparison). YAML diffs are just `diff`. |
| **auto_config is brittle** | **High** | Cannot handle control flow, nested functions, lambdas, classes, async, try/except, with blocks. AST rewriting via `libcst` — a heavy dep for a fragile feature. |
| **Barrier to entry** | **Low** | ML researchers already write Python. But `Annotated[float, malet.Grid()]` is more ceremony than `lr: [0.01, 0.1]` in YAML. |

### Verdict for Malet

**Adopt the philosophy selectively, not wholesale.**

What to take from Fiddle/XManager:
- **Python dataclass for schema** (1.16) — yes. This is the right move. Schema is a structural definition that benefits from type safety and IDE support.
- **`inspect.signature` for validation** (1.14) — yes. Fiddle's `auto_config` validates against function signatures. Malet should too, but without the AST rewriting.
- **Config diffing** — yes, useful for schema evolution (2.10). Simpler than Fiddle's DAG diffing since Malet configs are flat.
- **Sweeps as Python loops** — Malet's `ConfigIter` with `exp_config.yaml` is already good here. A pure-Python grid API could be a nice alternative:
  ```python
  experiment.sweep(
      lr=[0.01, 0.1],
      optimizer=["adam", "sgd"],
      seed=[1, 2, 3],
  )
  ```

What NOT to take:
- **fdl.Config/fdl.build** — Malet's configs are flat key-value pairs, not nested object graphs. Fiddle solves a different problem (constructing deep model architectures from configs). Overkill.
- **auto_config AST rewriting** — brittle, heavy deps, limited Python support. Malet should use `inspect.signature` (simple, reliable) instead.
- **Python-only config storage** — Malet logs must be serializable to persistent, self-contained formats (TSV, Parquet). Python class paths are not stable across code versions. Keep YAML/TSV for storage, use Python for declaration.

**The hybrid approach:**
```
Declaration:  Python dataclass (schema) + Python API (sweep definition)
Storage:      YAML (exp_config.yaml) + TSV/Parquet (logs)
Validation:   Python type hints + inspect.signature
```

This gets 80% of the "native Python" benefit (type safety, autocomplete, refactoring) without the serialization/reproducibility pitfalls. The schema dataclass generates the YAML config and validates it — the YAML is derived, not primary.

### Open questions for further review

1. **Should `exp_config.yaml` become optional?** If users define sweeps in Python (`experiment.sweep(lr=[0.01, 0.1])`), do they still need a YAML file? The YAML is currently the serialization format for grid configs — removing it means Python code IS the config, with all the reproducibility implications above.

2. **Should Malet's `Experiment` API look like XManager's?** XManager's `experiment.add(Job(...))` is imperative. Malet's current approach is declarative (define grid, run all). The imperative style is more flexible but loses the "experiment as a unit" property that enables deduplication and resumption.

3. **How do you hash a Python config?** Fiddle can hash `fdl.Config` objects (sorted arguments + function reference). But the hash includes function identity — if you refactor your model code, the hash changes even if behavior is identical. This is the fundamental tension between "config as code" and "config as data."
