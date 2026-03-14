"""Shared fixtures for Malet tests."""

import os

import numpy as np
import pandas as pd
import pytest

from malet.experiment import ExperimentLog


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "_static", "figures")


@pytest.fixture(scope="session", autouse=True)
def ensure_figures_dir():
    """Create the figures output directory."""
    os.makedirs(FIGURES_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def resnet20_log():
    """Load the real CIFAR-10 ResNet20 experiment log."""
    tsv_file = os.path.join(FIXTURES_DIR, "cifar10_resnet20_log.tsv")
    log = ExperimentLog.from_tsv(tsv_file)
    return log, tsv_file


@pytest.fixture(scope="session")
def sample_log(tmp_path_factory):
    """Create a sample ExperimentLog with synthetic data for testing."""
    tmp = tmp_path_factory.mktemp("exp")
    tsv_file = str(tmp / "log.tsv")

    np.random.seed(42)

    grid_fields = ["optimizer", "lr", "seed"]
    metric_fields = ["train_loss", "val_accuracy"]
    static_configs = {"model": "ResNet18", "dataset": "cifar10", "num_epochs": 20, "batch_size": 128}

    optimizers = ["sgd", "adam"]
    lrs = [0.001, 0.01, 0.1]
    seeds = [1, 2, 3]

    rows = []
    for opt in optimizers:
        for lr in lrs:
            for seed in seeds:
                n_epochs = 20
                # Simulate training curves
                base_loss = 2.0 - (0.3 if opt == "adam" else 0.0) - lr * 5
                base_acc = 0.5 + (0.1 if opt == "adam" else 0.0) + lr * 2
                noise = np.random.randn(n_epochs) * 0.02 * seed

                train_loss = [max(0.1, base_loss * np.exp(-0.1 * e) + noise[e]) for e in range(n_epochs)]
                val_acc = [min(0.99, base_acc * (1 - np.exp(-0.15 * e)) + noise[e] * 0.5) for e in range(n_epochs)]

                rows.append({
                    "optimizer": opt,
                    "lr": lr,
                    "seed": seed,
                    "train_loss": train_loss,
                    "val_accuracy": val_acc,
                })

    df = pd.DataFrame(rows).set_index(grid_fields)
    log = ExperimentLog(df, static_configs, tsv_file)
    log.to_tsv()
    return log, tsv_file
