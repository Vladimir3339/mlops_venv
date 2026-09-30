import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plt_temp import make_temperature_dataframe


def test_dataframe_is_sorted_and_preserves_temperatures() -> None:
    times = [
        "2026-09-30T03:00",
        "2026-09-30T01:00",
        "2026-09-30T02:00",
    ]
    temperatures = [12.5, 10.0, 11.25]

    dataframe = make_temperature_dataframe(times, temperatures)

    assert dataframe.columns.tolist() == ["time", "temperature_c"]
    assert len(dataframe) == 3
    assert dataframe["time"].astype(str).tolist() == [
        "2026-09-30 01:00:00",
        "2026-09-30 02:00:00",
        "2026-09-30 03:00:00",
    ]
    assert dataframe["temperature_c"].tolist() == [10.0, 11.25, 12.5]
