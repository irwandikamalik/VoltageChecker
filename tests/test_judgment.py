from app.core.judgment import Judgment


def test_voltage_normal():
    judgment = Judgment()

    result = judgment.check_voltage(
        voltage=24.0,
        lower=23.0,
        upper=25.0
    )

    assert result is True


def test_voltage_too_low():
    judgment = Judgment()

    result = judgment.check_voltage(
        voltage=22.0,
        lower=23.0,
        upper=25.0
    )

    assert result is False


def test_voltage_too_high():
    judgment = Judgment()

    result = judgment.check_voltage(
        voltage=26.0,
        lower=23.0,
        upper=25.0
    )

    assert result is False


def test_current_normal():
    judgment = Judgment()

    result = judgment.check_current(
        current=0.150,
        lower=0.100,
        upper=0.200
    )

    assert result is True


def test_current_too_high():
    judgment = Judgment()

    result = judgment.check_current(
        current=0.250,
        lower=0.100,
        upper=0.200
    )

    assert result is False


def test_boundary_value():
    judgment = Judgment()

    result = judgment.check(
        voltage=23.0,
        current=0.100,
        voltage_lower=23.0,
        voltage_upper=25.0,
        current_lower=0.100,
        current_upper=0.200
    )

    assert result == "OK"