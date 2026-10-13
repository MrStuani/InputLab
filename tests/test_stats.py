import pytest

from app.services.stats import compute_stats, percentile


def test_percentile_basic():
    data = [1, 2, 3, 4, 5]
    assert percentile(data, 0) == 1
    assert percentile(data, 50) == 3
    assert percentile(data, 100) == 5


def test_percentile_interpolates():
    assert percentile([10, 20], 50) == 15


def test_compute_stats():
    s = compute_stats([5, 1, 3, 2, 4])
    assert s["sample_count"] == 5
    assert s["mean"] == 3
    assert s["min_value"] == 1
    assert s["max_value"] == 5
    assert s["p50"] == 3


def test_single_sample_has_zero_std():
    assert compute_stats([7.5])["std_dev"] == 0.0


def test_empty_raises():
    with pytest.raises(ValueError):
        compute_stats([])