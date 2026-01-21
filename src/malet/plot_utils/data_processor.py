
from __future__ import annotations

from typing import (Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple,
                    Union)

import numpy as np
import pandas as pd

ValueLike = Union[Any, List[Any], Tuple[Any, ...], Set[Any], np.ndarray, pd.Index]


def _as_list(v: ValueLike) -> List[Any]:
    """Normalize a filter value into a python list."""
    if isinstance(v, list):
        return v
    if isinstance(v, (tuple, set, np.ndarray, pd.Index)):
        return list(v)
    return [v]


def _ensure_index_levels(df: pd.DataFrame, keys: Iterable[str]) -> None:
    idx_names = set(df.index.names)
    missing = set(keys) - idx_names
    if missing:
        raise KeyError(f"filt_dict keys {missing} is not in df.index.names={df.index.names}")


def _subindex_on_levels(index: pd.MultiIndex, keep_levels: Sequence[str]) -> pd.MultiIndex:
    """
    Return a MultiIndex containing only keep_levels, in that order.
    """
    drop_levels = [lvl for lvl in index.names if lvl not in set(keep_levels)]
    sub_idx = index.droplevel(drop_levels) if drop_levels else index
    if list(sub_idx.names) != list(keep_levels):
        sub_idx = sub_idx.reorder_levels(list(keep_levels))
    return sub_idx


def select_df(
    df: pd.DataFrame,
    filt_dict: Dict[str, ValueLike],
    *exclude_fields: str,
    equal: bool = True,
    drop: bool = False,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Select df rows with matching values from ``filt_dict`` except ``exclude_fields``.

    This is a vectorized, single-pass version of the original implementation.

    Original behavior preserved:
    - Asserts that df is non-empty.
    - Asserts that filt_dict keys exist in df.index.names.
    - Validates that requested values exist in each index level.
    - Raises early if intermediate filtering yields an empty dataframe.
    - Supports ``equal`` (keep matches) and ``drop`` (drop filtered levels).

    Performance notes:
    - Builds ONE boolean mask and slices once, instead of repeated df.loc calls.
    - Avoids repeated DataFrame materialization inside Python loops.

    Args:
        df (pandas.DataFrame): DataFrame with MultiIndex.
        filt_dict (Dict[str, Any]): Mapping from index level to allowed values.
        exclude_fields (str): Index levels to exclude from filtering.
        equal (bool): If True, keep matching rows; otherwise exclude them.
        drop (bool): If True, drop filtered index levels.
        validate (bool): If True, run key/value existence checks.

    Returns:
        pandas.DataFrame: Filtered DataFrame.
    """
    assert not df.empty, "Given dataframe is empty."
    if not filt_dict: return df

    if validate:
        _ensure_index_levels(df, filt_dict.keys())

    filt_keys = [k for k in filt_dict.keys() if k not in set(exclude_fields)]

    idx = df.index
    mask = np.ones(len(df), dtype=bool)

    for i, k in enumerate(filt_keys):
        values = _as_list(filt_dict[k])

        if validate:
            vs = pd.Index(idx.get_level_values(k).unique())
            bad = set(values) - set(vs.tolist())
            assert not bad, f"Values {bad} are not in field '{k}': {sorted(vs.tolist())}"

        fltr = idx.get_level_values(k).isin(values)
        mask &= fltr if equal else ~fltr

        if validate and not mask.any():
            partial = {kk: filt_dict[kk] for kk in filt_keys[: i + 1]}
            raise AssertionError(
                f"Filter {k}:{values} return empty dataframe. Inspect {partial}"
            )

    out = df.loc[mask]

    if drop and filt_keys:
        out = out.reset_index([*filt_keys], drop=True)

    return out


def homogenize_df(
    df: pd.DataFrame,
    ref_df: pd.DataFrame,
    filt_dict: Dict[str, ValueLike],
    *exclude_fields: str,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Homogenize index values of ``df`` with reference to ``select_df(ref_df, filt_dict)``.

    Original intent (unchanged):
    - Align ``df`` so that its remaining index grid matches the grid induced by
      ``select_df(ref_df, filt_dict, drop=True)``.

    Original caveats (preserved verbatim):
    - grid should be complete, else some fields in filt_dict will be missing.
    - also, when metric in filt_dict, step and total_steps can be metric-dependent
      and could return empty df.

    Performance improvement:
    - Replaces per-row ``select_df`` + ``concat`` with a single vectorized
      MultiIndex membership test using ``isin``.

    Args:
        df (pandas.DataFrame): DataFrame to homogenize.
        ref_df (pandas.DataFrame): Reference DataFrame.
        filt_dict (Dict[str, Any]): Filter used to define the reference grid.
        exclude_fields (str): Index levels excluded from filtering.
        validate (bool): Run validation checks.

    Returns:
        pandas.DataFrame: Homogenized DataFrame.
    """
    ref_idx = select_df(ref_df ,filt_dict, *exclude_fields, drop=True, validate=validate).index

    if len(ref_idx) == 0:
        return df.iloc[0:0]

    keep_levels = list(ref_idx.names)
    sub_idx = _subindex_on_levels(df.index, keep_levels)
    mask = sub_idx.isin(ref_idx)
    return df.loc[mask]


def avgbest_df(
    df: pd.DataFrame,
    metric_field: str,
    avg_over: Set[str] = set(),
    best_over: Set[str] = set(),
    best_of: Dict[str, Any] = dict(),
    best_at_max: bool = True,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Average over ``avg_over`` and get best result over ``best_over``.

    Original semantics preserved:
    - ``avg_over``: aggregate (mean + SEM) over these index levels.
    - ``best_over``: choose hyperparameter values yielding best ``metric_field``.
    - ``best_of``: restrict best search to a fixed subset of index values,
      then apply the chosen hyperparameter globally.
    - ``best_at_max`` controls argmax vs argmin selection.

    Original internal logic (preserved):
    '''
    - aggregate index : avg_over, best_over
    - key index : best_of, others
    '''

    Performance improvements:
    - Vectorized filtering and grouping.
    - No repeated slicing inside loops.
    - ``homogenize_df`` uses index membership instead of concat.

    Args:
        df (pandas.DataFrame): Base dataframe to operate over.
        metric_field (str): Metric used to select best hyperparameter.
        avg_over (Set[str]): MultiIndex levels to average over.
        best_over (Set[str]): MultiIndex levels to select best over.
        best_of (Dict[str, Any]): Fixed index values for best selection.
        best_at_max (bool): True if larger metric is better.
        validate (bool): Enable validation checks.

    Returns:
        pandas.DataFrame: Processed DataFrame.
    """
    assert not df.empty, "Given dataframe is empty."
    if validate and metric_field not in df.columns:
        raise KeyError(f"metric_field='{metric_field}' not in df.columns={list(df.columns)}")

    df_fields = set(df.index.names)

    # avg over avg_over
    if avg_over:
        if validate:
            _ensure_index_levels(df, avg_over)

        df_fields -= set(avg_over)
        g = df.groupby([*df_fields], dropna=True, sort=False)
        df = g.mean(numeric_only=True)
        df[metric_field + "_std"] = g.sem(numeric_only=True)[metric_field]

        df_fields = set(df.index.names)

    # best result over best_over
    if best_over:
        if validate:
            _ensure_index_levels(df, best_over)
            _ensure_index_levels(df, best_of.keys())

        df_fields -= set(best_over)
        best_df = select_df(df, best_of, validate=validate)

        if df_fields:
            g = best_df.groupby([*df_fields], dropna=True, sort=False)[metric_field]
            idx = g.idxmax() if best_at_max else g.idxmin()
            best_df = best_df.loc[idx]
        else:
            idx = best_df[metric_field].idxmax() if best_at_max else best_df[metric_field].idxmin()
            best_df = best_df.loc[[idx]]

        df_fields -= set(best_of)
        df = homogenize_df(df, best_df, best_of, validate=validate)

    return df