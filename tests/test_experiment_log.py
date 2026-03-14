"""Tests for ExperimentLog."""

from malet.experiment import ExperimentLog


class TestExperimentLog:
    def test_from_tsv(self, sample_log):
        log, tsv_file = sample_log
        loaded = ExperimentLog.from_tsv(tsv_file)
        assert len(loaded.df) == len(log.df)
        assert loaded.static_configs == log.static_configs

    def test_grid_dict(self, sample_log):
        log, _ = sample_log
        gd = log.grid_dict()
        assert "optimizer" in gd
        assert "lr" in gd
        assert "seed" in gd

    def test_isin_and_contains(self, sample_log):
        log, _ = sample_log
        cfg = {"optimizer": "adam", "lr": 0.01, "seed": 1}
        assert log.isin(cfg)
        assert cfg in log

    def test_get_metric_and_getitem(self, sample_log):
        log, _ = sample_log
        cfg = {"optimizer": "adam", "lr": 0.01, "seed": 1}
        metrics = log.get_metric(cfg)
        assert "train_loss" in metrics
        assert "val_accuracy" in metrics
        # __getitem__ should return the same
        assert log[cfg] == metrics

    def test_derive_field(self, sample_log):
        log, tsv_file = sample_log
        # Work on a copy
        log_copy = ExperimentLog.from_tsv(tsv_file)
        log_copy.derive_field("lr_group", lambda lr: "high" if lr >= 0.1 else "low", "lr", is_index=True)
        assert "lr_group" in log_copy.df.index.names

    def test_drop_fields(self, sample_log):
        _, tsv_file = sample_log
        log_copy = ExperimentLog.from_tsv(tsv_file)
        log_copy.drop_fields(["train_loss"])
        assert "train_loss" not in log_copy.df.columns

    def test_rename_fields(self, sample_log):
        _, tsv_file = sample_log
        log_copy = ExperimentLog.from_tsv(tsv_file)
        log_copy.rename_fields({"val_accuracy": "val_acc"})
        assert "val_acc" in log_copy.df.columns
        assert "val_accuracy" not in log_copy.df.columns

    def test_melt_and_explode(self, sample_log):
        log, _ = sample_log
        df_long = log.melt_and_explode_metric()
        assert "metric" in df_long.index.names
        assert "step" in df_long.index.names
        assert "metric_value" in df_long.columns

    def test_melt_last_step(self, sample_log):
        log, _ = sample_log
        df_last = log.melt_and_explode_metric(step=-1)
        # Each config should have exactly 1 step per metric
        steps = df_last.index.get_level_values("step").unique()
        assert len(steps) == 1
