from ai_engine import analyze_complaint


def test_critical_complaint():
    result = analyze_complaint(
        "Short circuit happened in kitchen"
    )

    assert result["category"] == "Electrical"
    assert result["risk"] == "Critical"
    assert result["risk_score"] == 95


def test_parking_complaint():
    result = analyze_complaint(
        "Parking space is not available"
    )

    assert result["category"] == "Parking"
    assert result["risk"] == "Low"