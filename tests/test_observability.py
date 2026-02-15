from utils.observability import RequestMetrics, metrics_to_dict


def test_metrics_snapshot_contains_required_fields():
    metrics = RequestMetrics(estimated_cost_per_request_usd=0.01)
    metrics.record(latency_ms=100, is_error=False)
    metrics.record(latency_ms=200, is_error=True)

    data = metrics_to_dict(metrics.snapshot())

    assert data["total_requests"] == 2
    assert data["total_errors"] == 1
    assert data["latency_avg_ms"] >= 100
    assert data["latency_p95_ms"] >= 100
    assert data["requests_per_minute"] >= 1
    assert 0 <= data["error_rate"] <= 1
    assert data["cost_per_request_usd"] == 0.01
