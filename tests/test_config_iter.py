"""Tests for ConfigIter."""

import os

from malet.experiment import ConfigIter

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestConfigIter:
    def test_basic_grid(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        # 3 seeds * 3 lrs * 2 optimizers = 18
        assert len(configs) == 18

    def test_static_configs(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        assert configs.static_configs["model"] == "ResNet18"
        assert configs.static_configs["dataset"] == "cifar10"

    def test_grid_dict(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        gd = configs.grid_dict
        assert set(gd.keys()) == {"seed", "lr", "optimizer"}
        assert len(gd["seed"]) == 3
        assert len(gd["lr"]) == 3
        assert len(gd["optimizer"]) == 2

    def test_indexing(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        cfg = configs[0]
        assert "model" in cfg
        assert "lr" in cfg

    def test_slicing(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        sliced = configs[0:5]
        assert len(sliced) == 5

    def test_filter_iter(self):
        configs = ConfigIter(os.path.join(FIXTURES_DIR, "exp_config.yaml"))
        original_len = len(configs)
        configs.filter_iter(lambda i, d: d["optimizer"] == "sgd")
        assert len(configs) < original_len
        for cfg in configs:
            assert cfg["optimizer"] == "sgd"
