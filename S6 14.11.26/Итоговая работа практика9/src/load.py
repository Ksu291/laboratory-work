# Загрузка исходных таблиц
import pandas as pd
import config


def load_data():
    april = pd.read_csv(config.RAW_DIR / "trips_april.csv", parse_dates=["date"])
    may = pd.read_csv(config.RAW_DIR / "trips_may.csv", parse_dates=["date"])
    carriers = pd.read_csv(config.RAW_DIR / "carriers.csv")
    clients = pd.read_csv(config.RAW_DIR / "clients.csv")
    plan = pd.read_csv(config.RAW_DIR / "plan.csv")

    return april, may, carriers, clients, plan
