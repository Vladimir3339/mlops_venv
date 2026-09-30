from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
CSV_PATH = Path("temperature_24h.csv")
PNG_PATH = Path("temperature_24h.png")


def make_temperature_dataframe(
    times: list[str],
    temperatures: list[float],
) -> pd.DataFrame:
    """Создаёт отсортированную таблицу времени и температуры."""
    dataframe = pd.DataFrame(
        {
            "time": pd.to_datetime(times),
            "temperature_c": temperatures,
        }
    )
    return dataframe.sort_values("time").reset_index(drop=True)


def get_temperature_data() -> pd.DataFrame:
    """Запрашивает почасовую температуру Москвы и выбирает первые 24 часа."""
    params = {
        "latitude": 55.7558,
        "longitude": 37.6173,
        "hourly": "temperature_2m",
        "timezone": "Europe/Moscow",
    }

    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()

    hourly = payload["hourly"]
    return make_temperature_dataframe(
        hourly["time"][:24],
        hourly["temperature_2m"][:24],
    )


def save_plot(dataframe: pd.DataFrame, output_path: Path) -> None:
    """Строит и сохраняет график температуры."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dataframe["time"], dataframe["temperature_c"], marker="o")
    ax.set_title("Температура воздуха в Москве: первые 24 часа")
    ax.set_xlabel("Время")
    ax.set_ylabel("Температура, °C")
    ax.grid(True)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    dataframe = get_temperature_data()
    dataframe.to_csv(CSV_PATH, index=False)
    save_plot(dataframe, PNG_PATH)

    print(f"Сохранено строк: {len(dataframe)}")
    print(f"CSV: {CSV_PATH}")
    print(f"График: {PNG_PATH}")


if __name__ == "__main__":
    main()
