from security.guardian_agent import GuardianAgent


def test_guardian_detects_high_risk_event():
    agent = GuardianAgent(block_threshold=0.8)
    events = [
        {
            "ip": "10.0.0.1",
            "status_code": 500,
            "user_agent": "sqlmap/1.7",
            "path": "/.env",
            "requests_per_minute": 160,
        }
    ]

    alerts = agent.scan(events)
    assert len(alerts) == 1
    assert alerts[0].ip == "10.0.0.1"
    assert alerts[0].score >= 0.8
