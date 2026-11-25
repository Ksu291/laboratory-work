# Подготовка таблиц
import pandas as pd


def prepare_data(april, may, carriers, clients):
    # Объединяем рейсы за апрель и май
    trips = pd.concat([april, may], ignore_index=True)

    # Добавляем столбец с месяцем
    trips["month"] = trips["date"].dt.to_period("M").astype(str)

    # Убираем повтор перевозчика в справочнике
    carriers = carriers.drop_duplicates(subset="carrier")

    # Добавляем к рейсам информацию о перевозчиках и клиентах
    trips_full = trips.merge(carriers, on="carrier", how="left")
    trips_full = trips_full.merge(clients, on="client", how="left")

    return trips, trips_full
