import math
import statistics


def percentile(sorted_values: list[float], p: float) -> float:
    """Percentil por interpolação linear. `sorted_values` precisa estar ordenada."""
    k = (len(sorted_values) - 1) * p / 100
    lower = math.floor(k)
    upper = math.ceil(k)
    if lower == upper:
        return sorted_values[int(k)]
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (k - lower)


def compute_stats(values: list[float]) -> dict:
    if not values:
        raise ValueError("Nenhuma amostra fornecida")
    ordered = sorted(values)
    return {
        "sample_count": len(ordered),
        "mean": statistics.fmean(ordered),
        "min_value": ordered[0],
        "max_value": ordered[-1],
        "std_dev": statistics.stdev(ordered) if len(ordered) > 1 else 0.0,
        "p50": percentile(ordered, 50),
        "p95": percentile(ordered, 95),
        "p99": percentile(ordered, 99),
    }